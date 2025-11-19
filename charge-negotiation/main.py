from maspy import *
from agente_veiculo import AgenteVeiculoAutonomo
from agente_estacao import AgenteEstacaoDeRecarga
from ambiente_sma import AmbienteCidade
from inputs import CONFIG_VEICULOS, CONFIG_ESTACOES

if __name__ == "__main__":
    
    # Cria o Ambiente
    cidade = AmbienteCidade("MinhaCidade")
    
    # --- Carrega Veículos
    veiculos = []
    for config in CONFIG_VEICULOS:
        veiculos.append(
            AgenteVeiculoAutonomo(
                config["id"],
                bateria_inicial=config["bateria_inicial"],
                preferencia=config["preferencia"]
            )
        )
    
    # --- Carrega Estações
    estacoes = []
    for config in CONFIG_ESTACOES:
        estacoes.append(
            AgenteEstacaoDeRecarga(
                config["id"],
                num_vagas=config["num_vagas"],
                preco_base=config["preco_base"],
                localizacao=config["localizacao"]
            )
        )
    
    agentes = veiculos + estacoes
    Admin().connect_to(agentes, cidade)
    
    # Inicia o sistema
    print("--- Iniciando Simulação SMA de Recarga ---")
    Admin().start_system()