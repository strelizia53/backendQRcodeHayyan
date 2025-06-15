from flask import Flask, request, jsonify, send_file
import cv2
# from pyzbar.pyzbar import decode
from PIL import Image
import os, tempfile

app = Flask(__name__)

def check_qr_damage(img_path):
    import cv2
    img = cv2.imread(img_path)
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    return "undamageQR" if data else "damageQR"


@app.route("/scan", methods=["POST"])
def scan_qr():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        f.save(tmp.name)
        label = check_qr_damage(tmp.name)
        os.remove(tmp.name)

    return jsonify({"result": label})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
