from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json

app = Flask(__name__)
CORS(app)

@app.route('/get_score', methods=['POST'])
def get_score():
    article_url = request.json['url']
    url = "https://bizapi.csdn.net/trends/api/v1/get-article-score"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "X-Ca-Key": "203930474",
        "X-Ca-Nonce": "f48fbdf5-f166-4f33-aad3-9178bdd7990a",
        "X-Ca-Signature": "Dm5IRgsgWZ+4juiGSEOpsenOfYgbr0MTdWc0k7Pg5bY=",
        "X-Ca-Signature-Headers": "x-ca-key,x-ca-nonce",
        "X-Ca-Signed-Content-Type": "multipart/form-data",
    }
    data = urllib.parse.urlencode({"url": article_url}).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        score = json.loads(response.read().decode())['data']['score']
    return jsonify(score=score)

if __name__ == '__main__':
    app.run(debug=True)
