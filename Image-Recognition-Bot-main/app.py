from flask import Flask, request, render_template, jsonify
import os
import google.generativeai as genai
import PIL.Image

app = Flask(__name__)

# Pass the API key directly
genai.configure(api_key="Use your api here- gemini flash 5.1")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image provided", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        img = PIL.Image.open(file_path)

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(["What is in this photo?", img])
        result = response.text

        return render_template('upload.html', result=result, image_path=file_path)

    return render_template('upload.html', result=None, image_path=None)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5000, debug=True)
