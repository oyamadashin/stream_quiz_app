import streamlit as st
import pandas as pd
import csv
import random
import time

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
if "start_time" not in st.session_state:  # クイズ開始時間
    st.session_state.start_time = None
if "start_time" not in st.session_state:  # クイズ終了時間
    st.session_state.start_time = None
if (
    "shown_quiz" not in st.session_state
):  # 回答者に提示されたクイズのデータフレーム（解説提示時に使う）
    st.session_state.shown_quiz = pd.DataFrame(
        [
            {
                "question": None,
                "answer": None,
                "explanation": None,
            },
            {
                "question": None,
                "answer": None,
                "explanation": None,
            },
            {
                "question": None,
                "answer": None,
                "explanation": None,
            },
        ]
    )

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
            st.session_state.start_time = time.time()
            go_to("quiz")


# クイズ画面
def show_quiz():
    if (
        st.session_state.quiz is None
    ):  # 初回のみ実行(これがないと、ユーザーがアクションするたびにクイズと選択肢がランダムに変化してしまう)
        # csv読み込み
        with open("resources/quiz_questions.csv", encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            quiz_list = []
            for row in reader:
                # 欠損値をNoneに変換して扱いやすくする
                cleaned_row = {
                    key: (value if value not in ["", "NA", "N/A", "none"] else None)
                    for key, value in row.items()
                }
                quiz_list.append(cleaned_row)
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
        # 解説ページ用のデータフレームに現在のクイズの内容、解答、解説を入力
        st.session_state.shown_quiz.iloc[st.session_state.target_level - 1, :] = (
            st.session_state.quiz["question"],
            st.session_state.quiz["answer"],
            st.session_state.quiz["explanation"],
        )

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
                    st.session_state.end_time = time.time()
                    go_to("result")


def show_result():
    with center:
        st.title("🏆 結果発表")
        st.success(f"あなたの正解数は{st.session_state.score}です！")
        st.write(
            f"回答にかかった時間は{round(st.session_state.end_time - st.session_state.start_time, 1)}秒です。"
        )

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

    left_col1, col1, col2, right_col2 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("最初に戻る"):
            st.session_state.score = 0  # スコアをリセット
            st.session_state.answered = False  # 回答状態をリセット（念のため）
            st.session_state.target_level = 1
            go_to("start")  # トップページへ遷移
    with col2:
        if st.button("解説をみる"):
            st.session_state.answered = False  # 回答状態をリセット（念のため）
            st.session_state.target_level = 1
            go_to("explanation")  # トップページへ遷移


def show_explanation():
    with center:
        for i, level in enumerate(level_name):

            st.title(f"問題{i + 1} ({level})の解説")
            st.write(f"問題：{st.session_state.shown_quiz.iloc[i, 0]}")
            st.write(f"正解：{st.session_state.shown_quiz.iloc[i, 1]}")

            explanation = f"""
            <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 8px; background-color: #f9fff9;">
            <strong>解説：</strong><br>
            {st.session_state.shown_quiz.iloc[i, 2]}
            </div>
            """
            st.markdown(explanation, unsafe_allow_html=True)

        st.markdown(
            "<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True
        )  # 1行空け

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
if st.session_state.page == "explanation":
    show_explanation()
