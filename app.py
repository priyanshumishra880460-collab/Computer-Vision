from flask import Flask, request, jsonify
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# 🔑 Paste your Azure key & endpoint
key = "EBwcWa5ijkX9kJQ4YiQK0ESkZV5MNmOzmUIqS8qKV4tnCccZrdnwJQQJ99CDACqBBLyXJ3w3AAAFACOGQoxV"
endpoint = "https://vision-022.cognitiveservices.azure.com/"

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Analyze from URL
@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    image_url = data['image_url']

    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION]
    )

    caption = result.caption.text if result.caption else "No caption"
    return jsonify({"caption": caption})

# Analyze uploaded image
@app.route('/analyze-upload', methods=['POST'])
def analyze_upload():
    file = request.files['image']

    result = client.analyze(
        image_data=file.read(),
        visual_features=[VisualFeatures.CAPTION]
    )

    caption = result.caption.text if result.caption else "No caption"
    return jsonify({"caption": caption})

if __name__ == '__main__':
    app.run(debug=True)