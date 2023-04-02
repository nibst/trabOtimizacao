import math
def isPerfectSquare(n):
    return math.ceil(math.sqrt(n)) == math.floor(math.sqrt(n))

def open_file(instancia):
  """
  param:instancia:str - nome do arquivo a ser aberto
  out: len(lista), lista
  """ 
  instance = "instance_" + str(instancia) +".dat"
  location = "./instances/" + instance
  data = open(location).read().split()

  length, lista = int(data[0]), (data[1:])
  return length,lista

def get_list(instancia):
  length, lista = open_file(instancia)

  ps, qtt = get_ps_from_list(lista)
  ps_list = get_numbers(ps,qtt.copy())
  return ps_list, length

def get_ps_from_list(data):
    """
    input: lista de números
    return: lista de tuplas contendo as duplas que cuja soma
    return: dicionario {numero:qtd de vezes que aparece}

    é um quadrado perfeito
    """
    ps = []
    qtt = {}
    for i in range(len(data)):
        number1 = int(data[i])
        qtt[number1] = qtt.get(number1, 0) + 1
        for j in range(i+1,len(data)):
            number2 = int(data[j])
            if (isPerfectSquare(number1+number2)):
                ps.append((data[i],data[j]))
    return ps,qtt

def get_numbers(data,dic):
    """
    param:data -  lista dos numeros
    param:dicionario  - {numero:quantidade} 
    return: lista com números que fazem parte de uma possível dupla cuja
    soma forma um qp
    """
    n =[]
    for n1,n2 in data:
        n1 = int(n1)
        n2 = int(n2)
      
        if dic[n1]:
            n.append(n1)
            dic[n1] = dic.get(n1) - 1
        if dic[n2]:
            n.append(n2)
            dic[n2] = dic.get(n2) - 1
    return n
