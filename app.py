from flask import Flask, render_template_string, request, send_file, flash
import os
from pydub import AudioSegment

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max

HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>MP3 to WAV/FLAC</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
    .container { max-width: 600px; margin: 0 auto; }
    input, select, button { padding: 10px; margin: 10px 0; font-size: 16px; }
    button { background: #0077cc; color: white; border: none; cursor: pointer; }
    button:hover { background: #0055aa; }
  </style>
</head>
<body>
  <div class="container">
    <h2>🎵 MP3 to WAV/FLAC Converter</h2>
    <p>Convert your MP3 files to high-quality WAV or FLAC (lossless).</p>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="mp3_file" accept=".mp3" required><br>
      <label>Output Format:
        <select name="format">
          <option value="wav">WAV (Uncompressed)</option>
          <option value="flac">FLAC (Lossless Compressed)</option>
        </select>
      </label><br>
      <button type="submit">Convert Now</button>
    </form>
    <p><small>Your file is processed in memory and <strong>deleted immediately</strong> after download.</small></p>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        f = request.files['mp3_file']
        fmt = request.form['format']
        if f and f.filename.endswith('.mp3'):
            try:
                audio = AudioSegment.from_mp3(f.stream)
                output_filename = f.filename.rsplit('.', 1)[0] + '.' + fmt

                from io import BytesIO
                buf = BytesIO()
                audio.export(buf, format=fmt)
                buf.seek(0)

                return send_file(
                    buf,
                    mimetype='audio/wav' if fmt == 'wav' else 'audio/flac',
                    as_attachment=True,
                    download_name=output_filename
                )
            except Exception as e:
                return f"Error: {str(e)}", 400
        else:
            return "Please upload a valid MP3 file.", 400
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
