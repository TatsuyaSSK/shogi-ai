import os
import urllib.request

from google.cloud import storage


class CsaFetcher:
    def __init__(self, bucket):
        # # ちゃんと把握すること
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path
        # クライアントという概念がわからん
        self.client = storage.Client()
        # 棋譜保存先のバケットを取得
        self.bucket = self.client.get_bucket(bucket)

    def fetch_csa_file(self, url, upload_dir_path):
        # csaファイルのダウンロード
        csa_file_name = os.path.basename(url)
        urllib.request.urlretrieve(url, filename=csa_file_name)
        # アップロードするファイルをblobオブジェクトにする
        blob = self.bucket.blob(csa_file_name)
        # GCSにアップロードする
        upload_path = os.path.join(upload_dir_path, csa_file_name)
        blob.upload_from_filename(filename=upload_path)
        # ダウンロードしたファイルを削除する
        os.remove(csa_file_name)


if __name__ == "__main__":
    key_file_path = "kif-kaiseki-kun-project-4bfe10e90623.json"
    bucket = "sasaki-sample"
    url = "http://tk2-227-23463.vs.sakura.ne.jp/quest/kyuubou1/shogi10/kyuubou1_shogi10_20211115_231924.csa"
    upload_dir_path = ""
    csa_fetcher = CsaFetcher(key_file_path, bucket)
    csa_fetcher.fetch_csa_file(url, upload_dir_path)
    print("成功")
