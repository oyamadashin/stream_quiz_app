import streamlit as st


# ページ設定
st.set_page_config(page_title= "quiz1", layout = "wide")

# 初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False


st.title("🧠クイズ: このモンスターの名前は？")
st.image("static/images/mimic.png", caption = "このモンスターの名前は？", width = 400)

# ラジオボタンで選択
answer = st.radio(
    "選んでください",
    ["ゴブリン", "ミミック", "スライム", "フリーレン"]
)

# ボタンで答える
if st.button("解答する") and not st.session_state.answered:
    st.session_state.answered = True #回答済みにする
    if answer == "ミミック":
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error("不正解...")

if st.session_state.get("answered"):
    if st.button("➡ 次のクイズへ"):
        st.session_state.answered = False  # 回答状態をリセット
        st.switch_page("pages/2_quizTwo.py")  # クイズ2ページへ遷移


st.markdown("---")  # 横線で区切る

st.subheader("クイズをやめて最初に戻りますか？")  # 見出しをつける

# 最初に戻る用
if st.button("🏠️最初に戻る"):
    st.session_state.score = 0 # スコアをリセット
    st.session_state.answered = False # 回答状態をリセット（念のため）
    st.switch_page("quiz_demo.py") # トップページへ遷移