from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify(message="Hello, world!")

@app.route('/search', methods=['GET'])
def search_video():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Please provide a search query."}), 400

    try:
        ydl_opts = {'quiet': True, 'simulate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{query}', download=False)
        
        videos = []
        for item in info.get('entries', []):
            # Extract the correct m4a format (audio-only)
            m4a_url = None
            for fmt in item.get('formats', []):
                if fmt['ext'] == 'm4a':
                    m4a_url = fmt.get('url')
                    break  # stop after the first m4a format found

            if m4a_url:
                video = {
                    'id': item['id'],
                    'title': item['title'],
                    'description': item['description'],
                    'm4a_url': m4a_url
                }
                videos.append(video)
            else:
                # In case no m4a format is available, you can handle that gracefully.
                video = {
                    'id': item['id'],
                    'title': item['title'],
                    'description': item['description'],
                    'm4a_url': "No m4a available"
                }
                videos.append(video)

        return jsonify(videos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
