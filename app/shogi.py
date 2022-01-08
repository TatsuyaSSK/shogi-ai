from ssl import get_server_certificate
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
from utils import check_input_text, get_player_names
from get_kif_file import CsaFetcher
from vertex_ai import evaluate

st.title("将棋アプリ解析君")

text = st.text_input("csaファイルのURLを入力してください")
submit_button = st.button(label="評価値を計算する")

if submit_button:
    csa_file_url = check_input_text(text)
    csa_file_name = os.path.basename(csa_file_url)

    bucket_name = "sasaki-sample"
    csa_fetcher = CsaFetcher(bucket=bucket_name)
    csa_fetcher.fetch_csa_file(url=csa_file_url, upload_dir_path="")

    gcs_csa_file_path = f"gs://{bucket_name}/{csa_file_name}"
    evaluate_values = evaluate(gcs_csa_file_path)

    first_player_name, second_player_name = get_player_names(csa_file_url)

    # 描画
    fig, ax = plt.subplots(figsize=(12, 5))
    x = list(range(1, len(evaluate_values) + 1))
    ax.plot(x, evaluate_values)

    index = np.arange(0, len(evaluate_values) + 1, step=10).tolist()
    x_label = [f"{num}手目" for num in index]
    ax.set_xticks(index)
    ax.set_xticklabels(x_label)
    ax.axhline(y=0.5, lw=0.3, color="red")

    ax.set_title(f"先手：{first_player_name} 後手：{second_player_name}")
    plt.style.use("seaborn-darkgrid")
    plt.tight_layout()

    st.pyplot(fig)
