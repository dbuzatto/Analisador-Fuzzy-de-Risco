import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

idade = ctrl.Antecedent(np.arange(0, 101, 1), 'idade')
imc = ctrl.Antecedent(np.arange(10, 50, 1), 'imc')
glicemia = ctrl.Antecedent(np.arange(50, 201, 1), 'glicemia')
pas = ctrl.Antecedent(np.arange(80, 201, 1), 'pas')

risco_diabetes = ctrl.Consequent(np.arange(0, 101, 1), 'risco_diabetes')
risco_hipertensao = ctrl.Consequent(np.arange(0, 101, 1), 'risco_hipertensao')

idade['jovem'] = fuzz.trimf(idade.universe, [0, 20, 40])
idade['meia_idade'] = fuzz.trimf(idade.universe, [30, 50, 70])
idade['idoso'] = fuzz.trimf(idade.universe, [60, 80, 100])

imc['baixo'] = fuzz.trimf(imc.universe, [10, 15, 20])
imc['normal'] = fuzz.trimf(imc.universe, [18.5, 22, 25])
imc['alto'] = fuzz.trimf(imc.universe, [24, 30, 40])
imc['obeso'] = fuzz.trimf(imc.universe, [35, 45, 50])

glicemia['baixa'] = fuzz.trimf(glicemia.universe, [50, 60, 90])
glicemia['normal'] = fuzz.trimf(glicemia.universe, [85, 100, 115])
glicemia['alta'] = fuzz.trimf(glicemia.universe, [110, 150, 200])

pas['normal'] = fuzz.trimf(pas.universe, [80, 110, 120])
pas['pre_hipertensao'] = fuzz.trimf(pas.universe, [110, 130, 140])
pas['hipertensao'] = fuzz.trimf(pas.universe, [135, 160, 200])

risco_diabetes['baixo'] = fuzz.trimf(risco_diabetes.universe, [0, 20, 40])
risco_diabetes['medio'] = fuzz.trimf(risco_diabetes.universe, [30, 50, 70])
risco_diabetes['alto'] = fuzz.trimf(risco_diabetes.universe, [60, 80, 100])

risco_hipertensao['baixo'] = fuzz.trimf(risco_hipertensao.universe, [0, 20, 40])
risco_hipertensao['medio'] = fuzz.trimf(risco_hipertensao.universe, [30, 50, 70])
risco_hipertensao['alto'] = fuzz.trimf(risco_hipertensao.universe, [60, 80, 100])

regras = [
    ctrl.Rule(glicemia['alta'] | imc['obeso'] | idade['idoso'], risco_diabetes['alto']),
    ctrl.Rule(glicemia['normal'] & imc['normal'] & idade['meia_idade'], risco_diabetes['medio']),
    ctrl.Rule(glicemia['baixa'] & imc['baixo'] & idade['jovem'], risco_diabetes['baixo']),
    ctrl.Rule(glicemia['normal'] & idade['jovem'], risco_diabetes['baixo']),
    ctrl.Rule(imc['normal'] & glicemia['baixa'], risco_diabetes['baixo']),
    ctrl.Rule(glicemia['normal'], risco_diabetes['medio']),
    ctrl.Rule(pas['hipertensao'] | imc['obeso'] | idade['idoso'], risco_hipertensao['alto']),
    ctrl.Rule(pas['pre_hipertensao'] & idade['meia_idade'], risco_hipertensao['medio']),
    ctrl.Rule(pas['normal'] & idade['jovem'], risco_hipertensao['baixo']),
    ctrl.Rule(pas['pre_hipertensao'] & imc['normal'], risco_hipertensao['medio']),
    ctrl.Rule(pas['normal'], risco_hipertensao['baixo']),
]

sistema_ctrl = ctrl.ControlSystem(regras)

def calcular_risco():
    try:
        idade_text = entry_idade.get().strip()
        imc_text = entry_imc.get().strip()
        glicemia_text = entry_glicemia.get().strip()
        pas_text = entry_pas.get().strip()

        if not all([idade_text, imc_text, glicemia_text, pas_text]):
            raise ValueError("Todos os campos são obrigatórios.")

        idade_val = float(idade_text)
        imc_val = float(imc_text)
        glicemia_val = float(glicemia_text)
        pas_val = float(pas_text)

        sim = ctrl.ControlSystemSimulation(sistema_ctrl)

        sim.input['idade'] = idade_val
        sim.input['imc'] = imc_val
        sim.input['glicemia'] = glicemia_val
        sim.input['pas'] = pas_val

        sim.compute()

        resultado_diabetes = sim.output['risco_diabetes']
        resultado_hipertensao = sim.output['risco_hipertensao']

        def classificar(valor):
            if valor >= 70:
                return "Alto"
            elif valor >= 40:
                return "Médio"
            else:
                return "Baixo"

        severidade_d = classificar(resultado_diabetes)
        severidade_h = classificar(resultado_hipertensao)

        severidade_label.config(
            text=f"Diabetes: {severidade_d} risco   |   Hipertensão: {severidade_h} risco"
        )

        resultado_label.config(
            text=f"Risco de Diabetes: {resultado_diabetes:.1f}%\n"
                 f"Risco de Hipertensão: {resultado_hipertensao:.1f}%"
        )

    except ValueError as ve:
        messagebox.showwarning("Campos obrigatórios", str(ve))
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao calcular:\n{e}")

def validar_idade(valor):
    if not valor:
        return True
    try:
        num = int(valor)
        return 0 < num <= 100
    except ValueError:
        return False

root = tk.Tk()
root.title("Analisador Fuzzy de Risco")
is_dark = False

def alternar_tema():
    global is_dark
    is_dark = not is_dark
    bg = '#2e2e2e' if is_dark else 'white'
    fg = 'white' if is_dark else 'black'
    entry_bg = '#444' if is_dark else 'white'

    root.configure(bg=bg)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=bg, fg=fg)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        elif isinstance(widget, tk.Button):
            widget.configure(bg=bg, fg=fg)
    tema_btn.config(text="☀" if is_dark else "☾", bg=bg, fg=fg)

for i in range(3):
    root.columnconfigure(i, weight=1)
for i in range(8):
    root.rowconfigure(i, weight=1)

tema_btn = tk.Button(root, text="☾", command=alternar_tema, relief="flat", bd=0)
tema_btn.grid(row=0, column=2, sticky='ne', padx=10, pady=10)

vcmd_idade = root.register(validar_idade)

tk.Label(root, text="Idade:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_idade = tk.Entry(root, validate='key', validatecommand=(vcmd_idade, '%P'))
entry_idade.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)

tk.Label(root, text="IMC:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_imc = tk.Entry(root)
entry_imc.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)

tk.Label(root, text="Glicemia (mg/dL):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_glicemia = tk.Entry(root)
entry_glicemia.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5)

tk.Label(root, text="Pressão Sistólica (mmHg):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_pas = tk.Entry(root)
entry_pas.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5)

tk.Button(root, text="Calcular Risco", command=calcular_risco).grid(row=5, column=0, columnspan=3, pady=10)

severidade_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
severidade_label.grid(row=6, column=0, columnspan=3, pady=(5, 0))

resultado_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
resultado_label.grid(row=7, column=0, columnspan=3, pady=(0, 10))

root.mainloop()
