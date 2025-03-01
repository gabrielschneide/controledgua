import os
import subprocess

# Verifica e instala dependências
try:
    import flask
    import PyPDF2
except ImportError:
    print("Instalando dependências...")
    subprocess.run(["pip", "install", "flask", "pypdf2"], check=True)
    import flask
    import PyPDF2

from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analisador de Currículos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #0056b3;
        }
        input, button {
            margin-top: 10px;
            padding: 10px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Analisador de Currículos</h1>
    <p>Envie seu currículo em PDF para análise:</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".pdf" required>
        <button type="submit">Analisar</button>
    </form>
    <p id="resultado"></p>
</body>
</html>
"""


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
        return f"<h1>Resultado da Análise</h1><p>{texto[:500]}...</p>"

    return "Formato inválido, envie um PDF", 400


def extrair_texto_pdf(filepath):
    with open(filepath, "rb") as f:
        leitor = PyPDF2.PdfReader(f)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() + "\n"
        return texto.strip()


if __name__ == "__main__":
    app.run(debug=True)
