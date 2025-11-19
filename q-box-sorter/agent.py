from maspy import *
from maspy.learning import *

# --- Definição do Ambiente ---
class AlocadorEnv(Environment):
    def __init__(self, env_name=None):
        super().__init__(env_name)
        
        # Se não estiver aqui, o estado "estar na caixa 3" não existe para o agente
        locais = ("Shelf", "Box_1", "Box_2", "Box_3")
        
        # Criação dos Percepts (Estados)
        self.create(Percept("Object_1", locais, listed))
        self.create(Percept("Object_2", locais, listed))
        
        # Estado Inicial
        self.possible_starts = {"Object_1": "Shelf", "Object_2": "Shelf"}
    
    # Função de Transição
    def move_transition(self, state: dict, obj_to_box: tuple[str, str]):
        obj, box = obj_to_box
        obj_current_pos = state[obj]
        
        reward = 0
        
        # Só permite mover se o objeto estiver na prateleira
        if obj_current_pos == "Shelf":
            state[obj] = box # Atualiza o estado no modelo matemático
            
            # Tabela de Recompensas
            if obj == "Object_1":
                if box == "Box_1":
                    reward = 5
                elif box == "Box_2":
                    reward = -5
                elif box == "Box_3":
                    reward = 7  # Melhor escolha para Obj 1
            elif obj == "Object_2":
                if box == "Box_1":
                    reward = -5
                elif box == "Box_2":
                    reward = 5  # Melhor escolha para Obj 2
                elif box == "Box_3":
                    reward = -2
        else:
            # Penalidade por tentar mover algo que já foi alocado
            reward = -10

        # Verifica se terminou (Se ambos saíram da Prateleira)
        terminated = True
        for value in state.values():
            if value == "Shelf":
                terminated = False
                break

        return state, reward, terminated
        
    # Definição da Ação
    # CORREÇÃO CRUCIAL: Adicionar "Box_3" nas opções de destino
    @action(cartesian, (('Object_1', 'Object_2'), ('Box_1', 'Box_2', 'Box_3')), move_transition)
    def move(self, agt, obj_to_box: tuple[str, str]):
        obj, box = obj_to_box
        
        # Pega o percept real para atualizar o ambiente visualmente
        objeto_percept = self.get(Percept(obj, Any))
        
        if objeto_percept.values == "Shelf":
            self.print(f"{agt} moveu {obj} de {objeto_percept.values} para {box}")
            self.change(objeto_percept, box)
        else:
            self.print(f"{agt} tentou mover {obj}, mas ele ja esta em {objeto_percept.values}")

# --- Definição do Agente ---
class AgenteAlocador(Agent):
    def __init__(self, name=None):
        super().__init__(name)

    # Plano para treinar o modelo
    @pl(gain, Goal("treinar_modelo", Any))
    def realizar_treinamento(self, src, model_list: list[EnvModel]):
        model = model_list[0]
        
        # Logs informativos
        self.print(f"Iniciando treinamento...")
        self.print(f"Espaço de Estados: {len(model.states_list)} (esperado: 16)")
        # 2 Objetos x 3 Caixas = 6 ações possíveis
        self.print(f"Espaço de Ações: {len(model.actions_list)} (esperado: 6)") 
        
        # Treinamento com X episódios para garantir exploração da Box_3
        model.learn(qlearning, num_episodes=20, max_steps=10)
        
        self.print("Treinamento concluído. Executando política aprendida.")
        
        # Ativa o uso do modelo treinado
        self.auto_action = True
        self.add_policy(model)

# --- Execução ---
if __name__ == "__main__":
    # Instancia Ambiente e Modelo
    env = AlocadorEnv("AmbienteAlocacao")
    model = EnvModel(env)
    
    # Instancia Agente
    agente = AgenteAlocador("RoboAlocador")
    
    # Define o objetivo inicial passando o modelo criado
    agente.add(Goal("treinar_modelo", [model]))
    
    # Inicia o sistema
    Admin().start_system()