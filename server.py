"""
🐍 贪吃蛇 —— 后端排行榜服务

它做两件事：
  1. 收成绩（POST /scores）
  2. 发排行榜（GET /scores）

运行方式：
    python3 server.py
"""

import json
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

SCORE_FILE = "scores.json"


# ---------- 读数据 ----------
def load_scores():
    """从文件读全部成绩"""
    if not os.path.exists(SCORE_FILE):
        return []                       # 第一次运行，文件还不存在

    with open(SCORE_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------- 写数据 ----------
def save_scores(scores):
    """把全部成绩写回文件"""
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


# ---------- 接口 1：拿排行榜 ----------
@app.route("/scores", methods=["GET"])
def get_scores():
    scores = load_scores()

    # 按成绩从高到低排
    scores.sort(key=lambda r: r["score"], reverse=True)

    return jsonify(scores[:10])         # 只返回前 10 名


# ---------- 接口 2：交成绩 ----------
@app.route("/scores", methods=["POST"])
def add_score():
    data = request.get_json()

    name = data.get("name", "匿名玩家")
    score = int(data.get("score", 0))

    scores = load_scores()
    scores.append({"name": name, "score": score})
    save_scores(scores)

    # 返回这个玩家的名次
    scores.sort(key=lambda r: r["score"], reverse=True)
    rank = 1
    for r in scores:
        if r["name"] == name and r["score"] == score:
            break
        rank = rank + 1

    return jsonify({"ok": True, "rank": rank})


# ---------- 允许前端跨域访问 ----------
@app.after_request
def allow_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    print("🚀 后端启动中…  地址：http://localhost:5000")
    app.run(port=5000, debug=True)
