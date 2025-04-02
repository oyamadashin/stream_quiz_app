import streamlit as st

# ページ設定
st.set_page_config(page_title= "quiz_demo", layout = "wide")


st.title("🎯 フリーレンクイズ")

st.image("static/images/muhu.jpg")

st.page_link("pages/1_quizOne.py", label = "フリーレンクイズに挑戦する")
