from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index2.html")

@app.route("/convert", methods=["POST"])
def convert():
    currency = request.form.get("currency")
    res = requests.get("http://data.fixer.io/api/latest?access_key=8827677973499660e6135528904334b2", params={
            "base" : "USD", "symbols" : currency})
    if res.status_code != 200:
        return jsonify({"success": False, "error": res.status_code})

    data = res.json()
    return jsonify({"success": True, "rate": data["rate"][currency]})
