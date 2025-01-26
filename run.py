from flask import request, jsonify

from app import create_app
from app.main import process_video

app = create_app()
@app.route('/process_video', methods=['POST'])
def process_video_endpoint():
    """
    Endpoint to process a video sent as Base64 via POST request.
    """
    try:
        data = request.json
        base64_video = data.get('video')
        if not base64_video:
            return jsonify({"error": "No video provided"}), 400

        process_video(base64_video)
        return jsonify({"message": "Video processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run('0.0.0.0',debug=False)