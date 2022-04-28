from re import L
import pandas as pd
import numpy as np
import itertools


'''All test cases'''
#df = pd.DataFrame({'Beef': [1,1,0,1,1,0,0], 'Chicken':[1,0,0,1,1,1,1], 'Cheese': [0,1,1,1,1,0,0]
#                , 'Clothes':[0,0,0,0,1,1,1], 'Boots':[0,0,1,0,0,0,0], 'Milk': [1,0,0,0,1,1,1]})
#
#df2 = pd.DataFrame({'Bread': [1,1,1,1,0], 'Cheese':[1,0,0,1,1], 'Juice': [1,0,1,1,1], 'Eggs': [0,0,0,0,1], 'Milk':[0,1,1,0,1], 'Yogurt':[0,1,0,0,0]})
#
#df3 = pd.read_csv('19127444/Data.csv', sep=',')
#
#df4 = pd.DataFrame({'Crab': [1,0,1,0], 'Milk': [1,1,0,1], 'Cheese': [1,1,0,1], 'Bread': [1,1,1,1], 'Apple': [0,1,1,0], 'Pie': [0,1,1,0]})
#
#df5 = pd.DataFrame({'Bread':[1,1,1,1,0], 'Cheese': [1,0,0,1,1], 'Juice': [1,0,1,1,1], 'Milk': [0,1,1,0,1], 'Yogurt': [0,1,0,0,0], 'Eggs': [0,0,0,1,0]})
#
#df6 = pd.DataFrame({'Beef': [1,1,0,1,1,0,0], 'Chicken': [1,0,0,1,1,1,1], 'Milk': [1,0,0,0,1,1,1], 'Cheese': [0,1,1,1,1,0,0], 
#                    'Boot': [0,0,1,0,0,0,0], 'Clothes': [0,0,0,0,1,1,1]})
#
#df7 = pd.DataFrame({'Crab': [1,0,1,0], 'Milk': [1,1,0,1], 'Cheese': [1,1,0,1], 'Bread': [1,1,1,1], 'Pie': [0,1,1,0], 'Apple': [0,1,1,0]})


class Items: # Class item present an itemset with support count
    def __init__(self, item, sup):
        self.itemset = item
        self.sup = sup
    def __repr__(self) -> str:
        return f"({self.itemset}, sup = {self.sup})"

def init_pass(T):
    out = []
    for item in T:
        temp = Items([item], T[item].sum() / len(T))
        out.append(temp)
    return sorted(out, key= lambda x: x.itemset)

def findsubsets(itemset,k):
    '''(k)subsets of itemset'''
    if k > len(itemset):
        return []
    return [list(i) for i in itertools.combinations(itemset, k)]

def candidate_gen(F):
    c = []
    f = [item.itemset for item in F]
    for i in range(len(f) - 1):
        temp = None
        for j in range(i+1, len(f)):
            f1 = sorted(f[i][:-1])
            f2 = sorted(f[j][:-1])
            if f1 == f2:
                temp = sorted(list(set(F[i].itemset + F[j].itemset)))
                c.append(temp)
            else:
                temp = []
                continue
            if len(temp) >= 2 :
                for subset in findsubsets(temp, len(temp) - 1):
                    if subset not in  f: 
                        c.remove(temp)
                        break
    return [Items(itemset, 0) for itemset in c]

def Contained(items, t):
    for item in items.itemset:
        if t[item] == 0:
            return False
    return True

def Apriori(T, minsup):
    F, f = [], []
    C = init_pass(T)

    for item in C:
        if item.sup >= minsup:
            f.append(item)
    #print(f)
    F.append(f)

    while(len(f)):
        f = []
        C = candidate_gen(F[-1])
        for t in range(len(T)):
            for item in C:
                if Contained(item, T.loc[t]):
                    item.sup += 1 / len(T)
        for item in C:
            if item.sup >= minsup:
                f.append(item)
        #print(f, end='\n\n')
        F.append(f)
        

    return F[:-1]

def confidence(Item, premise, T):
    count = 0
    for i in range(len(T)):
        if T.loc[i][premise].sum() == len(premise):
            count+=1
    return round(Item.sup * len(T) / count, 3)

def lift(conf, consequence, T):
    count = 0
    for i in range(len(T)):
        if T.loc[i][consequence].sum() == len(consequence):
            count+=1
    result = conf / (count / len(T))
    return round(result, 3)
    
def ap_genRules(item, H, T, minconf):
    if len(H) != 0 and len(item.itemset) > len(H[0].itemset) + 1:
        H = candidate_gen(H)
        i = 0
        while(i < len(H)):
            premise = list(set(item.itemset).difference(H[i].itemset))
            consequence = H[i].itemset
            conf = confidence(item, premise,T)
            measure = lift(conf, consequence, T)
            i += 1
            if conf >= minconf and measure > 1:
                    print(f"{premise} ---> {consequence}, conf = {conf}, lift = {measure}, sup = {item.sup}")
            else:
                i -= 1
                del H[i]           
        ap_genRules(item, H, T, minconf)
            
def genRules(F, T, minconf):
    for k_itemset in F[1:]:
        for item in k_itemset:
            H = []
            premises = findsubsets(item.itemset, len(item.itemset) - 1)
            consequences = [list(set(item.itemset).difference(premise))for premise in premises]
            for i in range(len(premises)):
                conf = confidence(item, premises[i], T)
                measure = lift(conf, consequences[i], T)
                if conf >= minconf and measure > 1:
                    print(f"{premises[i]} ---> {consequences[i]}, conf = {conf}, lift = {measure}, sup = {item.sup}")
                    H.append(Items(consequences[i], 0))
            ap_genRules(item, H, T, minconf)
                      
                



#F = Apriori(df6, 0.3)
#print(F)
#genRules(F, df7, 0.8)

