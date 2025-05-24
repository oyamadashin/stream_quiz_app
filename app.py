import streamlit as st
import pandas as pd
import numpy as np
import csv
import random
import time
from supabase import create_client, Client
import base64
import os

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
if "player_name" not in st.session_state:  # プレイヤー名
    st.session_state.player_name = None
if "total_score" not in st.session_state:  # 総得点
    st.session_state.total_score = 0
if "start_time" not in st.session_state:  # クイズ開始時間
    st.session_state.start_time = None
if "start_time" not in st.session_state:  # クイズ終了時間
    st.session_state.start_time = None
if (
    "score_uploaded" not in st.session_state
):  # supabaseにアップロードする回数を1回きりにするために使う
    st.session_state.score_uploaded = False
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


# Supabaseと通信するためのクライアントインスタンスを生成
@st.cache_resource  # 毎回通信すると重くなるのでキャッシュする
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    return supabase


supabase = get_supabase_client()


# 名前を最終点数のデータをsupabaseに書き込むための関数
def write_score(player_name, elapsed_time, score_efficiency):
    data = {
        "player_name": st.session_state.player_name,
        "total_score": st.session_state.total_score,
        "elapsed_time": elapsed_time,
        "score_efficiency": score_efficiency,
    }
    response = supabase.table("scores").insert(data).execute()
    return response


# クイズページに表示する難易度の名称リスト
level_name = ["初級編", "中級編", "上級編"]


# ページ遷移処理
def go_to(page_num):
    st.session_state.page = page_num
    st.rerun()  # 強制的にスクリプト再実行（これをやらないと、その実行回でのpage_numのまま最後までスクリプトが実行されてしまう）


# スタート画面
def show_start():
    with center:
        st.markdown(
            """
            <style>
            .outlined-text{
            font-size: 70px;
            font-weight: bold;
            color: black;      
            text-shadow:
                -1px -1px 5px white,
                1px -1px 5px white,
                -1px 1px 5px white,
                1px 1px 5px white;
            }
            </style>
            <div class="outlined-text">🌏環境情報クイズ</div>
            """,
            unsafe_allow_html=True,
        )

        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        image = "./static/images/top_pic.png"
        encode_image = get_base64_image(image)

        css = f"""
        <style>
            .stApp{{
                background-image: url("data:image/png;base64,{encode_image}");
                background-size: cover;
                background-position: center;
                background-color:rgba(255,255,255,0.4);
            }}
            .stApp > header {{
                background-color: transparent;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

        # TODO ランキング表示用の名前を入力してもらう
        st.session_state.player_name = st.text_input(
            "ランキング表示用の名前（自由に変更できます）", value="とおりすがり"
        )
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
                st.session_state.score += 1  # 正解数加算
                if st.session_state.target_level == 1:  # 正解得点加算
                    st.session_state.total_score += 20
                elif st.session_state.target_level == 2:
                    st.session_state.total_score += 30
                elif st.session_state.target_level == 3:
                    st.session_state.total_score += 50

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
    elapsed_time = st.session_state.end_time - st.session_state.start_time
    score_efficiency = st.session_state.total_score / np.sqrt(elapsed_time)

    left_col, right_col = st.columns(2)
    with left_col:
        st.title(f"{st.session_state.player_name}さんの成績")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="正解数", value=st.session_state.score)
        with col2:
            st.metric(label="得点", value=st.session_state.total_score)
        with col3:
            st.metric(label="回答時間", value=f"{round(elapsed_time, 1)}秒")

        # 得点に応じてご褒美画像を提示
        left, center, right = st.columns([0.5, 1, 2])
        with center:
            if st.session_state.score == 3:
                st.image(
                    "static/images/kujira.png",
                    width=300,
                    caption="画像素材提供：てがきっず、いらすとや",
                )
            elif st.session_state.score == 2:
                st.image(
                    "static/images/kuma.png",
                    width=300,
                    caption="画像素材提供：てがきっず、いらすとや",
                )
            elif st.session_state.score == 1:
                st.image(
                    "static/images/shika.png",
                    width=300,
                    caption="画像素材提供：てがきっず、いらすとや",
                )
            else:
                st.image(
                    "static/images/marimo.png",
                    width=300,
                    caption="画像素材提供：てがきっず、いらすとや",
                )

        if not st.session_state.score_uploaded:
            # プレイヤー名と得点をsupabaseに送信
            write_score(st.session_state.player_name, elapsed_time, score_efficiency)
            st.session_state.score_uploaded = True

    with right_col:
        st.title("ランキング")

        response = (
            supabase.table("scores")
            .select("player_name, total_score, elapsed_time")
            .order("total_score", desc=True)  # まずは点数のよい順で並べ
            .order("elapsed_time", desc=False)  # その中で、回答時間の短い順で並べる
            .limit(10)
            .execute()
        )

        if response.data:
            df = pd.DataFrame(response.data)
            df.index = range(1, len(df) + 1)
            df["elapsed_time"] = df["elapsed_time"].apply(lambda t: round(t, 1))

            df_display = df.rename(
                columns={
                    "player_name": "名前",
                    "total_score": "得点",
                    "elapsed_time": "回答時間（秒）",
                }
            )
            df_display
        else:
            st.write("ランキングデータがまだありません。")

    left_col1, col1, col2, right_col2 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("最初に戻る"):
            st.session_state.score = 0  # 正解数をリセット
            st.session_state.total_score = 0  # 合計得点をリセット
            st.session_state.answered = False  # 回答状態をリセット（念のため）
            st.session_state.pyaler_name = None  # プレイヤー名をリセット
            st.session_state.target_level = 1
            st.session_state.score_uploaded = False
            go_to("start")  # トップページへ遷移
    with col2:
        if st.button("解説をみる"):
            st.session_state.answered = False  # 回答状態をリセット（念のため）
            go_to("explanation")  # 解説ページへ遷移


def show_explanation():
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    for i, level in enumerate(level_name):
        with columns[i]:

            st.title(f"問題{i + 1} ({level})の解説")
            st.write(f"問題：{st.session_state.shown_quiz.iloc[i, 0]}")
            st.write(f"正解：{st.session_state.shown_quiz.iloc[i, 1]}")

            with st.expander("解説を表示"):
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
        st.session_state.score = 0  # 正解数をリセット
        st.session_state.total_score = 0  # 合計得点をリセット
        st.session_state.pyaler_name = None  # プレイヤー名をリセット
        st.session_state.answered = False  # 回答状態をリセット（念のため）
        st.session_state.target_level = 1
        st.session_state.score_uploaded = False
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
