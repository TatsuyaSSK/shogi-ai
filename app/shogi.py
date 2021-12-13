import streamlit as st

import utils
from get_kif_file import CsaFetcher

st.title("将棋アプリ解析君")

text = st.text_input("csaファイルのURLを入力してください")
submit_button = st.button(label="評価値を計算する")

if submit_button:
    csa_file_url = utils.check_input_text(text)
    csa_fetcher = CsaFetcher(bucket="sasaki-sample")
    csa_fetcher.fetch_csa_file(url=csa_file_url, upload_dir_path="")
    st.write("upload done!")
