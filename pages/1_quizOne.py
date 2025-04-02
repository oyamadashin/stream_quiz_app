import streamlit as st
import csv
import random

# ページ設定
st.set_page_config(page_title= "quiz1", layout = "wide")

# 初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# csv読み込み
with open("resources/quiz_questions.csv", encoding="UTF-8") as f:
    reader = csv.DictReader(f)
    quiz_list = list(reader)

# 難易度でフィルタリング
target_level = 1
filtered_quiz_list = [quiz for quiz in quiz_list if int(quiz["level"]) == target_level]

# ランダムに1問選ぶ
quiz = random.choice(filtered_quiz_list)

# 選択肢をシャッフルする
choices =[quiz["choice1"], quiz["choice2"], quiz["choice3"], quiz["choice4"]]
random.shuffle(choices)

st.title("🧠問題1（初級編）")
st.image("static/images/mimic.png", caption = quiz["question"], width = 400)

# ラジオボタンで選択
answer = st.radio(
    "選んでください",
    choices
)

# ボタンで答える
if st.button("解答する") and not st.session_state.answered:
    st.session_state.answered = True #回答済みにする
    if answer == quiz["answer"]:
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