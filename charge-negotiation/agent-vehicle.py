from maspy import *
from random import uniform
import time
from inputs import TIMEOUT_NEGOCIACAO, TEMPO_RECARGA

class AgenteVeiculoAutonomo(Agent):

    def __init__(self, agent_id, bateria_inicial=100, localizacao_inicial=(0,0), preferencia="BARATO"):
        super().__init__(agent_id)

        self.bateria = bateria_inicial
        self.localizacao = localizacao_inicial

        self.add(Belief("bateria", self.bateria))
        self.add(Belief("localizacao", self.localizacao))
        self.add(Belief("limite_urgencia", 20))
        self.add(Belief("preferencia", preferencia))

        self.add(Goal("viver"))

    @pl(gain, Goal("viver"))
    def viver(self, src):
        if self.bateria > 0:
            self.bateria -= uniform(0.5, 2.0)
            bateria_belief = self.get(Belief("bateria", Any))
            if bateria_belief:
                bateria_belief.change(args=round(self.bateria, 2))

        limite = self.get(Belief("limite_urgencia", Any)).args

        precisa_recarga = self.bateria <= limite
        esta_negociando = self.has(Belief("negociando"))
        decisao_pendente = self.has(Goal("decidir_recarga"))

        if precisa_recarga and not esta_negociando and not decisao_pendente:
            self.print(f"Bateria baixa ({self.bateria:.2f}%)! Procurando recarga.")
            self.add(Goal("procurar_recarga"))

        time.sleep(2)
        if self.running:
            self.add(Goal("viver"))

    @pl(gain, Goal("procurar_recarga"))
    def procurar_recarga(self, src):
        if not self.has(Belief("negociando")):
            self.add(Belief("negociando"))

        self.print("Enviando CFP (pedido_recarga) para todas as estações...")
        self.send(broadcast,
                  tell,
                  Belief("pedido_recarga", {"localizacao": self.localizacao}))

        self.add(Goal("decidir_recarga"))

    @pl(gain, Goal("proposta_estacao", Any))
    def armazenar_proposta(self, src, proposta):
        if self.has(Belief("negociando")):
            self.print(f"Recebi e armazenei proposta de {proposta['sender']}: Preço={proposta['preco']}")
            self.add(Belief("proposta_recebida", proposta))
        else:
            self.print(f"Recebi proposta de {proposta['sender']}, mas não estou negociando. Rejeitando.")
            self.send(proposta['sender'], tell, Belief("rejeita_proposta"))

    @pl(gain, Goal("decidir_recarga"))
    def decidir_recarga(self, src):
        self.print(f"Iniciando período de espera por propostas ({TIMEOUT_NEGOCIACAO}s)...")
        self.wait(TIMEOUT_NEGOCIACAO)

        self.print("Tempo de espera esgotado. Avaliando todas as propostas...")

        propostas_beliefs = self.get(Belief("proposta_recebida", Any), all=True)

        if not propostas_beliefs:
            self.print("Nenhuma proposta recebida.")
            negociando_belief = self.get(Belief("negociando", Any), ck_src=False)
            if negociando_belief:
                self.print("Removendo flag 'negociando' (sem propostas).")
                self.rm(negociando_belief)
            return

        propostas = [b.args for b in propostas_beliefs]
        preferencia = self.get(Belief("preferencia", Any)).args
        melhor_proposta = None

        if preferencia == "BARATO":
            melhor_proposta = min(propostas, key=lambda p: p['preco'])
        elif preferencia == "RAPIDO":
            melhor_proposta = min(propostas, key=lambda p: p['espera'])

        if not melhor_proposta:
             melhor_proposta = min(propostas, key=lambda p: p['preco'])

        self.print(f"Melhor proposta é de {melhor_proposta['sender']} com Preço={melhor_proposta['preco']}")

        for p in propostas:
            target_agent = p['sender']
            if target_agent == melhor_proposta['sender']:
                self.print(f"Enviando ACEITE para {target_agent}")
                self.send(target_agent, achieve, Goal("aceito_proposta", {"id": self.my_name}))
            else:
                self.print(f"Enviando REJEIÇÃO para {target_agent}")
                self.send(target_agent, tell, Belief("rejeita_proposta"))

        if propostas_beliefs:
            self.rm(propostas_beliefs)


    @pl(gain, Belief("confirmado", Any))
    def recarga_confirmada(self, src, confirmacao):
        self.print(f"Recarga confirmada na {src}! Detalhes: {confirmacao}")

        negociando_belief = self.get(Belief("negociando", Any), ck_src=False)
        if negociando_belief:
            self.print("Removendo flag 'negociando' (sucesso).")
            self.rm(negociando_belief)

        self.print("Simulando recarga...")
        time.sleep(TEMPO_RECARGA)
        self.bateria = 100
        bateria_belief = self.get(Belief("bateria", Any))
        if bateria_belief:
            bateria_belief.change(args=self.bateria)
        self.print(f"Recarga completa! Bateria: {self.bateria}%")

        self.print(f"Informando {src} que a vaga foi liberada.")
        self.send(src, tell, Belief("saiu_da_vaga", {"id": self.my_name}))


    @pl(gain, Belief("falha_recarga", Any))
    def falha_recarga(self, src, razao):
        self.print(f"FALHA da {src}: {razao}. Reiniciando busca...")
        
        negociando_belief = self.get(Belief("negociando", Any), ck_src=False)
        if negociando_belief:
            self.print("Removendo flag 'negociando' (falha).")
            self.rm(negociando_belief)