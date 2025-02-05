#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random
import sys
import math


# O(n)
def weighted_median(I, P, V, N, W):
    items_added = []
    weight_added = []
    value_added = []
    #Se |items| == 0, não há items para adicionar a mochila
    if(N == 0):
        return []

    #Se |items| == 1 e capacidade da < items[0].peso 
    if N == 1 and P[0] > W:
        items_added.append(I[0])
        weight_added.append(W)
        value_added(W*V[0]/P[0])
        return items_added, weight_added, value_added
    
    v_w = [x/z for x, y, z in zip(P, V)]
    median = select (v_w, math.ceil(len(v_w)/2) - 1)

    L1 = [] # Itens com valor/peso < que a mediana
    L2 = [] # Itens com valor/peso = que a mediana
    L3 = [] # Itens com valor/peso > que a mediana 

    counter = 0

    for item in I:
        #print(item)
        if v_w[counter] > median:
            L1.append(item)
        elif v_w[counter] ==  median:
            L2.append(item)
        else:
            L3.append(item)

    sum_L1 = 0
    for item in L1:
        sum_L1 += P[item]

    sum_L2 = 0
    for item in L2:
        sum_L2 += P[item]

    sum_L3 = 0
    for item in L3:
        sum_L3 += P[item]
   
    if sum_L1 < W and sum_L1 + sum_L2 >= W:
        #print("===> Adiciona frações")
        for item in L2:
            if sum_L1 == W:
                break
            elif sum_L1 + P[item] > W:
                items_added.append(I[0])
                weight_added.append(W)
                value_added(W*V[0]/P[0])
                break
            else:
                items_added.append(item)
                L1.append(item)
                W = W - item[2]
        return L1
    if sum_L1 + sum_L2 < W:
        return L1 + L2 + (weighted_median(L3, W - (sum_L1 + sum_L2)))
    if sum_L1 > W:
        return weighted_median(L1, W)  

    #print("===> Seu algorítmo está mal projetado")
def select(items, k):

    if(len(items) == 1):
        #print("===> Um item")
        #print(items)
        return items[0]
    S = []
    lIndex = 0
    while lIndex+5 < len(items):
        S.append(items[lIndex:lIndex+5])
        lIndex += 5
    S.append(items[lIndex:])

    medianas = []
    for subList in S:
        subList.sort(key = lambda subList : subList[0], reverse = False)
        #Calcula mediana das medianas recursivamente a partir do agrupamento das medianas dos grupos de 5 items
        medianas.append(subList[math.ceil(len(subList)/2) - 1])
        #print(subList)
    #print(medianas)

    median = select(medianas, math.ceil(len(medianas)/2) - 1)

    #print("===> Mediana encontrada:")
    #print(median)
    #print("===> Arranging")
    #print(items)

    L1 = [] # Itens com valor/peso < que a mediana
    L2 = [] # Itens com valor/peso = que a mediana
    L3 = [] # Itens com valor/peso > que a mediana 

    for item in items:
        if item[0] < median[0]:
            L1.append(item)
        elif item[0] ==  median[0]:
            L2.append(item)
        else:
            L3.append(item)

    A = L1 + L2 + L3

    #print("===> A")
    #print(A)
    #print("===> Median atual")
    #print(median)
    j = 0
    count = 0
    for item in A:
        if(item == median):
            j = count
        count += 1

    #print("===> J")
    #print(j)
    #print("===> K")
    #print(k)

    if(k < j):
        #print("===> <")
        #print(A[0:j])
        return select(A[0:j],k)
    elif(k == j):
        #print("===> ==")
        #print(median)
        return median
    else:
        #print("===> >")
        #print(A[j+1:len(A)])
        return select(A[j+1:len(A)],k-j) 
    
def prepara_items(items):
    items_tmp = []
    for nome, peso, valor in items:
        item_tmp = (valor/peso, nome, peso, valor)
        items_tmp.append(item_tmp)
    return items_tmp

def generate_items(size):
    items = []
    for i in range(size):
        random_name = "item {0}".format(i)
        random_weight = random.uniform(1.0, 5.0)
        random_value = random.uniform(1.0, 5.0)
        item = (random_name, random_weight, random_value)
        items.append(item)
    return items

if __name__ == "__main__":

    knapsack_weight = 0.0
    items = []

    #Modo de teste com valores pré-definidos
    if sys.argv[1] == "test":
        print("===> Modo teste para validar alogritmo")
        
        items = [
            ("item1", 1.0, 2.0),
            ("item2", 1.0, 2.5),
            ("item3", 1.0, 3.0),
            ("item4", 1.0, 4.0),
            ("item5", 1.0, 1.0),
            ("item6", 1.0, 5.0)
        ]

        knapsack_weight = 3.5

    #Modo de teste com valores e pesos de items gerados aleatóriamente   
    elif len(sys.argv) == 3:

        knapsack_weight = float(sys.argv[1])
        item_size = int(sys.argv[2])

        print("===> Gerarando mochila com valorizes randomicos - ")
        print("===> {0} de peso e {1} items".format(knapsack_weight, item_size))
        items = generate_items(item_size)

    #Erro ao chamar linha de comando    
    else:
        print("==> Não encontrei um padrão")

    items_to_add = weighted_median(prepara_items(items), knapsack_weight);
    print("===> Capacidade da Mochila: {0}".format(knapsack_weight))
    print("===> Itens que ficam no mochila:")
    peso = 0
    valor = 0
    for item in items_to_add:
        print(item)
        peso += item[2]
        valor += item[3]

    print("===> Peso da mochila: {0}".format(peso))
    print("===> Valor da mochila: {0}".format(valor))
