import numpy as np
import torch
from cshogi import CSA
from cshogi import HuffmanCodedPos, HuffmanCodedPosAndEval, Board, BLACK, move16
from features import FEATURES_NUM, make_input_features, make_move_label, make_result
from policy_value_resnet import PolicyValueNetwork


class KifEvaluator():
  def __init__(self, checkpoint_path, device):
    # モデルの読み込み
    self.model = PolicyValueNetwork()
    # デバイスの指定
    self.device = torch.device(device)
    self.model.to(device)
    # チェックポイントの読み込み
    self.checkpoint = torch.load(checkpoint_path, map_location=self.device)
    self.model.load_state_dict(self.checkpoint["model"])
    self.model.eval()

  def csa_to_features(self, csa_path):
    # csaファイル1つに1対局が格納していることを想定しているので0番目の要素を取得
    kif = CSA.Parser.parse_file(csa_path)[0]
    board = Board()
    move_num = len(kif.moves)
    # 出力用の配列
    torch_features = torch.empty((move_num + 1, FEATURES_NUM, 9, 9), dtype=torch.float32, device=torch.device(self.device))
    # make_input_featuresがnumpyでしか動作しないのでnumpy型に変換
    np_features = torch_features.numpy()
    # 初期局面の特徴量を生成
    make_input_features(board, np_features[0])
    # 1手目から終局までの特徴量を生成
    for i, move in enumerate(kif.moves):
      board.push(move)
      make_input_features(board, np_features[i+1])
    return torch_features

  def evaluate(self, csa_path):
    features = self.csa_to_features(csa_path)
    # モデルで評価値を算出
    _, y = self.model(features)
    # Tensorをnumpyに変換
    y = y.to('cpu').detach().numpy().copy()
    # 次元を削減
    y = np.squeeze(y)
    # シグモイドで出力する
    return (1 / (np.exp(-y) + 1))

if __name__ == '__main__':
    checkpoint_path = "../checkpoints/checkpoint-004.pth"
    device = "cpu"
    csa_path = "kyuubou1_shogi10_20211115_231924.csa"
    kif_evaluator = KifEvaluator(checkpoint_path, device)
    kif_evaluator.evaluate(csa_path)
