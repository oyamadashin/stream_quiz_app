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

# 画面を左、中央、右に1:2:1に分割
left, center, right = st.columns([1, 2, 1])

# csv読み込み
with open("resources/quiz_questions.csv", encoding="UTF-8") as f:
    reader = csv.DictReader(f)
    quiz_list = list(reader)

# 難易度でフィルタリング
target_level = 3
filtered_quiz_list = [quiz for quiz in quiz_list if int(quiz["level"]) == target_level]

# ランダムに1問選ぶ (初回だけ)
if "quiz" not in st.session_state:
    st.session_state.quiz = random.choice(filtered_quiz_list)
    choices = [st.session_state.quiz["choice1"], st.session_state.quiz["choice2"], st.session_state.quiz["choice3"], st.session_state.quiz["choice4"]]
    random.shuffle(choices)
    st.session_state.choices = choices

# セッションから読み出す
quiz = st.session_state.quiz
choices = st.session_state.choices


with center:
    st.title("❓問題3（上級編）")
    # TODO:画像はあとで
    # st.image(f"static/images/{quiz['image']}.png", caption = quiz["question"], width = 400)
    st.subheader(quiz["question"])

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
            del st.session_state.quiz
            del st.session_state.choices
            st.session_state.answered = False  # 回答状態をリセット
            st.switch_page("pages/4_結果表示.py")  # 結果ページへ遷移



    st.markdown("---")  # 横線で区切る

    st.subheader("クイズをやめて最初に戻りますか？")  # 見出しをつける

    # 最初に戻る用
    if st.button("🏠️最初に戻る"):
        st.session_state.score = 0 # スコアをリセット
        st.session_state.answered = False # 回答状態をリセット（念のため）
        st.switch_page("app.py") # トップページへ遷移