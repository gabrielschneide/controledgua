import os
import subprocess

# Instala dependências automaticamente
try:
    import flask
    import PyPDF2
    import requests
except ImportError:
    print("Instalando dependências...")
    subprocess.run(["pip", "install", "flask", "pypdf2", "requests"], check=True)
    import flask
    import PyPDF2
    import requests

from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Chave API fornecida
API_KEY = "AIzaSyBzwbCvx_LMKbGu3OiVmJzveXmW25Hfuk0"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files["file"]
    if file.filename == "":
        return "Nenhum arquivo selecionado", 400

    if file and file.filename.endswith(".pdf"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        texto = extrair_texto_pdf(filepath)

        return render_template("resultado.html", texto=texto[:1000])  # Mostra primeiros 1000 caracteres

    return "Formato inválido, envie um PDF", 400

def extrair_texto_pdf(filepath):
    with open(filepath, "rb") as f:
        leitor = PyPDF2.PdfReader(f)
        texto = "".join([pagina.extract_text() for pagina in leitor.pages if pagina.extract_text()])
        return texto.strip()

if __name__ == "__main__":
    app.run(debug=True)
