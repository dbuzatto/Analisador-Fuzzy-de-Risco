import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

idade = ctrl.Antecedent(np.arange(0, 101, 1), 'idade')
imc = ctrl.Antecedent(np.arange(10, 50, 0.1), 'imc')
glicemia = ctrl.Antecedent(np.arange(50, 300, 1), 'glicemia')
pas = ctrl.Antecedent(np.arange(80, 200, 1), 'pas')

risco_diabetes = ctrl.Consequent(np.arange(0, 101, 1), 'risco_diabetes')
risco_hipertensao = ctrl.Consequent(np.arange(0, 101, 1), 'risco_hipertensao')

idade['jovem'] = fuzz.trimf(idade.universe, [0, 20, 40])
idade['meia_idade'] = fuzz.trimf(idade.universe, [30, 50, 70])
idade['idoso'] = fuzz.trimf(idade.universe, [60, 80, 100])

imc['baixo'] = fuzz.trimf(imc.universe, [10, 15, 20])
imc['normal'] = fuzz.trimf(imc.universe, [18.5, 22, 25])
imc['alto'] = fuzz.trimf(imc.universe, [24, 30, 40])

glicemia['normal'] = fuzz.trimf(glicemia.universe, [50, 80, 100])
glicemia['alterada'] = fuzz.trimf(glicemia.universe, [90, 120, 150])
glicemia['alta'] = fuzz.trimf(glicemia.universe, [140, 200, 300])

pas['normal'] = fuzz.trimf(pas.universe, [80, 110, 120])
pas['pre_hipertensao'] = fuzz.trimf(pas.universe, [110, 130, 140])
pas['hipertensao'] = fuzz.trimf(pas.universe, [135, 160, 200])

risco_diabetes['baixo'] = fuzz.trimf(risco_diabetes.universe, [0, 20, 40])
risco_diabetes['medio'] = fuzz.trimf(risco_diabetes.universe, [30, 50, 70])
risco_diabetes['alto'] = fuzz.trimf(risco_diabetes.universe, [60, 80, 100])

risco_hipertensao['baixo'] = fuzz.trimf(risco_hipertensao.universe, [0, 20, 40])
risco_hipertensao['medio'] = fuzz.trimf(risco_hipertensao.universe, [30, 50, 70])
risco_hipertensao['alto'] = fuzz.trimf(risco_hipertensao.universe, [60, 80, 100])

rules = [
    ctrl.Rule(glicemia['alta'] | imc['alto'] | idade['idoso'], risco_diabetes['alto']),
    ctrl.Rule(glicemia['alterada'] & imc['normal'], risco_diabetes['medio']),
    ctrl.Rule(glicemia['normal'] & idade['jovem'], risco_diabetes['baixo']),
    ctrl.Rule(pas['hipertensao'] | idade['idoso'] | imc['alto'], risco_hipertensao['alto']),
    ctrl.Rule(pas['pre_hipertensao'] & idade['meia_idade'], risco_hipertensao['medio']),
    ctrl.Rule(pas['normal'] & idade['jovem'], risco_hipertensao['baixo']),
]

sistema_ctrl = ctrl.ControlSystem(rules)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Fuzzy - Risco de Saúde")
        self.is_dark = False
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill='both', expand=True)
        self.toggle_icon = tk.Button(self.main_frame, command=self.toggle_theme)
        self.toggle_icon.pack(anchor='ne')
        self.set_icon()

        # Validações para os campos
        vcmd_idade = (root.register(self.validate_idade), '%P')
        vcmd_float = (root.register(self.validate_float), '%P')

        self.inputs = {}
        campos = [
            ("Idade (anos)", "Informe sua idade em anos completos.", vcmd_idade),
            ("IMC", "Índice de Massa Corporal. Use peso (kg) / altura (m²).", vcmd_float),
            ("Glicemia (mg/dL)", "Verifique esse valor em um exame de sangue em jejum.", vcmd_float),
            ("Pressão Arterial Sistólica (PAS)", "Use o valor maior de sua pressão, ex: 120 se for 120/80.", vcmd_float),
        ]

        for label_text, descricao, vcmd in campos:
            label = ttk.Label(self.main_frame, text=label_text)
            label.pack(anchor='w', pady=(10, 0))
            entry = tk.Entry(self.main_frame, validate='key', validatecommand=vcmd)
            entry.pack(fill='x')
            descricao_label = ttk.Label(self.main_frame, text=descricao, style='Desc.TLabel', wraplength=400)
            descricao_label.pack(anchor='w')
            self.inputs[label_text] = entry

        self.resultado = ttk.Label(self.main_frame, text="", font=("Arial", 12, "bold"))
        self.resultado.pack(pady=20)
        self.botao = ttk.Button(self.main_frame, text="Calcular Riscos", command=self.calcular)
        self.botao.pack(pady=10)
        self.apply_theme()

    def set_icon(self):
        icon = "☾" if not self.is_dark else "☀"
        self.toggle_icon.config(text=icon, font=("Arial", 12))

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        self.set_icon()

    def apply_theme(self):
        style = ttk.Style()
        if self.is_dark:
            self.root.configure(bg='#2e2e2e')
            style.configure('.', background='#2e2e2e', foreground='white')
            style.configure('Desc.TLabel', foreground='#bbbbbb', background='#2e2e2e', font=("Arial", 8))
            for entry in self.inputs.values():
                entry.configure(bg='white', fg='black', insertbackground='black')
            self.botao.configure(style="Custom.TButton")
            style.configure("Custom.TButton", background='white', foreground='black')
        else:
            self.root.configure(bg='white')
            style.configure('.', background='white', foreground='black')
            style.configure('Desc.TLabel', foreground='gray', background='white', font=("Arial", 8))
            for entry in self.inputs.values():
                entry.configure(bg='white', fg='black', insertbackground='black')
            self.botao.configure(style="Custom.TButton")
            style.configure("Custom.TButton", background='white', foreground='black')

    def validate_idade(self, new_value):
        if new_value == "":
            return True
        if new_value.isdigit():
            valor = int(new_value)
            return 0 < valor <= 100
        return False

    def validate_float(self, new_value):
        if new_value == "":
            return True
        try:
            # Permite um único ponto decimal
            if new_value.count('.') > 1:
                return False
            float(new_value)
            return True
        except ValueError:
            return False

    def calcular(self):
        try:
            idade_text = self.inputs["Idade (anos)"].get()
            imc_text = self.inputs["IMC"].get()
            glicemia_text = self.inputs["Glicemia (mg/dL)"].get()
            pas_text = self.inputs["Pressão Arterial Sistólica (PAS)"].get()

            if not idade_text:
                raise ValueError("Idade é obrigatória.")
            idade_val = int(idade_text)
            if idade_val <= 0 or idade_val > 100:
                raise ValueError("Idade deve ser um número entre 1 e 100.")

            if not imc_text:
                raise ValueError("IMC é obrigatório.")
            imc_val = float(imc_text)
            if not (10 <= imc_val <= 50):
                raise ValueError("IMC deve estar entre 10 e 50.")

            if not glicemia_text:
                raise ValueError("Glicemia é obrigatória.")
            glicemia_val = float(glicemia_text)
            if not (50 <= glicemia_val <= 300):
                raise ValueError("Glicemia deve estar entre 50 e 300 mg/dL.")

            if not pas_text:
                raise ValueError("PAS é obrigatório.")
            pas_val = float(pas_text)
            if not (80 <= pas_val <= 200):
                raise ValueError("PAS deve estar entre 80 e 200.")

            sistema.input['idade'] = idade_val
            sistema.input['imc'] = imc_val
            sistema.input['glicemia'] = glicemia_val
            sistema.input['pas'] = pas_val
            sistema.compute()

            risco_diab = sistema.output['risco_diabetes']
            risco_hiper = sistema.output['risco_hipertensao']

            self.resultado.config(
                text=f"Risco de Diabetes: {risco_diab:.1f}%\nRisco de Hipertensão: {risco_hiper:.1f}%"
            )
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
