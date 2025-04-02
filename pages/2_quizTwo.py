import streamlit as st


# ページ設定
st.set_page_config(page_title= "quiz2", layout = "wide")

# 初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False


st.title("🧠クイズ: この魔法の名前は？")
st.image("static/images/zoru.jpg", caption = "この魔法の名前は？", width = 400)

# ラジオボタンで選択
answer = st.radio(
    "選んでください",
    ["ヒャダイン", "ゾルトラーク", "ホイミ", "だいたい何でも切る魔法"]
)

# ボタンで答える
if st.button("解答する") and not st.session_state.answered:
    st.session_state.answered = True #回答済みにする
    if answer == "ゾルトラーク":
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error("不正解...")

if st.session_state.get("answered"):
    if st.button("➡ 次のクイズへ"):
        st.session_state.answered = False  # 回答状態をリセット
        st.switch_page("pages/3_quizThree.py")  # クイズ2ページへ遷移


st.markdown("---")  # 横線で区切る

st.subheader("クイズをやめて最初に戻りますか？")  # 見出しをつける

# 最初に戻る用
if st.button("🏠️最初に戻る"):
    st.session_state.score = 0 # スコアをリセット
    st.session_state.answered = False # 回答状態をリセット（念のため）
    st.switch_page("quiz_demo.py") # トップページへ遷移