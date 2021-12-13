import os
import re
from urllib import error, request


def check_input_text(text: str) -> str:
    """
    入力されたテキストがcsaファイルのURLになっているかチェック

    チェック項目
    1. そもそも入力があるか（本来は入力がなければボタンがクリックできないように制御するもんだがstreamlitでは無理っぽい）
    2. 入力がURLの形式になっているか
    3. csa形式になっているか
    4. URLが有効か

    Args:
        text (str): 入力されたテキスト

    Returns:
        text(str): 入力されたテキスト（URLとして問題ないことを確認済み）
    """

    # チェック項目1
    if not text:
        raise ValueError("入力が確認できませんでした")

    # チェック項目12
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    if not re.match(pattern, text):
        raise ValueError("URLを入力してください")

    # チェック項目13
    if (extention := os.path.splitext(text)[1]) != ".csa":
        raise ValueError("csa形式のファイルを入力してください")

    # チェック項目14
    try:
        f = request.urlopen(text)
        f.close()
    except error.HTTPError:
        raise ValueError("csaファイルの存在が確認できませんでした")

    return text
