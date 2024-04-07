from flask import Flask, request, render_template, send_file
from libsif import SimplisticImageFormat
import os
from io import BytesIO

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

ALLOWED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods = ["POST"])
def convert():
    # print(request, request.files)
    if len(request.files) != 1:
        return "No files", 400  
    
    imageFile = request.files["image"]
    fileNameData = os.path.splitext(imageFile.filename)

    if fileNameData[1] not in ALLOWED_EXTENSIONS:
        return f"File format not allowed. Allowed formats : {', '.join(ALLOWED_EXTENSIONS)}"

    data = imageFile.read()
    # print(data)
    sifImage = SimplisticImageFormat.fromFileInMemory(data)
    sifImageBinaryData = sifImage.save("Yo.SIF", True)

    responseData = BytesIO(sifImageBinaryData)

    return send_file(responseData, "image/sif", True, fileNameData[0] + ".SIF")



if __name__ == "__main__":
    app.run(host = "0.0.0.0")