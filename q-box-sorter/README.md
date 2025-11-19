# q-box-sorter

Este projeto implementa um agente inteligente de alocação utilizando a biblioteca **MASPY**. O sistema simula um ambiente onde um robô deve aprender, através de Aprendizado por Reforço (Q-Learning), a mover objetos de uma prateleira para as caixas corretas a fim de maximizar sua pontuação.

## 📋 Sobre o Projeto

O agente, denominado `AgenteAlocador`, interage com o ambiente `AlocadorEnv`. O objetivo é retirar dois objetos (`Object_1` e `Object_2`) de uma prateleira (`Shelf`) e colocá-los em uma das três caixas disponíveis (`Box_1`, `Box_2`, `Box_3`).

O agente não conhece as regras inicialmente e deve aprendê-las através de **5 episódios de treinamento** definidos no código.

### Dinâmica de Recompensas

O ambiente possui uma lógica de pontuação que guia o aprendizado do agente:

* **Object_1:**
    * Melhor destino: `Box_3` (+7 pontos)
    * `Box_1`: +5 pontos
    * `Box_2`: -5 pontos (penalidade)
* **Object_2:**
    * Melhor destino: `Box_2` (+5 pontos)
    * `Box_1`: -5 pontos
    * `Box_3`: -2 pontos
* **Penalidades:** Tentar mover um objeto que já foi alocado resulta em -10 pontos.

## 🚀 Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [MASPY](https://github.com/nicolassmotta/MASPY).

## 🛠️ Como Executar

Certifique-se de ter a biblioteca `maspy` instalada e configurada. Execute o arquivo principal:

```bash
python main.py