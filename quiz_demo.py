import streamlit as st

# ページ設定
st.set_page_config(page_title= "quiz_demo", layout = "wide")


st.title("環境情報クイズ（仮）")

st.image("static/images/top_pic.png", caption = "網走海浜での釣り人調査")

st.page_link("pages/1_quizOne.py", label = "👉環境情報クイズに挑戦する")
