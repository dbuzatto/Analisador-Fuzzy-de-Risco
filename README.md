# 🏥 Sistema Fuzzy para Diagnóstico de Diabetes e Hipertensão

Um sistema especialista baseado em lógica fuzzy para avaliar riscos de diabetes e hipertensão a partir de parâmetros clínicos básicos.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Dataset](#-dataset)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Lógica Fuzzy](#-lógica-fuzzy)
- [Tecnologias](#-tecnologias)

## 🎯 Visão Geral

Este sistema utiliza **lógica fuzzy** para simular o raciocínio médico na avaliação de riscos de saúde. Diferente de sistemas binários (sim/não), a lógica fuzzy permite trabalhar com **incertezas** e **graduações** típicas do diagnóstico médico.

### 🔬 Como Funciona

1. **Entrada**: Idade, IMC, Glicemia e Pressão Arterial
2. **Processamento**: Inferência fuzzy com regras médicas
3. **Saída**: Percentual de risco + categoria semântica (baixo/médio/alto)

## ✨ Funcionalidades

- 📊 **Avaliação de Risco Dupla**: Diabetes e Hipertensão simultaneamente
- 🎯 **Calibração Automática**: Adapta-se ao dataset fornecido
- 🌡️ **Lógica Fuzzy**: Trabalha com incertezas e valores intermediários
- 🎨 **Interface Intuitiva**: Streamlit com emojis e feedback visual
- 📈 **Resultados Detalhados**: Percentual + categoria semântica
- 🔄 **Fallback Inteligente**: Funciona mesmo sem dataset

## 📊 Dataset

### 🎯 **Papel Fundamental do Dataset**

O dataset **NÃO é uma limitação**, mas sim o **calibrador** do sistema:

```csv
idade,imc,glicemia,pas
22,20.5,75,105    # Jovem saudável
45,32.0,125,145   # Adulto com fatores de risco
70,34.0,160,175   # Idoso com risco elevado
```

### 🔧 **Como o Dataset é Usado**

#### 1. **Calibração dos Universos Fuzzy**

```python
# Dataset define os limites dos universos
dados_dataset = np.loadtxt('dataset.csv', delimiter=',', skiprows=1)
valores_idade, valores_imc, valores_glicemia, valores_pressao = dados_dataset.T

# Calcula estatísticas para posicionamento das funções
estatisticas = {
    'min':  np.min(valores),     # Limite inferior
    'max':  np.max(valores),     # Limite superior
    'mean': np.mean(valores),    # Centro das funções
    'std':  np.std(valores)      # Dispersão
}
```

#### 2. **Posicionamento das Funções de Pertinência**

```python
# Usa estatísticas para criar funções trapezoidais otimizadas
parametros_baixo = [min, min, mean, mean + std]
parametros_medio = [mean - std, mean, mean + std, mean + 2*std]
parametros_alto = [mean, mean + std, max, max]
```

### 📈 **Estrutura do Dataset Atual**

O dataset fornecido contém **109 registros** cobrindo:

#### **👶 Jovens (18-30 anos)**

```csv
18,19.2,72,95     # Atleta jovem
22,28.6,96,110    # Jovem normal
28,18.5,68,90     # Jovem muito ativo
```

#### **👥 Adultos (30-50 anos)**

```csv
32,28.1,98,109    # Adulto saudável
40,29.0,110,135   # Adulto normal
45,32.0,125,145   # Pré-diabetes
```

#### **👴 Idosos (50-85 anos)**

```csv
55,42.0,195,175   # Alto risco diabetes
70,34.0,160,175   # Risco moderado
85,28.5,155,170   # Idoso controlado
```

#### **⚠️ Casos Especiais**

```csv
33,48.0,225,192   # Obesidade + diabetes severa
24,16.8,65,85     # Subpeso + hipoglicemia
80,27.4,84,80     # Idoso com pressão baixa
```

### 🎯 **Vantagens do Dataset Diversificado**

#### ✅ **Com Dataset Abrangente:**

- **Precisão**: Funções calibradas para população real
- **Adaptabilidade**: Reconhece padrões específicos
- **Robustez**: Lida bem com casos extremos
- **Confiabilidade**: Diagnósticos mais assertivos

#### 🔄 **Sem Dataset (Fallback):**

```python
# Dados genéricos para demonstração
valores_idade = np.array([25, 30, 45, 60, 70])
valores_imc = np.array([18.5, 25, 30, 35, 40])
valores_glicemia = np.array([80, 100, 120, 140, 180])
valores_pressao = np.array([90, 120, 140, 160, 180])
```

### 🔍 **Dataset vs Entrada do Usuário**

| Aspecto           | Dataset                | Entrada do Usuário      |
| ----------------- | ---------------------- | ----------------------- |
| **Função**        | Calibração do sistema  | Dados para diagnóstico  |
| **Momento**       | Inicialização          | Runtime                 |
| **Limitações**    | Define otimização      | Limitada pela interface |
| **Flexibilidade** | Fixa após carregamento | Qualquer valor válido   |

**Exemplo:** Dataset com idades 18-85, mas usuário pode inserir qualquer idade entre 1-120 anos!

## 🚀 Instalação

### Pré-requisitos

```bash
python >= 3.8
pip >= 21.0
```

### Dependências

```bash
pip install numpy
pip install scikit-fuzzy
pip install streamlit
```

### Executar Aplicação

```bash
streamlit run main.py
```

## 🖥️ Como Usar

### 1. **Iniciar o Sistema**

```bash
streamlit run main.py
```

### 2. **Inserir Dados Clínicos**

- 👤 **Idade**: 1-120 anos
- ⚖️ **IMC**: 10.0-50.0 kg/m²
- 🩸 **Glicemia**: 50-300 mg/dL
- 💓 **Pressão Sistólica**: 70-220 mmHg

### 3. **Interpretar Resultados**

```
🩺 Risco de Diabetes: 67.3%
🔴 Alto

❤️ Risco de Hipertensão: 23.1%
🟢 Baixo
```

#### 🎨 **Códigos de Cores**

- 🟢 **Verde**: Risco Baixo (0-40%)
- 🟡 **Amarelo**: Risco Médio (30-70%)
- 🔴 **Vermelho**: Risco Alto (60-100%)

## 🧠 Arquitetura do Sistema

### 📊 **Fluxo de Dados**

```mermaid
Dataset CSV → Estatísticas → Universos Fuzzy → Funções de Pertinência
                                                        ↓
Entrada Usuário → Fuzzificação → Regras → Inferência → Defuzzificação → Resultado
```

### 🔧 **Componentes Principais**

#### 1. **Processamento de Dados**

```python
carregar_dados_clinicos()           # Carrega dataset ou fallback
calcular_estatisticas_parametros()  # Min, max, média, desvio
```

#### 2. **Sistema Fuzzy**

```python
criar_variaveis_entrada()           # Antecedentes (idade, imc, etc.)
criar_variaveis_saida()            # Consequentes (riscos)
configurar_funcoes_pertinencia()   # Baixo, médio, alto
criar_regras_inferencia()          # Lógica médica
```

#### 3. **Interface**

```python
criar_interface_usuario()          # Streamlit UI
processar_avaliacao_risco()       # Engine principal
exibir_resultados()               # Resultados formatados
```

## 🎯 Lógica Fuzzy

### 📏 **Funções de Pertinência**

#### **Variáveis de Entrada (Trapezoidais)**

```python
# Baseadas nas estatísticas do dataset
baixo = [min, min, mean, mean + std]
medio = [mean - std, mean, mean + std, mean + 2*std]
alto = [mean, mean + std, max, max]
```

#### **Variáveis de Saída (Triangulares)**

```python
risco_baixo = [0, 20, 40]      # 0-40%
risco_medio = [30, 50, 70]     # 30-70%
risco_alto = [60, 80, 100]     # 60-100%
```

### 🧩 **Regras de Inferência**

#### **Para Diabetes:**

```python
SE (glicemia ALTA OU imc ALTO OU idade ALTA) ENTÃO risco_diabetes ALTO
SE (glicemia MÉDIA E imc MÉDIO) ENTÃO risco_diabetes MÉDIO
SE (glicemia BAIXA E idade BAIXA) ENTÃO risco_diabetes BAIXO
```

#### **Para Hipertensão:**

```python
SE (pressão ALTA OU idade ALTA OU imc ALTO) ENTÃO risco_hipertensao ALTO
SE (pressão MÉDIA E idade MÉDIA) ENTÃO risco_hipertensao MÉDIO
SE (pressão BAIXA E idade BAIXA) ENTÃO risco_hipertensao BAIXO
```

### ⚙️ **Processo de Inferência**

1. **Fuzzificação**: Converte valores crisp em graus de pertinência
2. **Avaliação de Regras**: Aplica operadores fuzzy (E, OU)
3. **Agregação**: Combina resultados de múltiplas regras
4. **Defuzzificação**: Converte resultado fuzzy em valor crisp

## 🛠️ Tecnologias

| Tecnologia       | Versão | Função              |
| ---------------- | ------ | ------------------- |
| **Python**       | 3.8+   | Linguagem principal |
| **NumPy**        | Latest | Computação numérica |
| **scikit-fuzzy** | Latest | Lógica fuzzy        |
| **Streamlit**    | Latest | Interface web       |

## 📝 Estrutura de Arquivos

```
sistema-fuzzy-diagnostico/
├── main.py              # Aplicação principal
├── dataset.csv          # Dados para calibração (109 registros)
├── README.md           # Este arquivo
└── requirements.txt    # Dependências
```

## 🔬 Validação Médica

### ⚠️ **Disclaimer Importante**

Este sistema é para **fins educacionais e demonstrativos**. Não substitui:

- Consulta médica profissional
- Exames laboratoriais completos
- Diagnóstico clínico especializado

### 🎯 **Uso Recomendado**

- Triagem inicial
- Educação em saúde
- Demonstração de IA em medicina
- Pesquisa acadêmica

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ para educação em IA médica**
