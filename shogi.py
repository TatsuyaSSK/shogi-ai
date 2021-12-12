import streamlit as st

import utils

st.title("将棋アプリ解析君")

text = st.text_input("csaファイルのURLを入力してください")
submit_button = st.button(label="評価値を計算する")

if submit_button:
    csa_file_url = utils.check_input_text(text)
    st.write(csa_file_url)
