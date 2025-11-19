from maspy import Environment, Percept

class AmbienteCidade(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        # O ambiente pode conter informações globais, como o "mapa"
        self.create(Percept("mapa_info", "Cidade 10x10"))
        self.create(Percept("estacao_loc", {"EstacaoNorte": (2,2), "EstacaoSul": (8,8)}))

    def on_connect(self, agt_name):
        self.print(f"Agente {agt_name} entrou no ambiente da cidade.")