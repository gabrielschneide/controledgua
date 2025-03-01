import requests
import PyPDF2
from fpdf import FPDF
import re
import os

# 🚀 Instalar automaticamente as bibliotecas (caso necessário)
try:
    import PyPDF2
    import fpdf
    import requests
except ModuleNotFoundError:
    os.system("pip install PyPDF2 fpdf requests")

# 🚀 Função para analisar currículo via API Gemini
def analyze_resume_with_gemini(resume_text, job_description):
    api_key = "SUA_CHAVE_API_AQUI"  # Substitua pela sua chave válida
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    data = {
        "contents": [{
            "parts": [
                {"text": f"Analise a compatibilidade do seguinte currículo com a descrição da vaga.\n\nCurrículo:\n{resume_text}\n\nVaga:\n{job_description}\n\nRetorne um resumo da compatibilidade e uma nota de 0 a 100%."}
            ]
        }]
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()

        if "candidates" in result and len(result["candidates"]) > 0:
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            match = re.search(r"(\d{1,3})%", text_response)
            percentage = match.group(1) if match else "N/A"
            return text_response, percentage
        else:
            return "A API não retornou uma resposta válida.", "N/A"
    else:
        return f"Erro na API: {response.status_code} - {response.text}", "N/A"

# 🚀 Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

# 🚀 Função para limpar texto e evitar erro de codificação no PDF
def clean_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# 🚀 Função para gerar um PDF formatado
def generate_pdf_report(report_text, percentage, job_description):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório de Análise de Currículo", ln=True, align="C")
    
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, f"Compatibilidade: {percentage}%", ln=True, align="C")
    
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Descrição da Vaga:", ln=True)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, clean_text(job_description))

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Análise do Currículo:", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, clean_text(report_text))

    pdf_filename = "Relatorio_Analise_Curriculo.pdf"
    pdf.output(pdf_filename, "F")

    print(f"\nRelatório gerado com sucesso! Salvo como {pdf_filename}.")

# 🚀 Fluxo principal
if __name__ == "__main__":
    pdf_path = input("Digite o caminho do PDF do currículo: ")

    if not os.path.exists(pdf_path):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
    else:
        resume_text = extract_text_from_pdf(pdf_path)
        job_description = input("Insira a descrição da vaga: ")

        result_text, compatibility_percentage = analyze_resume_with_gemini(resume_text, job_description)

        print("\nResultado da Análise do Currículo:\n")
        print(result_text)

        generate_pdf_report(result_text, compatibility_percentage, job_description)
