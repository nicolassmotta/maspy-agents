# 🤖 Agentes Inteligentes com MASPY

Este repositório reúne implementações de Sistemas Multiagentes (SMA) e Aprendizado por Reforço desenvolvidas com a biblioteca [MASPY](https://github.com/nicolassmotta/MASPY). O objetivo é demonstrar diferentes protocolos de interação, negociação e aprendizado em ambientes simulados.

## 📂 Projetos Disponíveis

### 1. [EV Charging Negotiation](./charge-negotiation)
📍 **Diretório:** `/charge-negotiation`
Um sistema de negociação onde Veículos Autônomos interagem com Estações de Recarga em uma cidade simulada.
* **Destaques:** Protocolo de negociação (CNP), preços dinâmicos baseados em oferta/demanda e tomada de decisão baseada em preferências (Preço vs. Tempo).

### 2. [Q-Box Sorter](./q-box-sorter)
📍 **Diretório:** `/q-box-sorter`
Um agente que aprende a classificar objetos em caixas corretas utilizando Aprendizado por Reforço (Q-Learning).
* **Destaques:** Definição de ambiente MDP (Markov Decision Process), recompensas e punições, treinamento e exploração.

## 🚀 Instalação e Uso

### Pré-requisitos
* Python 3.8+
* Biblioteca `maspy`

### Configuração
1. Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/maspy-agents.git](https://github.com/seu-usuario/maspy-agents.git)
    cd maspy-agents

2. Instale as dependências:
    pip install -r requirements.txt

3. Para executar um projeto específico, navegue até a pasta ou execute o script principal. Exemplo:
    python charge-negotiation/main.py