# Sistema Especialista Fuzzy para Apoio ao Diagnóstico Inicial de Diabetes e Hipertensão

![Status do Projeto](https://img.shields.io/badge/status-ativo-brightgreen)
![Licença](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Visão Geral do Projeto

Este projeto apresenta um **Sistema Especialista Fuzzy** desenvolvido para auxiliar no diagnóstico inicial de diabetes mellitus tipo 2 e hipertensão arterial. Utilizando a lógica fuzzy, o sistema processa variáveis clínicas simples (idade, Índice de Massa Corporal - IMC, glicemia e pressão arterial sistólica) para fornecer uma classificação de risco interpretável (baixo, médio e alto) para cada condição. O objetivo é oferecer uma ferramenta de apoio à triagem clínica, especialmente útil em ambientes com recursos limitados, onde o acesso a médicos especialistas pode ser restrito.

O sistema foi implementado em Python, utilizando a biblioteca `scikit-fuzzy` para o motor de inferência Mamdani e `Streamlit` para a construção de uma interface web interativa e acessível.

## ✨ Recursos e Tecnologias

* **Python**: Linguagem de programação principal.
* **Scikit-fuzzy**: Biblioteca para implementação de sistemas de lógica fuzzy.
* **Streamlit**: Framework para criação de aplicações web interativas com Python.
* **NumPy**: Para operações numéricas eficientes.
* **Matplotlib**: Para a visualização das funções de pertinência e ativações fuzzy.

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local:

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```
    (Lembre-se de substituir `seu-usuario/seu-repositorio` pelo caminho real do seu repositório no GitHub.)

2.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação Streamlit:**

    ```bash
    streamlit run main.py
    ```

    Isso abrirá a aplicação em seu navegador web padrão (geralmente em `http://localhost:8501`).

## 🖥️ Como Usar

A interface do Streamlit permite que você insira os valores das variáveis clínicas:

* **Idade** (anos)
* **IMC** (kg/m²)
* **Glicemia** (mg/dL)
* **Pressão Sistólica** (mmHg)

Após inserir os dados, clique no botão "Calcular Riscos" para obter a avaliação de risco de diabetes e hipertensão, apresentada em percentuais e classificações linguísticas (Baixo, Médio, Alto). O sistema também exibe gráficos das funções de pertinência e o processo de fuzzificação, que ajudam a entender como o sistema chegou aos resultados.

## 📊 Resultados e Exemplos

O sistema foi testado com diferentes perfis de usuários para demonstrar seu comportamento:

### Exemplo 1 — Baixo Risco

* **Dados de Entrada:** Idade: 21 anos; IMC: 26; Glicemia: 100 mg/dL; PAS: 90 mmHg
* **Resultados:** Risco de Diabetes: 20.0%; Risco de Hipertensão: 20.0%

[Image of Interface do sistema fuzzy - Baixo Risco]

### Exemplo 2 — Médio Risco

* **Dados de Entrada:** Idade: 62 anos; IMC: 32.1; Glicemia: 50 mg/dL; PAS: 114 mmHg
* **Resultados:** Risco de Diabetes: 56.6%; Risco de Hipertensão: 54.1%

[Image of Interface do sistema fuzzy - Médio Risco]

### Exemplo 3 — Alto Risco

* **Dados de Entrada:** Idade: 70 anos; IMC: 34.0; Glicemia: 160 mg/dL; PAS: 175 mmHg
* **Resultados:** Risco de Diabetes: 65.0%; Risco de Hipertensão: 65.8%

[Image of Interface do sistema fuzzy - Alto Risco]

### Processo de Fuzzificação

Este gráfico mostra como os valores de entrada são convertidos em graus de pertinência fuzzy:

[Image of Processo de Fuzzificação]

## 📁 Estrutura do Projeto

* `main.py`: O código-fonte principal da aplicação Streamlit, contendo a lógica fuzzy e a interface.
* `dataset.csv`: (Opcional) Arquivo de dados utilizado para carregar exemplos ou definir o universo de discurso das variáveis fuzzy.
* `requirements.txt`: Lista de todas as dependências do Python necessárias para o projeto.
* `images/`: Pasta contendo as imagens utilizadas no README e possivelmente no documento LaTeX.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você quiser melhorar este projeto, por favor:

1.  Faça um fork do repositório.
2.  Crie uma branch para sua feature (`git checkout -b feature/minha-nova-feature`).
3.  Faça suas alterações e commit (`git commit -m 'feat: adiciona nova funcionalidade'`).
4.  Envie para o branch original (`git push origin feature/minha-nova-feature`).
5.  Abra um Pull Request.

## 👨‍💻 Autores

* **Diogo Buzatto** - `diogobuzatto@alunos.fho.edu.br`
* **Lucas Ferreira Silva** - `lucas.silva2958@alunos.fho.edu.br`
