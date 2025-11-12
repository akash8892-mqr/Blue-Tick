from flask import Flask, request, render_template, jsonify
from model import predict_fake_probability

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    prob = predict_fake_probability(url)
    return jsonify({"prob_fake": prob})

if __name__ == "__main__":
    app.run(debug=True)
