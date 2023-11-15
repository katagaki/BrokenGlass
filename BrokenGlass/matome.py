import os
import uuid

import openai
from PyPDF2 import PdfReader
from openai import OpenAI
from flask import render_template, request, Response

from BrokenGlass.decorators import authenticated_resource

from BrokenGlass import app

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="xxxxx"
)
files = {}


@app.route("/mypage/matome")
@authenticated_resource
def matome():
    return render_template("matome.html")


@app.route("/mypage/matome/upload", methods=["POST"])
@authenticated_resource
def matome_upload():
    file = request.files["file"]
    path = os.path.join("/tmp/com.kaminari.BrokenGlass/uploads", file.filename)
    try:
        os.makedirs("/tmp/com.kaminari.BrokenGlass/uploads")
    except FileExistsError:
        pass
    file.save(path)
    document = PdfReader(path)
    pages = document.pages
    all_text = []
    for page in pages:
        all_text.append(page.extract_text())
    id = str(uuid.uuid4())
    all_text = "".join(map(lambda text: text + "\n", all_text))
    files[id] = all_text
    return Response(id, mimetype="text/plain")


@app.route("/mypage/matome/stream")
@authenticated_resource
def matome_stream():
    try:
        return Response(summarize(files[request.args["id"]]), mimetype="text/event-stream")
    except openai.APIConnectionError:
        response = "まとめ中エラーが発生しました。"
        pass
    except openai.APIStatusError as e:
        response = e.message
    return render_template("matome.html", response=response)


def summarize(text: str):
    response = client.chat.completions.create(
        model="llama",
        messages=[
            {"role": "system",
             "content": """
                あなたは教授です。
                どんな複雑で読みづらい書類でも、一般人にでもわかりやすくなります。
                返答の書き方は、タイトルのあとにポイントフォームとなります。
                内容は、最大10個の点で、数字で整理し、改行で分けます。
                ユーザーが別の言語にするように言わない限り、常に日本語で返事します。
                まとめることができなければ、概要を言って、そのようにしたと述べます。
                """
             },
            {"role": "user",
             "content": f"この行のあとにXMLタグで囲まれたユーザーにアップロードされたドキュメントのテキストがあります。そのテキストの概要をまとめてください。\n<DOC>\n{text}\n</DOC>"
             }
        ],
        temperature=0.1,
        presence_penalty=-0.3,
        frequency_penalty=-0.2,
        stream=True
    )

    for line in response:
        text = line.choices[0].delta.content
        if len(text):
            yield f"data: {text}\n\n"

    # collected_chunks = []
    # collected_messages = []
    # for chunk in response:
    #     collected_chunks.append(chunk)
    #     chunk_message = chunk.choices[0].delta.content
    #     if chunk_message:
    #         collected_messages.append(chunk_message)
    #     print(f"{chunk_message}", end="", file=sys.stdout)
    #
    # return "".join(collected_messages)
