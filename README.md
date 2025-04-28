# 🚀 CryptoPrice Dashboard

Bem-vindo ao **CryptoPrice Dashboard**! Este é um projeto interativo desenvolvido em **Python** e **Streamlit**, que monitora em tempo real o desempenho das 10 principais criptomoedas do mercado.

---

## 📋 Sobre o Projeto

O **CryptoPrice Dashboard** foi criado para:

- Monitorar a variação de preço das maiores criptomoedas.
- Exibir resumos analíticos, gráficos interativos e tabelas detalhadas.
- Permitir atualização automática dos dados com apenas um clique.
- Oferecer uma experiência fluída, com feedbacks amigáveis ao usuário.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- **Streamlit** - Criação do front-end interativo.
- **Pandas** - Manipulação de dados.
- **Requests** - Requisições à API da CoinGecko.
- **CoinGecko API** - Fonte dos dados de criptomoedas.
- **Glob e OS** - Organização de arquivos e pastas.

---

## ⚙️ Funcionalidades Principais

- 🔄 **Atualizar Dados**: Coleta os dados mais recentes das criptomoedas.
- 🏠 **Visão Geral**: Mostra a moeda que mais subiu, mais caiu e a média de variação.
- 📈 **Gráficos Dinâmicos**: Visualize rapidamente variações, market cap e volume.
- 📑 **Tabela Detalhada**: Dados organizados e filtrados das 10 maiores moedas.
- ⏳ **Mensagens de Feedback**: Atualizações e erros tratados com animações elegantes.
- 🧹 **Gerenciamento de Arquivos**: Mantém apenas os 5 arquivos CSV mais recentes no projeto.

---

## 🖥️ Layout da Interface

- **Sidebar** para navegação entre as seções:
  - Visão Geral
  - Gráficos
  - Tabela Detalhada
- **Botão Atualizar Dados** fixo e de fácil acesso.
- **Mensagem de sucesso** com efeito de fade-out suave.
- **Experiência contínua**: ao atualizar os dados, você continua na mesma página.

---

## 🧩 Estrutura do Projeto

```plaintext
CryptoPrice-Dashboard/
│
├── dashboard/
│   └── app.py               # Código principal do Streamlit
│
├── data/
│   ├── processed/            # Arquivos CSV processados para análise
│   └── raw/                  # Arquivos CSV brutos coletados
│
├── src/
│   ├── data_fetcher.py       # Coleta dados da API CoinGecko
│   └── data_processor.py     # Processa os dados brutos
│
├── venv/                     # Ambiente virtual (não versionado)
├── README.md                 # Documentação do projeto
├── requirements.txt          # Dependências do projeto
└── ...
```

---

## 📦 Como Rodar o Projeto

1. **Clone o repositório**:

      ```bash
      git clone https://github.com/seu-usuario/CryptoPrice-Dashboard.git
      cd CryptoPrice-Dashboard
      ```

2. **(Opcional) Crie um ambiente virtual**:

      ```bash
      python -m venv venv
      # Ative o ambiente:
      # No Windows:
      venv\Scripts\activate
      # No Linux/Mac:
      source venv/bin/activate
      ```

3. **Instale as dependências**:

      ```bash
      pip install -r requirements.txt
      ```

4. **Rode o Dashboard**:

      ```bash
      streamlit run dashboard/app.py
      ```

---

## 📊 Demonstração

O dashboard exibe:

- Tabela completa das 10 principais criptomoedas.
- Gráficos interativos.
- Resumo visual de melhor e pior moeda do dia.

---

## 🔥 Melhorias Futuras

- 📅 Filtros por datas para acompanhar evolução histórica.
- 🏆 Ranking das 3 maiores altas e baixas.
- 📊 Novos gráficos comparativos (evolução semanal/mensal).
- 📱 Otimização para dispositivos móveis.
- 🌐 Hospedagem do Dashboard em nuvem (Streamlit Share, Render, AWS).

---

## 👨‍💻 Autor

![Profile Picture](https://avatars.githubusercontent.com/u/000000?v=4)  
**[@NathanThomaz](https://github.com/NathanThomaz)**  
Graduando em Sistemas de Informação | Desenvolvedor Full Stack  

- 💬 [LinkedIn](https://linkedin.com/in/nathan-thomaz-devs)  
- 📧 E-mail: <nathanthomaz@gmail.com>  
- 📸 Instagram: [@nathann_thomaz](https://instagram.com/nathann_thomaz)  
- 🌐 [Portfólio](https://nathanthomaz.github.io)  

---

## ⭐ Considerações

Este projeto é um case completo de:

- **Python Moderno + Dashboards**
- **Automação de Coleta e Processamento de Dados**
- **Boas práticas de organização de código**
- **Foco em UX/UI mesmo usando Streamlit**

Se você gostou, ⭐ marque o repositório e compartilhe!

---

🚀 **Obrigado por acompanhar o projeto!**
