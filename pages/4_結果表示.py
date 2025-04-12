import streamlit as st

st.set_page_config(page_title= "結果", layout = "wide")
# 画面を左、中央、右に1:2:1に分割
left, center, right = st.columns([1, 2, 1])

with center:
    st.title("🏆 結果発表")

    if "score" in st.session_state:
        st.success(f"あなたの正解数は{st.session_state.score}です！")
        if st.button("最初に戻る"):
            st.session_state.score = 0 # スコアをリセット
            st.session_state.answered = False # 回答状態をリセット（念のため）
            st.switch_page("app.py") # トップページへ遷移

    else:
        st.warning("まだクイズに答えていません")


score = st.session_state.get("score", 0)

with center:
    if score == 3:
        st.image("static/images/kujira.png", width = 400, caption="画像素材提供：てがきっず、いらすとや")
    elif score == 2:
        st.image("static/images/kuma.png", width = 400, caption="画像素材提供：てがきっず、いらすとや")
    elif score == 1:
        st.image("static/images/shika.png", width = 400, caption="画像素材提供：てがきっず、いらすとや")
    else:
        st.image("static/images/marimo.png", width = 400, caption="画像素材提供：てがきっず、いらすとや")        