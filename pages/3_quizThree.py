import streamlit as st
import csv
import random

# ページ設定
st.set_page_config(page_title= "quiz3", layout = "wide")

# 初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False


st.title("🧠クイズ: このエルフの名前は？")
st.image("static/images/mimic.png", caption = "このエルフの名前は？", width = 400)

# ラジオボタンで選択
answer = st.radio(
    "選んでください",
    ["マルシル", "ゼーリエ", "ミスルン", "フリーレン"]
)

# ボタンで答える
if st.button("解答する") and not st.session_state.answered:
    st.session_state.answered = True #回答済みにする
    if answer == "フリーレン":
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error("不正解...")

if st.session_state.get("answered"):
    if st.button("➡ 結果を表示する"):
        st.session_state.answered = False  # 回答状態をリセット
        st.switch_page("pages/4_結果表示.py") # 結果ページへ遷移


st.markdown("---")  # 横線で区切る

st.subheader("クイズをやめて最初に戻りますか？")  # 見出しをつける

# 最初に戻る用
if st.button("🏠️最初に戻る"):
    st.session_state.score = 0 # スコアをリセット
    st.session_state.answered = False # 回答状態をリセット（念のため）
    st.switch_page("quiz_demo.py") # トップページへ遷移