# ⚡ Sistema de Negociação de Carga para VEs

Este projeto simula um ambiente de cidade inteligente onde **Veículos Autônomos** (agentes compradores) negociam serviços de recarga com **Estações de Recarga** (agentes vendedores). O sistema utiliza o framework MASPY para gerenciar a comunicação, crenças e objetivos dos agentes.

## 🧠 Lógica dos Agentes

### 🚗 Agente Veículo (`AgenteVeiculoAutonomo`)
Representa um carro elétrico com autonomia para tomar decisões baseadas em seu estado interno.
* **Estados:** Possui nível de bateria e localização.
* **Comportamento:**
    * Monitora a bateria: quando cai abaixo de 20%, inicia a busca por recarga.
    * **Preferências:** Pode priorizar "BARATO" (menor preço) ou "RAPIDO" (menor fila).
    * **Negociação:** Envia um pedido em *broadcast* e coleta propostas. Após um tempo de espera (`TIMEOUT`), escolhe a melhor opção e envia o aceite.

### ⛽ Agente Estação (`AgenteEstacaoDeRecarga`)
Representa um ponto de recarga com múltiplas vagas.
* **Preço Dinâmico:** O preço da recarga aumenta conforme a lotação da estação.
  > Fórmula: `Preço = Preço Base * (1 + (Vagas Ocupadas / Vagas Totais))`
* **Concorrência:** Gerencia o número de vagas disponíveis e rejeita pedidos se estiver lotada ou se a vaga for tomada por outro agente durante a negociação.

## 🏙️ O Ambiente (`AmbienteCidade`)
Simula uma cidade (grid 10x10) onde os agentes estão situados. O ambiente facilita a descoberta de serviços e mantém o estado global da simulação.

## 🔄 Fluxo de Interação (Protocolo)

1. **Solicitação:** O Veículo percebe bateria baixa e envia um `pedido_recarga` para todas as estações.
2. **Proposta:** As Estações com vagas disponíveis respondem com uma `proposta_estacao` contendo preço e tempo de espera estimado.
3. **Decisão:** O Veículo aguarda propostas por 5 segundos, seleciona a melhor (baseado em sua preferência) e envia `aceito_proposta`. As demais são rejeitadas.
4. **Confirmação:** A Estação escolhida verifica se a vaga ainda está livre.
    * **Sucesso:** Envia `confirmado` e reserva a vaga.
    * **Falha:** Envia `falha_recarga` (ex: vaga ocupada milissegundos antes).
5. **Serviço:** O Veículo simula o tempo de recarga e, ao finalizar, libera a vaga na estação.

## ⚙️ Configuração (`inputs.py`)

Você pode alterar os parâmetros da simulação no arquivo `inputs.py`:
* **CONFIG_VEICULOS:** Adicione mais carros, mude a bateria inicial ou a preferência.
* **CONFIG_ESTACOES:** Crie novas estações, altere o número de vagas ou o preço base.
* **TIMEOUTS:** Ajuste o tempo de negociação e recarga.

## ▶️ Como Executar

Certifique-se de estar na raiz do repositório `maspy-agents` e execute:

```bash
python charge-negotiation/main.py