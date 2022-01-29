import json
import numpy as np
from google.cloud import storage
from cshogi import CSA, Board
import torch
from policy_value_network_resnet10_swish import PolicyValueNetwork
from cshogi.dlshogi import make_input_features, FEATURES1_NUM, FEATURES2_NUM
from flask import Flask, request, Response, jsonify

model = PolicyValueNetwork()
device = torch.device("cpu")
model.to(device)
model_weight = torch.load("checkpoint_resnet10_swish-072.pth", map_location=device)
model.load_state_dict(model_weight["model"])
model.eval()


# ここからflaskの設定
app = Flask(__name__)

# flask route for liveness checks
@app.route("/healthcheck")
def healthcheck():
    status_code = Response(status=200)
    return status_code


# flask route for predictions
@app.route("/predict", methods=["GET", "POST"])
def predict():
    request_json = request.get_json(silent=True, force=True)
    data = request_json["instances"]
    csa_file_path = data[0]["csa_file_path"]

    csa_file_path_splitted = csa_file_path.split(
        "/"
    )  # bucket名とfile名の取得のためfile_pathを分割している　gs://bucket_name/file_nameを仮定
    bucket_name = csa_file_path_splitted[2]
    file_name = csa_file_path_splitted[3]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = storage.Blob(file_name, bucket)

    content = blob.download_as_text()

    kif = CSA.Parser.parse_str(content)[0]
    board = Board()
    move_num = len(kif.moves)
    # 出力用の配列
    torch_features_1 = torch.empty(
        (move_num + 1, FEATURES1_NUM, 9, 9),
        dtype=torch.float32,
        device=torch.device(device),
    )
    torch_features_2 = torch.empty(
        (move_num + 1, FEATURES2_NUM, 9, 9),
        dtype=torch.float32,
        device=torch.device(device),
    )
    # make_input_featuresがnumpyでしか動作しないのでnumpy型に変換
    np_features_1 = torch_features_1.numpy()
    np_features_2 = torch_features_2.numpy()
    # 初期局面の特徴量を生成
    make_input_features(board, np_features_1[0], np_features_2[0])
    # 1手目から終局までの特徴量を生成
    for i, move in enumerate(kif.moves):
        board.push(move)
        make_input_features(board, np_features1[i + 1], np_features_2[i + 1])

    _, y = model(torch_features_1, torch_features_2)
    # Tensorをnumpyに変換
    y = y.to("cpu").detach().numpy().copy()
    # 次元を削減
    y = np.squeeze(y)
    # シグモイドで出力する
    result = 1 / (np.exp(-y) + 1)
    result = result.tolist()  # numpy.ndarrayはjsonでシリアライズできないのでリストに変換

    # jsonでdump
    return json.dumps({"predictions": [{"evaluate_value": result}]})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
