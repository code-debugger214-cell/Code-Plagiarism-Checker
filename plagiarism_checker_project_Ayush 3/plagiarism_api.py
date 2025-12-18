import os
import difflib
import re
import ast
from flask import Flask, request, jsonify


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")
THRESHOLD = 70



def load_dataset(path):
    dataset = {}
    for file in os.listdir(path):
        if file.endswith(".py"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                dataset[file] = f.read()
    return dataset


dataset_codes = load_dataset(DATASET_PATH)



def text_similarity(c1, c2):
    return difflib.SequenceMatcher(None, c1, c2).ratio() * 100


def token_similarity(c1, c2):
    t1 = re.findall(r"[A-Za-z_]\w*", c1)
    t2 = re.findall(r"[A-Za-z_]\w*", c2)
    return difflib.SequenceMatcher(None, t1, t2).ratio() * 100


def line_similarity(c1, c2):
    return difflib.SequenceMatcher(None, c1.splitlines(), c2.splitlines()).ratio() * 100


def normalize_variables(code):
    try:
        tree = ast.parse(code)
        vars_found = sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)})
        for i, v in enumerate(vars_found):
            code = re.sub(rf"\b{v}\b", f"v{i}", code)
        return code
    except:
        return code


def variable_similarity(c1, c2):
    return difflib.SequenceMatcher(
        None,
        normalize_variables(c1),
        normalize_variables(c2)
    ).ratio() * 100


def control_flow_similarity(c1, c2):
    k1 = re.findall(r"\b(if|for|while|elif|else|try|except|with)\b", c1)
    k2 = re.findall(r"\b(if|for|while|elif|else|try|except|with)\b", c2)
    return difflib.SequenceMatcher(None, k1, k2).ratio() * 100



def compute_match_score(m):
    return round(
        0.35 * m["text"]
        + 0.20 * m["token"]
        + 0.20 * m["line"]
        + 0.15 * m["variable"]
        + 0.10 * m["control_flow"],
        2
    )


def plagiarism_risk(score):
    if score >= 85:
        return "HIGH"
    elif score >= THRESHOLD:
        return "MEDIUM"
    return "LOW"


def plagiarism_statement(score):
    if score >= THRESHOLD:
        return "The submitted source code is classified as plagiarised."
    return "The submitted source code is classified as original."


@app.route("/")
def home():
    return jsonify({
        "message": "Plagiarism Checker API is running",
        "endpoint": "/check",
        "method": "POST"
    })


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    user_code = data["code"]
    results = []

    for file, dataset_code in dataset_codes.items():
        metrics = {
            "text": text_similarity(user_code, dataset_code),
            "token": token_similarity(user_code, dataset_code),
            "line": line_similarity(user_code, dataset_code),
            "variable": variable_similarity(user_code, dataset_code),
            "control_flow": control_flow_similarity(user_code, dataset_code),
        }

        score = compute_match_score(metrics)

        results.append({
            "file": file,
            "match_score": score,
            "plagiarism_risk": plagiarism_risk(score),
            "threshold": THRESHOLD,
            "plagiarised": score >= THRESHOLD,
            "plagiarism_statement": plagiarism_statement(score),
            "detailed_metrics": {
                "overall_similarity": round(metrics["text"], 2),
                "token_similarity": round(metrics["token"], 2),
                "line_similarity": round(metrics["line"], 2),
                "variable_renaming_similarity": round(metrics["variable"], 2),
                "control_flow_similarity": round(metrics["control_flow"], 2),
            }
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return jsonify({
        "most_similar_file": results[0],
        "all_results": results
    })



if __name__ == "__main__":
    app.run(debug=True)
