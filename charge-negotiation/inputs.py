# Configuração dos veículos
CONFIG_VEICULOS = [
    {"id": "AVA_1", "bateria_inicial": 16, "preferencia": "BARATO"},
    {"id": "AVA_2", "bateria_inicial": 15, "preferencia": "BARATO"},
    {"id": "AVA_3", "bateria_inicial": 17, "preferencia": "BARATO"},
]
# Configuração das estações
CONFIG_ESTACOES = [
    # Estação cara
    {"id": "EstacaoNorte", "num_vagas": 1, "preco_base": 0.75, "localizacao": (2,2)},
    
    # Estação barata com apenas 1 VAGA para forçar o conflito
    {"id": "EstacaoSul", "num_vagas": 1, "preco_base": 0.50, "localizacao": (8,8)},
]

TIMEOUT_NEGOCIACAO = 5
TEMPO_RECARGA = 5
