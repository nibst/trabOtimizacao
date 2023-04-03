import random
from parser import parse_args
import utils
import sys


class GA:
  # def __init__(self,g,n,k,m,e,instancia)
  def __init__(self):
    """
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :param instancia:int - numero da instancia
    :return:list - melhor individuo encontrado
    """

    args = parse_args()
    g = args.g
    n = args.n
    k = args.k
    m = args.m
    e = args.e
    #self.i = args.i

    instancias = [4,5,6,10,20,50,100,200,500,1000,10000]
    for instancia in instancias:
      self.lista, self.length = utils.get_list_stats(instancia)
      if not self.lista:
        continue

      best_graph_data = []
      maior = 0
      valores = []
      
      iteracoes = 10 if instancia not in [1000,10000] else 1
      for _ in range(iteracoes):
        resultado, graph_data  = self.run_ga(g,n,k,m,e,self.lista)
        valor = self.evaluate(resultado,self.lista)
        valores.append(valor)
        if valor > maior:
          maior = valor
          best_graph_data = graph_data
          melhor_solucao = resultado
        avg = sum(valores)/len(valores)

      utils.create_graph(best_graph_data,True,instancia)
      print(resultado)
      print(self.lista)

      print(f"#######################")
      print(f"#      {instancia}             #")
      print(f"#######################")

      print(f"Maior valor encontrado    = {self.evaluate(melhor_solucao,self.lista)}")
      print(f"Valor médio encontrado    = {avg}")
      print(f"Melhor solução encontrada = {[self.lista[i] for i in melhor_solucao]}")
      #print(f"Valor da solução do prof. = {utils.ideal_value(my_instance.i)}")

    """
    print(f"Entrada      = {self.lista}")
    print(f"Qp possiveis = {utils.get_ps_from_list(self.lista)[0]}")
    print(f"Resultado    = {[self.lista[i] for i in result]}")
    print(f"Somas        = {(self.evaluate(result,self.lista))}")
    print(f"Valor ideal =  {utils.ideal_value(self.instancia)}")
    """
    # VOLTAR PARA O IRACE
    #print(self.evaluate(self.result,self.lista) * -1) # iRace sempre minimiza

    #utils.create_graph(graph_data)


  def best_worst_avg_diversity(self,population,data):
    """
      Informações para o gráfico
      Recebe uma lista de individuos e retorna seu melhor valor,pior valor, media dos valores e diversidade
      Diversidade é baseada na quantidade de individuos com a mesma quantidade de conflitos.
      :param population: lista com os individuos
      :return: quadrupla com melhor,pior, media e o grau de diversidade
    """
    diversity_list = []
    smallest, biggest, sums = float("inf"), -float("inf"), 0
    for individual in population:
      value = self.evaluate(individual,data)
      smallest = value if value < smallest else smallest
      biggest =  value if value > biggest else biggest
      sums += value
      diversity_list.append(value)

    diversity = len(set(diversity_list)) / len(population)
    return smallest,biggest,sums/len(population),diversity


  def evaluate(self,individual,data):
      """
      Recebe um indivíduo (lista de inteiros) e retorna o número de pares
      cuja soma forma um quadrado perfeito.

      :param individual:list
      :return:int numero de duplas cuja soma é um qp
      """
      # TODO teste com profiler: Vale mais a pena verificar se está na lista ou calcular?
      total = 0
      #print("erro: individual",individual)
      for i in range(len(individual)-1):
        if utils.isPerfectSquare(data[individual[i]] + data[individual[i+1]]):
          total += 1
      return total

  def tournament(self,participants,ps_list):
      """
      Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
      ao numero de conflitos
      :param participants:list - lista de individuos
      :return:list melhor individuo da lista recebida
      """
      probs = []
      values = []
      for individual in participants:
        values.append(self.evaluate(individual,ps_list))
        reversed(values)   
      total = sum(values)
      if total == 0:
        total = 1
        probs = [1] * 10
      else:
        probs =[v / total for v in values]
      return random.choices(participants, weights=probs,k=1)[0]
      
  def crossover(self,p1, p2):
      """
      Partially Mapped Crossover (PMX):
      D.E. Goldberg and R. Lingle. Alleles, loci, and the traveling salesman problem.
      In Grefenstette [197], pages 154–159.

      Realiza o PMX de um ponto: recebe dois indivíduos e o ponto de
      cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
      dois indivíduos com o material genético trocado.
      Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
      deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
      A ordem dos dois indivíduos retornados não é importante
      (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
      :param parent1:list
      :param parent2:list
      :param index:int
      :return:list,list
      """
      if p1 == p2:
          return p1
      individual_size = len(p1)
      n = ["x"] * individual_size
      # 
      # Basic+Algorithms+and+Operators.pdf p.313 (276 no livro)
   
      
      n1, n2 = random.sample(range(individual_size),2)
      if n1 > n2:
        temp = n1
        n1 = n2
        n2 = temp
      n[n1:n2] = p1[n1:n2]
         
      # Achar outro algg pra essa parte aqui
      for i in range(individual_size):
        if p2[i] not in n:
          n[n.index('x')] = p2[i]
      return n

  def mutate(self,individual, m):
      """
      Recebe um indivíduo e a probabilidade de mutação (m).
      Caso random() < m, sorteia uma posição aleatória do indivíduo e
      coloca nela um número aleatório entre 1 e 8 (inclusive).
      :param individual:list
      :param m:int - probabilidade de mutacao
      :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
      """
      if random.random() <= m:
        if not len(individual):
          return individual
        pos1 = random.randint(0,len(individual)-1)
        pos2 = random.randint(0,len(individual)-1)
        while pos1 == pos2:  # garente que ocorra swap
          pos2 = random.randint(0,len(individual)-1)

        temp = individual[pos1]
          
        individual[pos1] = individual[pos2]
        individual[pos2] = temp

      return individual

  def run_ga(self,g, n, k, m, e,ps_list):
      """
      Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
      :param g:int - numero de gerações
      :param n:int - numero de individuos
      :param k:int - numero de participantes do torneio
      :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
      :param e:int - número de indivíduos no elitismo
      :return:list - melhor individuo encontrado
      """
      def select_parent(population):
        """
          Seleciona dois individuos de uma populacao
          :param population: lista com os individuos
          :return: 2 individuos (listas de 8 elementos)
        """
        p1 = random.choice(population)
        p2 = random.choice(population)
        #print(f"populacao = {population} \np1 = {p1} \np2 = {p2}")

        return p1,p2

      # Cria populacao a partir da listas de elementos que podem formar
      # uma dupla de qp
      population = []
      graph_data = []
      indexes = [i for i in range(len(ps_list))]

      for _ in range(n):
        shuffled_list = indexes.copy()
        random.shuffle(shuffled_list)
        population.append(shuffled_list)

      for _ in range(g):
        p = []
        graph_data.append(self.best_worst_avg_diversity(population,ps_list))
        while len(p) < e:
          p1 = self.tournament(random.sample(population,k),ps_list)
          p2 = self.tournament(random.sample(population,k),ps_list)
          #print(f"winner = {tournament_winner}")
          #p.append(tournament_winner)
          #p1, p2 = select_parent(p)

          child = self.crossover(p1,p2)
          child = self.mutate(child,m)
          p.append(child)

        population += p

      #print(tournament(participants))
      #print(evaluate(tournament(participants)))
      #print(len(graph_data))
      return self.tournament(population,ps_list), graph_data

if __name__ == "__main__":
    # read the first command-line argument and pass it to MyClass constructor
    #print(sys.argv)
    maior = -float("inf")
    lista = []
    melhor_solucao = []
    my_instance = GA()
    """
    for _ in range(1):
      my_instance = GA()
      resultado = my_instance.result
      valor = my_instance.evaluate(resultado,my_instance.lista)
      lista.append(valor)
      if valor > maior:
        maior = valor
        melhor_solucao = resultado

    avg = sum(lista)/len(lista)
    print(f"Maior valor encontrado    = {maior}")
    print(f"Valor médio encontrado    = {avg}")
    #print(f"Valor da solução do prof. = {utils.ideal_value(my_instance.i)}")
    print(f"Melhor solução encontrada = {[my_instance.lista[i] for i in resultado]}")
    """


