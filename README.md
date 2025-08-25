Previsão do Tempo CLI




Um aplicativo de linha de comando (CLI) em Python para consultar o clima atual e a previsão dos próximos dias de qualquer cidade, utilizando a API gratuita Open-Meteo.
Exibe os resultados de forma bonita e organizada no terminal usando a biblioteca Rich.

🗂 Estrutura do Projeto
clima_cli/
├─ app/
│  ├─ __init__.py
│  ├─ api.py           # Comunicação com a API (geocoding + forecast)
│  ├─ formatters.py    # Formata e exibe os dados no terminal
│  └─ cli.py           # Ponto de entrada do programa
└─ requirements.txt    # Dependências do projeto
⚡ Funcionalidades

Consultar o clima de qualquer cidade pelo nome

Exibir clima atual (temperatura, umidade, chuva, condição)

Mostrar previsão dos próximos 3 dias

Tabelas e painéis coloridos e organizados no terminal

Permite escolher entre múltiplas cidades com o mesmo nome

🛠 Pré-requisitos

Python 3.10 ou superior

Conexão com a internet

Instalação das dependências: requests, rich, python-dateutil

💻 Instalação

Clone o repositório:

git clone https://github.com/seu-usuario/clima_cli.git
cd clima_cli

Crie e ative um ambiente virtual:

# Windows PowerShell
python -m venv .venv
. .venv/Scripts/Activate.ps1


# macOS/Linux
# python3 -m venv .venv
# source .venv/bin/activate

Instale as dependências:

pip install -r requirements.txt
🚀 Como usar
Executando sem argumentos
python -m app.cli

O programa pedirá que você digite o nome da cidade.

Executando com argumento
python -m app.cli "Belém"

Mostra automaticamente os resultados da cidade informada.

📝 Exemplo de saída
🌦️ CLI
┌─────────────────────────────┐
│ Local                       │
│ Belém • Pará • Brasil (−1.45, −48.50) │
└─────────────────────────────┘


Tabela: Agora
┌───────────┬───────────────┬──────────┬────────────┬─────────────┐
│ Quando    │ Condição      │ Temp (°C) │ Umidade (%) │ Precipitação (mm) │
│ 25/08 16:00 │ Céu limpo   │ 30.0      │ 80         │ 0.0          │
└───────────┴───────────────┴──────────┴────────────┴─────────────┘


Tabela: Próximos 3 dias
┌────────────┬───────────────┬──────────┬──────────┬──────────┐
│ Data       │ Condição      │ Mín (°C) │ Máx (°C) │ Chuva (mm) │
│ Seg, 26/08 │ Chuva fraca   │ 24.0      │ 31.0     │ 2.0       │
└────────────┴───────────────┴──────────┴──────────┴──────────┘
🔧 Estrutura do Código

api.py → Comunicação com a API Open-Meteo:

Geocodificação (nome → lat/lon)

Previsão horária e diária

Funções para extrair clima atual e resumo diário

formatters.py → Formatação e exibição no terminal:

Painel da cidade

Tabela do clima atual

Tabela próximos dias

cli.py → Interação com o usuário:

Recebe input do usuário

Chama funções da API

Organiza e exibe os dados

💡 Possíveis melhorias

Argumentos CLI para definir número de dias (--dias 5)

Suporte a diferentes unidades (°F, km/h)

Cache local para geocoding e previsões

Versão web com Streamlit ou Flask

Testes automatizados das funções principais
