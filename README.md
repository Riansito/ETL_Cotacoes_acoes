# 📈 Pipeline ETL de Dados Financeiros com Yahoo Finance + Airflow + Neon + Power BI

## 📌 Visão Geral

Este projeto consiste em um pipeline ETL automatizado para coleta, processamento e armazenamento de dados de ações utilizando a API do Yahoo Finance.

Os dados são coletados diariamente, tratados e armazenados em um banco PostgreSQL hospedado na nuvem utilizando o Neon. Posteriormente, o Power BI se conecta ao banco para geração de dashboards e relatórios analíticos.

Todo o fluxo é orquestrado pelo Apache Airflow executando automaticamente de segunda a sexta-feira às 05:00 da manhã.

---

# 🏢 Problema de Negócio

Uma empresa do setor financeiro deseja acompanhar diariamente o comportamento de ações da bolsa para auxiliar analistas e gestores na tomada de decisão de investimentos.

O processo era realizado manualmente:

* Os analistas acessavam plataformas financeiras todos os dias;
* Exportavam planilhas manualmente;
* Atualizavam relatórios no Power BI;
* Validavam inconsistências nos dados;
* E verificavam duplicidades manualmente.

Esse processo gerava diversos problemas:

* ❌ Perda de tempo operacional;
* ❌ Alto risco de erro humano;
* ❌ Dados inconsistentes;
* ❌ Relatórios desatualizados;
* ❌ Dificuldade de escalabilidade.

---

# ✅ Solução Desenvolvida

Foi desenvolvido um pipeline ETL automatizado capaz de:

* Coletar dados de ações automaticamente do Yahoo Finance;
* Validar se os dados retornados estão vazios;
* Transformar e padronizar os dados;
* Evitar envio de dados duplicados para o banco;
* Armazenar os dados em PostgreSQL na nuvem;
* Disponibilizar os dados para dashboards no Power BI;
* Automatizar toda a execução utilizando Apache Airflow.

---

# 🏗️ Arquitetura do Projeto

O pipeline realiza a coleta diária de dados financeiros do Yahoo Finance, processa as informações utilizando Python e Airflow, armazena os dados no PostgreSQL (Neon) e disponibiliza tudo para análise no Power BI.

## 🔄 Fluxo do Pipeline

```text
Yahoo Finance
      ↓
Extração dos Dados
      ↓
Transformação e Tratamento
      ↓
Carga no PostgreSQL (Neon)
      ↓
Power BI
````

## 📌 Fluxo Completo da Arquitetura

<img width="1859" height="846" alt="Arquitetura do Projeto" src="https://github.com/user-attachments/assets/ee376890-ea0c-41a6-91d8-26c0ce1eebc2" />


---

# ⚙️ Etapas do ETL

## 1️⃣ Extract — Extração dos Dados

A etapa de extração realiza:

* Conexão com o Yahoo Finance;
* Coleta diária dos dados das ações;
* Validação da resposta da API.

### 🔍 Validação Implementada

Antes de continuar o pipeline, o sistema verifica:

* Se os dados retornaram corretamente;
* Se o DataFrame está vazio;
* Se houve falha na coleta.

Caso os dados estejam vazios:

* O pipeline é interrompido;
* Nenhum dado inválido é enviado;
* Evita processamento desnecessário.

Isso é especialmente importante em:

* Feriados;
* Dias sem pregão;
* Problemas temporários da API.

---

## 2️⃣ Transform — Transformação dos Dados

Na etapa de transformação são realizados tratamentos como:

* Remoção de colunas desnecessárias;
* Padronização de nomes das colunas;
* Conversão de tipos de dados;
* Formatação de datas;
* Tratamento de valores nulos;
* Organização estrutural dos dados.

Essa etapa garante:

* Consistência;
* Padronização;
* Qualidade dos dados.

---

## 3️⃣ Load — Carga no Banco de Dados

Após o tratamento, os dados são enviados para o PostgreSQL hospedado no Neon.

### 🔍 Verificação de Duplicidade

Antes de inserir os dados, o pipeline verifica:

* Se os registros já existem no banco;
* Se a combinação de data + ticker já foi carregada.

Caso os dados já existam:

* O envio não é realizado;
* Evita duplicidade;
* Mantém integridade do banco.

---

# ⏰ Orquestração com Apache Airflow

O pipeline é automatizado utilizando Apache Airflow.

## Agendamento

Execução automática:

```cron
0 5 * * 1-5
```

Ou seja:

* Segunda a sexta-feira;
* Às 05:00 da manhã.

---

## 📌 Motivo do Agendamento

O mercado financeiro não opera:

* Aos sábados;
* Aos domingos;
* Em alguns feriados.

Mesmo em feriados, o pipeline permanece seguro porque:

* Se os dados vierem vazios;
* O processo é interrompido automaticamente;
* Nenhuma carga inválida é realizada.

---

# 📊 Integração com Power BI

O Power BI conecta diretamente ao PostgreSQL hospedado no Neon, permitindo atualização automática dos dashboards e monitoramento contínuo do mercado financeiro.

O projeto possui duas páginas principais desenvolvidas com foco em análise executiva e inteligência analítica do mercado.

# 📈 Página 1 — Visão Geral de Mercado

A primeira tela possui foco executivo e de monitoramento.

Nela são apresentados:

* KPIs principais do mercado;
* Volume total negociado;
* Maiores altas e quedas;
* Evolução temporal dos preços;
* Evolução do volume negociado;
* Análise candlestick;
* Insights automáticos;
* Monitoramento geral dos ativos.

O objetivo dessa página é fornecer uma visão rápida e estratégica do comportamento do mercado, permitindo identificar tendências, movimentações relevantes e ativos de destaque.

# 📉 Página 2 — Inteligência de Mercado e Análise de Risco

A segunda tela possui foco analítico e investigativo.

Nela são exploradas análises como:

* Volatilidade dos ativos;
* Performance percentual;
* Relação entre risco e retorno;
* Comparação entre ações;
* Insights inteligentes automatizados;
* Análise comportamental dos ativos.

A página utiliza visualizações analíticas como scatter plots e gráficos temporais para auxiliar na identificação de ativos mais arriscados, ativos mais estáveis e possíveis oportunidades de mercado.

O objetivo dessa tela é aprofundar a análise financeira e apoiar tomadas de decisão baseadas em comportamento, risco e performance dos ativos.


<p align="center">
  <img width="48%" alt="Captura de tela 2026-05-12 163857" src="https://github.com/user-attachments/assets/6f8b6840-f1d3-44e6-851c-596eff40e6de" />
  
  <img width="48%" alt="Captura de tela 2026-05-12 164938" src="https://github.com/user-attachments/assets/0367b975-b214-4d0c-9398-d78e44561cc8" />
</p>

<p align="center">
  <img width="70%" alt="Captura de tela 2026-05-12 164517" src="https://github.com/user-attachments/assets/f238ead0-0ab0-44db-be43-446dc0e6fd14" />
</p>

---

# 🛠️ Tecnologias Utilizadas

- Python  
- Pandas  
- Apache Airflow  
- Docker  
- PostgreSQL (Neon Database)  
- Power BI  
- yfinance  
---

# 📂 Estrutura do Projeto

```bash
project/
│
├── dags/
│   └── DAGs de orquestração do Airflow
│
├── notebooks/
│   └── Testes e análises exploratórias
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── Scripts principais do ETL
│
├── .gitignore
├── .python-version
├── README.md
├── docker-compose.yaml
├── main.py
├── pyproject.toml
└── uv.lock
```

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

---

## 2️⃣ Entrar na Pasta

```bash
cd seu-repositorio
```

---

## 3️⃣ Criar o Arquivo `.env`

```env
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=host_neon
POSTGRES_PORT=5432
POSTGRES_DB=database
```

---

## 4️⃣ Subir o Ambiente Docker

```bash
docker-compose up --build
```

---

## 5️⃣ Acessar o Airflow

```text
http://localhost:8080
```

---

## 6️⃣ Ativar a DAG

Após acessar o Airflow:

* Ative a DAG;
* O pipeline começará a executar automaticamente.

---

# ✅ Benefícios do Projeto

* Automação completa do processo;
* Eliminação de tarefas manuais;
* Redução de erros;
* Dados padronizados;
* Controle de duplicidade;
* Segurança contra dados vazios;
* Escalabilidade;
* Atualização automática dos dashboards.
