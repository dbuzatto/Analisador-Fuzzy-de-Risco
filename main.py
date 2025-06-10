import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st
import matplotlib.pyplot as plt 
import pandas as pd 

#todo: adicionar grafico fuzzy e tabela verdade para cada variavel de entrada e saida

st.set_page_config(
  page_title="Sistema Fuzzy para Diagnóstico de Deabetes e Hipertensão",
  page_icon="🏥",
  layout="centered"
)

try:
  dados_dataset = np.loadtxt('dataset.csv', delimiter=',', skiprows=1)
  valores_idade, valores_imc, valores_glicemia, valores_pressao = dados_dataset.T
except:
  st.warning("⚠️ Arquivo dataset.csv não encontrado. Usando dados de exemplo.")
  # Adicionar dados de exemplo
  valores_idade = np.array([25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
  valores_imc = np.array([18.5, 22.0, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5])
  valores_glicemia = np.array([80, 90, 100, 110, 120, 130, 140, 150, 160, 170])
  valores_pressao = np.array([110, 115, 120, 125, 130, 135, 140, 145, 150, 155])

# calcular estatísticas dos parâmetros
estatisticas_parametros = {}
for nome_parametro, valores_parametro in [
  ('idade', valores_idade),
  ('imc', valores_imc),
  ('glicemia', valores_glicemia),
  ('pressao', valores_pressao),
]:
  estatisticas_parametros[nome_parametro] = {
    'min': float(np.min(valores_parametro)), # valor mínimo
    'max': float(np.max(valores_parametro)), # valor máximo
    'mean': float(np.mean(valores_parametro)), # média
    'std': float(np.std(valores_parametro)), # desvio padrão
  }

# Definição das variáveis fuzzy - Antecedentes
antecedente_idade = ctrl.Antecedent(
  np.arange(estatisticas_parametros['idade']['min'], estatisticas_parametros['idade']['max'] + 1, 1),
  'idade'
)
antecedente_imc = ctrl.Antecedent(
  np.arange(estatisticas_parametros['imc']['min'], estatisticas_parametros['imc']['max'] + 0.1, 0.1),
  'imc'
)
antecedente_glicemia = ctrl.Antecedent(
  np.arange(estatisticas_parametros['glicemia']['min'], estatisticas_parametros['glicemia']['max'] + 1, 1),
  'glicemia'
)
antecedente_pressao = ctrl.Antecedent(
  np.arange(estatisticas_parametros['pressao']['min'], estatisticas_parametros['pressao']['max'] + 1, 1),
  'pas'
)

# Definição das variáveis fuzzy - Consequentes
consequente_risco_diabetes = ctrl.Consequent(np.arange(0, 101, 1), 'risco_diabetes')
consequente_risco_hipertensao = ctrl.Consequent(np.arange(0, 101, 1), 'risco_hipertensao')

# Criação das funções de pertinência trapezoidais para os antecedentes
def criar_funcoes_membership_trapezoidais(valor_minimo, valor_maximo, valor_medio, desvio_padrao):
  parametros_baixo = [valor_minimo, valor_minimo, valor_medio, valor_medio + desvio_padrao]
  parametros_medio = [valor_medio - desvio_padrao, valor_medio, valor_medio + desvio_padrao, valor_medio + 2 * desvio_padrao]
  parametros_alto = [valor_medio, valor_medio + desvio_padrao, valor_maximo, valor_maximo]
  return parametros_baixo, parametros_medio, parametros_alto

# Criação das funções de pertinência trapezoidais para os antecedentes
for variavel_entrada, chave_estatistica in [(antecedente_idade, 'idade'), (antecedente_imc, 'imc'), (antecedente_glicemia, 'glicemia'), (antecedente_pressao, 'pressao')]:
  stats_variavel = estatisticas_parametros[chave_estatistica]
  params_baixo, params_medio, params_alto = criar_funcoes_membership_trapezoidais(stats_variavel['min'], stats_variavel['max'], stats_variavel['mean'], stats_variavel['std'])
  variavel_entrada['baixo'] = fuzz.trapmf(variavel_entrada.universe, params_baixo)
  variavel_entrada['medio'] = fuzz.trapmf(variavel_entrada.universe, params_medio)
  variavel_entrada['alto'] = fuzz.trapmf(variavel_entrada.universe, params_alto)

# Criação das funções de pertinência trapezoidais para os consequentes
consequente_risco_diabetes['baixo'] = fuzz.trapmf(consequente_risco_diabetes.universe, [0, 15, 25, 40])
consequente_risco_diabetes['medio'] = fuzz.trapmf(consequente_risco_diabetes.universe, [30, 45, 55, 70])
consequente_risco_diabetes['alto'] = fuzz.trapmf(consequente_risco_diabetes.universe, [60, 75, 85, 100])
consequente_risco_hipertensao['baixo'] = fuzz.trapmf(consequente_risco_hipertensao.universe, [0, 15, 25, 40])
consequente_risco_hipertensao['medio'] = fuzz.trapmf(consequente_risco_hipertensao.universe, [30, 45, 55, 70])
consequente_risco_hipertensao['alto'] = fuzz.trapmf(consequente_risco_hipertensao.universe, [60, 75, 85, 100])

# Regras de inferência
inferencia = [
  ctrl.Rule(antecedente_glicemia['alto'] | antecedente_imc['alto'] | antecedente_idade['alto'], consequente_risco_diabetes['alto']),
  ctrl.Rule(antecedente_glicemia['medio'] & antecedente_imc['medio'], consequente_risco_diabetes['medio']),
  ctrl.Rule(antecedente_glicemia['baixo'] & antecedente_idade['baixo'], consequente_risco_diabetes['baixo']),
  ctrl.Rule(antecedente_pressao['alto'] | antecedente_idade['alto'] | antecedente_imc['alto'], consequente_risco_hipertensao['alto']),
  ctrl.Rule(antecedente_pressao['medio'] & antecedente_idade['medio'], consequente_risco_hipertensao['medio']),
  ctrl.Rule(antecedente_pressao['baixo'] & antecedente_idade['baixo'], consequente_risco_hipertensao['baixo']),
]

# Sistema de controle fuzzy
sistema_controle_fuzzy = ctrl.ControlSystem(inferencia)
simulacao_sistema = ctrl.ControlSystemSimulation(sistema_controle_fuzzy)

# Funções auxiliares
def obter_categoria_semantica(simulacao, variavel_consequente, nome_variavel):
  valor_crisp = simulacao.output[nome_variavel]
  universo_variavel = variavel_consequente.universe
  categorias_disponiveis = variavel_consequente.terms.keys()
  graus_pertinencia = {categoria: fuzz.interp_membership(universo_variavel, variavel_consequente[categoria].mf, valor_crisp) for categoria in categorias_disponiveis}
  return max(graus_pertinencia, key=graus_pertinencia.get)

def obter_emoji_nivel_risco(categoria_risco: str) -> str:
  if categoria_risco == 'baixo':
    return "🟢"
  elif categoria_risco == 'medio':
    return "🟡"
  else:
    return "🔴"

st.title("🏥 Sistema Fuzzy para Diagnóstico de Deabetes e Hipertensão")
st.markdown("---")

st.subheader("Dados Clínicos do Paciente")

col1, col2 = st.columns(2)

with col1:
  entrada_idade = st.number_input(
    "👤 Idade (anos)", 
    min_value=1, 
    max_value=120, 
    value=30,
    help="Idade do paciente em anos completos"
  )
  entrada_imc = st.number_input(
    "⚖️ IMC (kg/m²)", 
    min_value=10.0, 
    max_value=50.0, 
    value=25.0, 
    step=0.1,
    help="Índice de Massa Corporal = peso(kg) / altura²(m)"
  )

with col2:
  entrada_glicemia = st.number_input(
    "🩸 Glicemia (mg/dL)", 
    min_value=50, 
    max_value=300, 
    value=100,
    help="Nível de glicose no sangue em jejum"
  )
  entrada_pressao = st.number_input(
    "💓 Pressão Sistólica (mmHg)", 
    min_value=70, 
    max_value=220, 
    value=120,
    help="Pressão arterial sistólica (valor maior na medição)"
  )

st.markdown("---")

if st.button("Calcular Riscos", type="primary", use_container_width=True):
  try:
    with st.spinner("Processando avaliação de risco..."):
      simulacao_sistema.input['idade'] = entrada_idade
      simulacao_sistema.input['imc'] = entrada_imc
      simulacao_sistema.input['glicemia'] = entrada_glicemia
      simulacao_sistema.input['pas'] = entrada_pressao
      simulacao_sistema.compute()

      percentual_risco_diabetes = simulacao_sistema.output['risco_diabetes']
      percentual_risco_hipertensao = simulacao_sistema.output['risco_hipertensao']

      categoria_diabetes = obter_categoria_semantica(simulacao_sistema, consequente_risco_diabetes, 'risco_diabetes')
      categoria_hipertensao = obter_categoria_semantica(simulacao_sistema, consequente_risco_hipertensao, 'risco_hipertensao')

    st.success("✅ Avaliação de risco concluída com sucesso!")
    st.markdown("---")
    
    st.subheader("Resultados da Avaliação")
    
    col1, col2 = st.columns(2)
    with col1:
      emoji_diabetes = obter_emoji_nivel_risco(categoria_diabetes)
      st.metric(
        "🩺 Risco de Diabetes", 
        f"{percentual_risco_diabetes:.1f}%", 
        f"{emoji_diabetes} {categoria_diabetes.capitalize()}"
      )
        
    with col2:
      emoji_hipertensao = obter_emoji_nivel_risco(categoria_hipertensao)
      st.metric(
        "❤️ Risco de Hipertensão", 
        f"{percentual_risco_hipertensao:.1f}%", 
        f"{emoji_hipertensao} {categoria_hipertensao.capitalize()}"
      )

    # Adicionando gráficos fuzzy
    st.markdown("---")
    st.subheader("Visualização das Funções Fuzzy")
    
    # Configuração dos gráficos
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Sistema Fuzzy - Funções de Pertinência e Ativações', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Idade
    ax = axes[0, 0]
    ax.plot(antecedente_idade.universe, antecedente_idade['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(antecedente_idade.universe, antecedente_idade['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(antecedente_idade.universe, antecedente_idade['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(entrada_idade, color='black', linestyle='--', linewidth=2, label=f'Entrada: {entrada_idade}')
    ax.set_title('👤 Idade (anos)', fontweight='bold')
    ax.set_xlabel('Idade')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Gráfico 2: IMC
    ax = axes[0, 1]
    ax.plot(antecedente_imc.universe, antecedente_imc['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(antecedente_imc.universe, antecedente_imc['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(antecedente_imc.universe, antecedente_imc['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(entrada_imc, color='black', linestyle='--', linewidth=2, label=f'Entrada: {entrada_imc}')
    ax.set_title('⚖️ IMC (kg/m²)', fontweight='bold')
    ax.set_xlabel('IMC')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Gráfico 3: Glicemia
    ax = axes[0, 2]
    ax.plot(antecedente_glicemia.universe, antecedente_glicemia['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(antecedente_glicemia.universe, antecedente_glicemia['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(antecedente_glicemia.universe, antecedente_glicemia['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(entrada_glicemia, color='black', linestyle='--', linewidth=2, label=f'Entrada: {entrada_glicemia}')
    ax.set_title('🩸 Glicemia (mg/dL)', fontweight='bold')
    ax.set_xlabel('Glicemia')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Gráfico 4: Pressão
    ax = axes[1, 0]
    ax.plot(antecedente_pressao.universe, antecedente_pressao['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(antecedente_pressao.universe, antecedente_pressao['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(antecedente_pressao.universe, antecedente_pressao['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(entrada_pressao, color='black', linestyle='--', linewidth=2, label=f'Entrada: {entrada_pressao}')
    ax.set_title('💓 Pressão Sistólica (mmHg)', fontweight='bold')
    ax.set_xlabel('Pressão')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Gráfico 5: Risco de Diabetes
    ax = axes[1, 1]
    ax.plot(consequente_risco_diabetes.universe, consequente_risco_diabetes['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(consequente_risco_diabetes.universe, consequente_risco_diabetes['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(consequente_risco_diabetes.universe, consequente_risco_diabetes['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(percentual_risco_diabetes, color='purple', linestyle='--', linewidth=3, label=f'Resultado: {percentual_risco_diabetes:.1f}%')
    ax.set_title('🩺 Risco de Diabetes (%)', fontweight='bold')
    ax.set_xlabel('Risco (%)')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Gráfico 6: Risco de Hipertensão
    ax = axes[1, 2]
    ax.plot(consequente_risco_hipertensao.universe, consequente_risco_hipertensao['baixo'].mf, 'b', linewidth=2, label='Baixo')
    ax.plot(consequente_risco_hipertensao.universe, consequente_risco_hipertensao['medio'].mf, 'g', linewidth=2, label='Médio')
    ax.plot(consequente_risco_hipertensao.universe, consequente_risco_hipertensao['alto'].mf, 'r', linewidth=2, label='Alto')
    ax.axvline(percentual_risco_hipertensao, color='purple', linestyle='--', linewidth=3, label=f'Resultado: {percentual_risco_hipertensao:.1f}%')
    ax.set_title('❤️ Risco de Hipertensão (%)', fontweight='bold')
    ax.set_xlabel('Risco (%)')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)

    graus_idade = {
      'Baixo': fuzz.interp_membership(antecedente_idade.universe, antecedente_idade['baixo'].mf, entrada_idade),
      'Médio': fuzz.interp_membership(antecedente_idade.universe, antecedente_idade['medio'].mf, entrada_idade),
      'Alto': fuzz.interp_membership(antecedente_idade.universe, antecedente_idade['alto'].mf, entrada_idade)
    }
    
    graus_imc = {
      'Baixo': fuzz.interp_membership(antecedente_imc.universe, antecedente_imc['baixo'].mf, entrada_imc),
      'Médio': fuzz.interp_membership(antecedente_imc.universe, antecedente_imc['medio'].mf, entrada_imc),
      'Alto': fuzz.interp_membership(antecedente_imc.universe, antecedente_imc['alto'].mf, entrada_imc)
    }
    
    graus_glicemia = {
      'Baixo': fuzz.interp_membership(antecedente_glicemia.universe, antecedente_glicemia['baixo'].mf, entrada_glicemia),
      'Médio': fuzz.interp_membership(antecedente_glicemia.universe, antecedente_glicemia['medio'].mf, entrada_glicemia),
      'Alto': fuzz.interp_membership(antecedente_glicemia.universe, antecedente_glicemia['alto'].mf, entrada_glicemia)
    }
    
    graus_pressao = {
      'Baixo': fuzz.interp_membership(antecedente_pressao.universe, antecedente_pressao['baixo'].mf, entrada_pressao),
      'Médio': fuzz.interp_membership(antecedente_pressao.universe, antecedente_pressao['medio'].mf, entrada_pressao),
      'Alto': fuzz.interp_membership(antecedente_pressao.universe, antecedente_pressao['alto'].mf, entrada_pressao)
    }
    
    # Gráfico de Fuzzificação
    st.markdown("---")
    st.subheader("Processo de Fuzzificação")
    st.write("Este gráfico mostra como os valores de entrada são convertidos em graus de pertinência fuzzy:")
    
    # Criar gráfico de fuzzificação
    fig_fuzz, ax_fuzz = plt.subplots(1, 1, figsize=(14, 8))
    
    # Preparar dados para o gráfico de barras
    variaveis = ['Idade', 'IMC', 'Glicemia', 'Pressão']
    niveis = ['Baixo', 'Médio', 'Alto']
    cores = ['blue', 'green', 'red']
    
    # Dados dos graus de pertinência
    dados_fuzzificacao = [
        [graus_idade['Baixo'], graus_idade['Médio'], graus_idade['Alto']],
        [graus_imc['Baixo'], graus_imc['Médio'], graus_imc['Alto']],
        [graus_glicemia['Baixo'], graus_glicemia['Médio'], graus_glicemia['Alto']],
        [graus_pressao['Baixo'], graus_pressao['Médio'], graus_pressao['Alto']]
    ]
    
    # Configurar posições das barras
    x = np.arange(len(variaveis))
    largura = 0.25
    
    # Criar barras agrupadas
    for i, (nivel, cor) in enumerate(zip(niveis, cores)):
        valores = [dados_fuzzificacao[j][i] for j in range(len(variaveis))]
        posicoes = x + (i - 1) * largura
        barras = ax_fuzz.bar(posicoes, valores, largura, label=nivel, color=cor, alpha=0.7, edgecolor='black')
        
        # Adicionar valores nas barras
        for barra, valor in zip(barras, valores):
            if valor > 0.01:
                ax_fuzz.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.01,
                           f'{valor:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Configurar o gráfico
    ax_fuzz.set_xlabel('Variáveis de Entrada', fontweight='bold', fontsize=12)
    ax_fuzz.set_ylabel('Grau de Pertinência', fontweight='bold', fontsize=12)
    ax_fuzz.set_title('Fuzzificação dos Valores de Entrada\n' + 
                     f'Idade: {entrada_idade} | IMC: {entrada_imc} | Glicemia: {entrada_glicemia} | Pressão: {entrada_pressao}',
                     fontweight='bold', fontsize=14)
    ax_fuzz.set_xticks(x)
    ax_fuzz.set_xticklabels(variaveis)
    ax_fuzz.legend()
    ax_fuzz.grid(True, alpha=0.3, axis='y')
    ax_fuzz.set_ylim(0, 1.1)
    
    # Adicionar linha de referência
    ax_fuzz.axhline(y=0.5, color='gray', linestyle=':', alpha=0.7, label='Referência (0.5)')
    
    plt.tight_layout()
    st.pyplot(fig_fuzz)
    
    # Explicação do processo
    st.info("""
    **📖 Como interpretar a Fuzzificação:**
    
    - **Barras Azuis (Baixo)**: Quanto o valor pertence à categoria "Baixo"
    - **Barras Verdes (Médio)**: Quanto o valor pertence à categoria "Médio"  
    - **Barras Vermelhas (Alto)**: Quanto o valor pertence à categoria "Alto"
    
    🔍 **Exemplo**: Se a idade tem grau 0.8 em "Alto" e 0.2 em "Médio", significa que a pessoa é considerada mais "idosa" que "meia-idade" pelo sistema fuzzy.
    """)
    
    # Métricas do processo fuzzy
    st.markdown("---")
    st.subheader("Resumo do Processo Fuzzy")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Calcular ativação total das regras
        total_ativacao = sum([
            max(graus_idade.values()),
            max(graus_imc.values()),
            max(graus_glicemia.values()),
            max(graus_pressao.values())
        ]) / 4
        st.metric("Ativação Média", f"{total_ativacao:.3f}")
    
    with col2:
        # Calcular incerteza (dispersão dos graus)
        incerteza_media = np.mean([
            np.std(list(graus_idade.values())),
            np.std(list(graus_imc.values())),
            np.std(list(graus_glicemia.values())),
            np.std(list(graus_pressao.values()))
        ])
        st.metric("Incerteza Média", f"{incerteza_media:.3f}")
    
    with col3:
        # Variável mais ativada
        max_ativacoes = {
            'Idade': max(graus_idade.values()),
            'IMC': max(graus_imc.values()),
            'Glicemia': max(graus_glicemia.values()),
            'Pressão': max(graus_pressao.values())
        }
        var_dominante = max(max_ativacoes, key=max_ativacoes.get)
        st.metric("Variável Dominante", var_dominante)

  except Exception as erro_processamento:
    st.error(f"❌ Erro ao calcular: {erro_processamento}")