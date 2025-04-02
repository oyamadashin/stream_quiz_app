import streamlit as st

# ページ設定
st.set_page_config(page_title= "quiz_demo", layout = "wide")


st.title("環境情報クイズ")

#TODO 画像差し替え
st.image("static/images/muhu.jpg")

st.page_link("pages/1_quizOne.py", label = "環境情報クイズに挑戦する")
