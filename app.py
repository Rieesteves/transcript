from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        transcribed_text = download_transcribe_youtube(youtube_url)
        return render_template('index.html', transcribed_text=transcribed_text)

    return render_template('index.html', transcribed_text=None)

def download_transcribe_youtube(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(file_extension='mp4').first()
        video.download('static/video.mp4')
        
        transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
