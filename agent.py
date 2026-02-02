import os
import zipfile
import json
import nbformat
import PyPDF2
import sys
import traceback
from utils import call_llm as oci_call_llm

class GradingAgent:
    def __init__(self):
        # Limite de caracteres para o contexto da OCI (ajustado conforme necessário)
        self.max_chars = 30000 

    def extract_text_from_pdf(self, file_path):
        try:
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            return f"[Erro ao ler PDF {file_path}: {str(e)}]"

    def extract_text_from_ipynb(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            text = ""
            for cell in nb.cells:
                if cell.cell_type in ['markdown', 'code']:
                    text += f"--- {cell.cell_type.upper()} CELL ---\n{cell.source}\n"
            return text
        except Exception as e:
            return f"[Erro ao ler IPYNB {file_path}: {str(e)}]"

    def extract_text_from_sql(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f"[Erro ao ler arquivo de texto {file_path}: {str(e)}]"

    def process_zip(self, zip_path, extract_to):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except Exception as e:
            print(f"Erro ao descompactar {zip_path}: {e}")
            return False

    def get_file_content(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        content = ""
        if ext == '.pdf':
            content = self.extract_text_from_pdf(file_path)
        elif ext == '.ipynb':
            content = self.extract_text_from_ipynb(file_path)
        elif ext in ['.sql', '.txt', '.py', '.c', '.cpp', '.java', '.md', '.json']:
            content = self.extract_text_from_sql(file_path)
        else:
            return None
        
        if len(content) > self.max_chars:
            print(f"Aviso: Arquivo {os.path.basename(file_path)} muito grande. Truncando para {self.max_chars} caracteres.")
            content = content[:self.max_chars] + "\n\n[CONTEÚDO TRUNCADO POR SER MUITO LONGO]"
        return content

    def call_grading_llm(self, content, instruction):
        full_prompt = f"Instrução de Correção: {instruction}\n\nConteúdo do Trabalho:\n{content}\n\nPor favor, forneça a correção e o feedback conforme solicitado."
        
        try:
            # Chama a função do utils.py que integra com a OCI
            response = oci_call_llm(full_prompt)
            return response if response else "Erro: Resposta vazia da LLM na OCI."
        except Exception as e:
            return f"Erro na chamada da LLM (OCI): {str(e)}"

    def save_output(self, original_name, feedback, output_dir):
        clean_name = "".join([c for c in original_name if c.isalnum() or c in (' ', '.', '_')]).rstrip()
        output_name = f"feedback_{os.path.splitext(clean_name)[0]}.txt"
        path = os.path.join(output_dir, output_name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(feedback)

    def run_grading(self, input_dir, prompt_instruction, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"Iniciando processamento em: {input_dir} via OCI LLM")
        
        for root, dirs, files in os.walk(input_dir):
            if "output_correcoes" in root or "temp_" in root:
                continue
                
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                if file_name.lower().endswith('.zip'):
                    temp_extract = os.path.join(output_dir, f"temp_{file_name}")
                    if self.process_zip(file_path, temp_extract):
                        self.run_grading(temp_extract, prompt_instruction, output_dir)
                    continue

                content = self.get_file_content(file_path)
                if content:
                    print(f"Corrigindo via OCI: {file_name}...")
                    feedback = self.call_grading_llm(content, prompt_instruction)
                    self.save_output(file_name, feedback, output_dir)
                else:
                    print(f"Ignorado: {file_name}")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Uso: python agent.py <diretorio_entrada> <prompt_correcao>")
            sys.exit(1)
        
        input_path = sys.argv[1]
        instruction = sys.argv[2]
        out_path = os.path.join(os.getcwd(), "output_correcoes")
        
        agent = GradingAgent()
        agent.run_grading(input_path, instruction, out_path)
        print(f"\nConcluído! Resultados em: {out_path}")
        
    except Exception as e:
        print(f"\nERRO NO SCRIPT:\n{str(e)}")
        traceback.print_exc()
        sys.exit(1)
