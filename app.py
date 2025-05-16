import streamlit as st
import csv
import random

# ページ設定
st.set_page_config(page_title="quiz_demo", layout="wide")

# 画面を3分割（左・中央・右）
left, center, right = st.columns([1, 2, 1])  # 1:2:1に分ける


# セッションステートメントの初期化
if "page" not in st.session_state:
    st.session_state.page = "start"
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "target_level" not in st.session_state:
    st.session_state.target_level = 1
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "choices" not in st.session_state:
    st.session_state.choices = None

# クイズページに表示する難易度の名称リスト
level_name = ["初級編", "中級編", "上級編"]


# ページ遷移処理
def go_to(page_num):
    st.session_state.page = page_num
    st.rerun()  # 強制的にスクリプト再実行（これをやらないと、その実行回でのpage_numのまま最後までスクリプトが実行されてしまう）


# スタート画面
def show_start():
    with center:
        st.title("環境情報クイズ（仮）")

        st.image("static/images/top_pic.png", caption="網走海浜での釣り人調査")
        if st.button("👉環境情報クイズに挑戦する"):
            go_to("quiz")


# クイズ画面
def show_quiz():
    if (
        st.session_state.quiz is None
    ):  # 初回のみ実行(これがないと、ユーザーがアクションするたびにクイズと選択肢がランダムに変化してしまう)
        # csv読み込み
        with open("resources/quiz_questions.csv", encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            quiz_list = list(reader)
        # 現在の難易度のクイズのみ抽出してリスト化
        filtered_quiz_list = [
            quiz
            for quiz in quiz_list
            if int(quiz["level"]) == st.session_state.target_level
        ]
        # クイズリストから1つをランダムに選択
        st.session_state.quiz = random.choice(filtered_quiz_list)
        # 現在のクイズの選択肢リストを作成した上で、シャッフルする
        choices = [
            st.session_state.quiz["choice1"],
            st.session_state.quiz["choice2"],
            st.session_state.quiz["choice3"],
            st.session_state.quiz["choice4"],
        ]
        random.shuffle(choices)
        st.session_state.choices = choices

    with center:
        st.title(
            f"❓問題{st.session_state.target_level}（{level_name[st.session_state.target_level - 1]}）"
        )
        st.subheader(st.session_state.quiz["question"])

        # ラジオボタンで選択
        answer = st.radio("選んでください", st.session_state.choices)

        # ボタンで答える
        if st.button("解答する") and not st.session_state.answered:
            st.session_state.answered = True  # 回答済みにする
            if answer == st.session_state.quiz["answer"]:
                st.success("正解！")
                st.session_state.score += 1
            else:
                st.error("不正解...")

        if st.session_state.target_level < 3:
            if st.session_state.get("answered"):
                if st.button("➡ 次のクイズへ"):
                    del st.session_state.quiz
                    del st.session_state.choices
                    st.session_state.answered = False  # 回答状態をリセット
                    st.session_state.target_level += 1
                    go_to("quiz")  # クイズ次ページへ遷移
        else:
            if st.session_state.get("answered"):
                if st.button("➡ 結果をみる"):
                    del st.session_state.quiz
                    del st.session_state.choices
                    st.session_state.answered = False  # 回答状態をリセット
                    go_to("result")


def show_result():
    with center:
        st.title("🏆 結果発表")
        st.success(f"あなたの正解数は{st.session_state.score}です！")

        # 得点に応じてご褒美画像を提示
        if st.session_state.score == 3:
            st.image(
                "static/images/kujira.png",
                width=400,
                caption="画像素材提供：てがきっず、いらすとや",
            )
        elif st.session_state.score == 2:
            st.image(
                "static/images/kuma.png",
                width=400,
                caption="画像素材提供：てがきっず、いらすとや",
            )
        elif st.session_state.score == 1:
            st.image(
                "static/images/shika.png",
                width=400,
                caption="画像素材提供：てがきっず、いらすとや",
            )
        else:
            st.image(
                "static/images/marimo.png",
                width=400,
                caption="画像素材提供：てがきっず、いらすとや",
            )

        if st.button("最初に戻る"):
            st.session_state.score = 0  # スコアをリセット
            st.session_state.answered = False  # 回答状態をリセット（念のため）
            st.session_state.target_level = 1
            go_to("start")  # トップページへ遷移


# ページの表示
if st.session_state.page == "start":
    show_start()
if st.session_state.page == "quiz":
    show_quiz()
if st.session_state.page == "result":
    show_result()
