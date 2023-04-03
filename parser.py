import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=str, help='instancia a ser utilizada')
    parser.add_argument('--g', type=int, help='numero de geraçoes')
    parser.add_argument('--n', type=int, help='numero de individuos')
    parser.add_argument('--k', type=int, help='numero de participantes do torneio')
    parser.add_argument('--m', type=float, help='probabilidade de mutacao')
    parser.add_argument('--e', type=int, help='n individuos elitismo')
    parser.add_argument('--seed', type=int, help='sla')
    args = parser.parse_args()
    return args

