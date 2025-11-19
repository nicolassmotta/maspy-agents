from maspy import *
from random import uniform

class AgenteEstacaoDeRecarga(Agent):

    def __init__(self, agent_id, num_vagas=3, preco_base=0.50, localizacao=(0,0)):
        super().__init__(agent_id)
        
        self.localizacao = localizacao
        self.preco_base = preco_base
        
        self.add(Belief("vagas_total", num_vagas))
        self.add(Belief("vagas_ocupadas", 0))
        self.add(Belief("localizacao", self.localizacao))
        self.add(Belief("tipo_servico", "estacao_recarga"))

    @pl(gain, Belief("pedido_recarga", Any))
    def receber_pedido_recarga(self, src, pedido):
        self.print(f"Recebi pedido de recarga de {src} em {pedido['localizacao']}")
        
        vagas_total_belief = self.get(Belief("vagas_total", Any))
        vagas_ocupadas_belief = self.get(Belief("vagas_ocupadas", Any))

        # Verifica se as crenças existem antes de usar .args
        if not vagas_total_belief or not vagas_ocupadas_belief:
             self.print("Erro: Não encontrei crenças de vagas.")
             return

        vagas_total = vagas_total_belief.args
        vagas_ocupadas = vagas_ocupadas_belief.args
        
        if vagas_ocupadas >= vagas_total:
            self.print("Estou lotado. Não enviarei proposta.")
            return

        preco_atual = self.preco_base * (1 + (vagas_ocupadas / vagas_total))
        tempo_espera = vagas_ocupadas * 5 
        
        proposta = {
            "sender": self.my_name,
            "preco": round(preco_atual, 2),
            "espera": tempo_espera,
            "localizacao": self.localizacao
        }
        
        self.print(f"Enviando proposta para {src}: {proposta}")
        self.send(src, achieve, Goal("proposta_estacao", proposta))

    @pl(gain, Goal("aceito_proposta", Any), Belief("vagas_ocupadas", Any))
    def proposta_aceita(self, src, aceite, vagas_ocupadas_args): # Recebe os argumentos
        self.print(f"Veículo {aceite['id']} (origem: {src}) aceitou a proposta.")
        
        vagas_total = self.get(Belief("vagas_total", Any)).args
        # Pega o objeto da crença para poder usar .change()
        vagas_ocupadas_belief = self.get(Belief("vagas_ocupadas", vagas_ocupadas_args)) 

        if not vagas_ocupadas_belief:
             self.print(f"FALHA: {src} aceitou, mas a crença de vagas ocupadas mudou. Rejeitando.")
             self.send(src, tell, Belief("falha_recarga", {"razao": "Erro interno de concorrência na estação."}))
             return

        vagas_ocupadas = vagas_ocupadas_args # Valor atual
        
        if vagas_ocupadas < vagas_total:
            # Aloca a vaga usando .change() para segurança
            novas_vagas_ocupadas = vagas_ocupadas + 1
            vagas_ocupadas_belief.change(args=novas_vagas_ocupadas) 
            
            self.print(f"Vaga alocada para {src}. Vagas ocupadas: {novas_vagas_ocupadas}/{vagas_total}")
            self.send(src, tell, Belief("confirmado", {"vaga_id": novas_vagas_ocupadas, "preco": "..."}))
        else:
            self.print(f"FALHA: {src} aceitou, mas não há mais vagas ({vagas_ocupadas}/{vagas_total}).")
            self.send(src, tell, Belief("falha_recarga", {"razao": "Vaga ocupada por outro veículo."}))

    @pl(gain, Belief("rejeita_proposta"))
    def proposta_rejeitada(self, src):
        self.print(f"Veículo {src} rejeitou minha proposta.")
        
    @pl(gain, Belief("saiu_da_vaga", Any), Belief("vagas_ocupadas", Any))
    def liberar_vaga(self, src, info_saida, vagas_ocupadas_args):
        """
        Plano disparado quando um veículo informa que terminou a recarga.
        """
        self.print(f"Veículo {info_saida['id']} (origem: {src}) informa que liberou a vaga.")
        
        vagas_ocupadas_belief = self.get(Belief("vagas_ocupadas", vagas_ocupadas_args))

        if not vagas_ocupadas_belief:
             self.print("Erro: Não encontrei crença de vagas ocupadas para liberar.")
             return
        
        vagas_ocupadas = vagas_ocupadas_args # Valor atual
        
        if vagas_ocupadas > 0:
            # Libera a vaga usando .change()
            novas_vagas_ocupadas = vagas_ocupadas - 1
            vagas_ocupadas_belief.change(args=novas_vagas_ocupadas)
            vagas_total = self.get(Belief("vagas_total", Any)).args
            self.print(f"Vaga liberada por {src}. Vagas ocupadas: {novas_vagas_ocupadas}/{vagas_total}")
        else:
             self.print(f"Aviso: {src} tentou liberar vaga, mas contador já estava em 0.")