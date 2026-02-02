import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

class GradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Corrige.AI - Agente de Correção para Professores v2.0")
        self.root.geometry("600x600")

        # Layout
        tk.Label(root, text="Diretório das Provas:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        frame_dir = tk.Frame(root)
        frame_dir.pack(fill=tk.X, padx=20, pady=5)
        self.entry_dir = tk.Entry(frame_dir)
        self.entry_dir.pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(frame_dir, text="Selecionar", command=self.browse_dir).pack(side=tk.RIGHT, padx=5)

        tk.Label(root, text="O que deve ser corrigido e gerado?", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.entry_prompt = tk.Text(root, height=8)
        self.entry_prompt.pack(padx=20, pady=5, fill=tk.X)
        self.entry_prompt.insert(tk.END, "Analise o conteúdo, verifique a lógica e dê uma nota de 0 a 5 com um breve feedback.")

        self.btn_run = tk.Button(root, text="Iniciar Correção", command=self.run_agent, bg="#28a745", fg="white", font=('Arial', 11, 'bold'), height=2)
        self.btn_run.pack(pady=15, padx=20, fill=tk.X)

        tk.Label(root, text="Log de Execução:", font=('Arial', 9)).pack()
        self.log_area = scrolledtext.ScrolledText(root, height=12, font=('Consolas', 9), bg="#f8f9fa")
        self.log_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Pronto")
        self.lbl_status = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, directory)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def run_agent(self):
        input_dir = self.entry_dir.get().strip()
        prompt = self.entry_prompt.get("1.0", tk.END).strip()
        
        if not input_dir or not prompt:
            messagebox.showwarning("Aviso", "Por favor, selecione o diretório e insira o prompt.")
            return

        if not os.path.exists(input_dir):
            messagebox.showerror("Erro", "O diretório selecionado não existe.")
            return

        self.btn_run.config(state=tk.DISABLED)
        self.status_var.set("Processando... Por favor, aguarde.")
        self.log_area.delete("1.0", tk.END)
        self.log("--- Iniciando Processo ---")

        def task():
            try:
                # Comando para rodar o agent.py
                # Usamos sys.executable para garantir que use o mesmo python da GUI
                process = subprocess.Popen(
                    [sys.executable, "agent.py", input_dir, prompt],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )

                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                if process.returncode == 0:
                    self.log("\n--- Finalizado com Sucesso! ---")
                    messagebox.showinfo("Sucesso", "Correção concluída!\nAs correções estão na pasta 'output_correcoes'.")
                else:
                    self.log(f"\n--- Erro na execução (Código {process.returncode}) ---")
                    messagebox.showerror("Erro", "O script encontrou um problema. Verifique o log de execução.")

            except Exception as e:
                self.log(f"Erro ao iniciar script: {str(e)}")
                messagebox.showerror("Erro Fatal", f"Não foi possível iniciar o agente: {str(e)}")
            finally:
                self.btn_run.config(state=tk.NORMAL)
                self.status_var.set("Pronto")

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GradingGUI(root)
    root.mainloop()
