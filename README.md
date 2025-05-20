# 🧠 Sistema Fuzzy de Avaliação de Riscos de Saúde

Este projeto implementa um sistema de inferência fuzzy que avalia o **risco de diabetes** e **risco de hipertensão** com base em quatro variáveis de entrada: idade, IMC, glicemia e pressão arterial sistólica (PAS). A aplicação possui uma interface gráfica amigável feita com `Tkinter` e suporte a modo claro e escuro.

## 📌 Funcionalidades

- Entrada de dados:
  - Idade (anos)
  - IMC (Índice de Massa Corporal)
  - Glicemia (mg/dL)
  - PAS (Pressão Arterial Sistólica)
- Cálculo do risco baseado em lógica fuzzy com `scikit-fuzzy`
- Interface com `Tkinter`, incluindo:
  - Validações de entrada
  - Feedback de erro
  - Alternância entre modo claro e escuro

## 🛠️ Tecnologias utilizadas

- Python 3.x
- [NumPy](https://numpy.org/)
- [scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy)
- Tkinter (interface nativa do Python)

## 💡 Lógica Fuzzy

### 🔹 Variáveis de Entrada

| Variável   | Conjuntos Fuzzy                  |
|------------|----------------------------------|
| **Idade**  | Jovem, Meia-idade, Idoso         |
| **IMC**    | Baixo, Normal, Alto              |
| **Glicemia** | Normal, Alterada, Alta         |
| **PAS**    | Normal, Pré-hipertensão, Hipertensão |

### 🔸 Variáveis de Saída

- **Risco de Diabetes:** Baixo, Médio, Alto
- **Risco de Hipertensão:** Baixo, Médio, Alto

### 🔁 Regras de Inferência

Exemplos:
- Se **glicemia é alta** OU **IMC é alto** OU **idade é idoso**, então **risco de diabetes é alto**.
- Se **PAS é hipertensão** OU **idade é idoso** OU **IMC é alto**, então **risco de hipertensão é alto**.
- Veja o código para a lista completa de regras.

## ▶️ Como executar

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/sistema-fuzzy-saude.git
cd sistema-fuzzy-saude
