from itertools import combinations as subset
from collections import defaultdict
import time

def trans_red(D, L_k):
    D1=[]
    for trans in D:
        for itemset in L_k:
            if set(itemset)<=trans:
                D1.append(trans)
                break
    return D1

def find_frequent_1_itemsets_hash(dataset, MINSUP):
    d = defaultdict(lambda: 0)
    hash_function = defaultdict(lambda: 0)
    L=[]
    F=[]
    hashset = []

    for t in dataset:
        ss = (subset(t, 2))
        for s in ss:
            hash_function[tuple(sorted(list(s)))]+=1
        for i in t:
            d[i] = d[i] + 1
    
    for i, v in d.items():
        if v<MINSUP:
            pass
        else:
            L.append([i])
            F.append(tuple([i]))
    
    for i, v in hash_function.items():
        if v<MINSUP:
            pass
        else:
            hashset.append(i)
    hashset=set(hashset)               
    return L, F, hashset

def get_subsets(C_k, t):
    C_t=[]
    for cand in C_k:
        if set(cand)<=t:
            C_t.append(tuple(cand))
    return C_t


def apriori_gen(L_k):
    C_k = []
    for l1 in L_k:
        for l2 in L_k:
            if l1[:-1] != l2[:-1]:
                pass
            else:
                if l1[-1] >= l2[-1]:
                    pass
                else:
                    c = l1 + [l2[-1]]

                    ssc=[]
                    ss = (subset(c, len(c)-1))
                    for s in ss:
                        ssc.append(sorted(list(s)))
                    infq_ss = False
                    for s in ssc: 
                        if s not in L_k:
                            infq_ss = True
                            break

                    if not infq_ss:
                        C_k.append(c)
    return C_k

# def has_infrequent_subset(c, L_k):
#     subc=[]
#     subsets = (subset(c, len(c)-1))
#     for sub in subsets:
#         subc.append(sorted(list(sub)))
#     for s in subc: 
#         if s not in L_k:
#             return True
#     return False




with open('BMS1_spmf.txt', 'r') as fname:
    data = fname.readlines()

MINIMUM_SUP = 0.01
MINSUP = int(MINIMUM_SUP*len(D))

D = [line[:-7].split(' -1 ') for line in data]

print()

for i in range(len(D)):
    for j in range(len(D[i])):
        D[i][j] = int(D[i][j])
    D[i]=set(D[i])



def basic_apriori():
    print("Running Basic Apriori")
    stime = time.time()
    d = defaultdict(lambda: 0)
    L_k=[]
    F=[]
    for t in D:
        for i in t:
            d[i] = d[i] + 1
    
    for i, v in d.items():
        if v<=MINSUP:
            pass
        else:
            L_k.append([i])
            F.append(tuple([i]))

    while True:
        count = defaultdict(lambda: 0)
        C_k = apriori_gen(L_k)
        for t in D:
            C_sub = get_subsets(C_k, t)
            for c in C_sub:
                count[c] = count[c] + 1
        L_k=[]
        for i, v in count.items():
            if v<MINSUP:
                pass
            else:
                L_k.append(list(i))
                F.append(i)
        if not L_k:
            break
    etime = time.time()
    print("Frequent ItemSets for Basic Apriori :")
    print(F)
    print(f"Time taken : {etime-stime}")
    print()

def apriori_with_transaction_red():
    print("Running Apriori with Transaction Reduction")
    stime = time.time()
    
    D_new=D
    L_k=[]
    F=[]

    d = defaultdict(lambda: 0)
    for trans in D_new:
        for item in trans:
            d[item] = d[item] + 1
    
    for k, v in d.items():
        if v<MINSUP:
            pass
        else:
            L_k.append([k])
            F.append(tuple([k]))

    while True:
        D_new=trans_red(D_new, L_k)
        count = defaultdict(lambda: 0)
        C_k = apriori_gen(L_k)
        for t in D_new:
            C_t = get_subsets(C_k, t)
            for c in C_t:
                count[c] = count[c] + 1
        L_k=[]

        for i, v in count.items():
            if v<MINSUP:
                pass
            else:
                L_k.append(list(i))
                F.append(i)
        if not L_k:
            break

    etime = time.time()
    print("Frequent ItemSets for Apriori with Transaction Reduction")
    print(F)
    print(f"Time taken : {etime-stime}")
    print()


def apriori_with_hash_mapping():
    print("Running Apriori with Hash Mapping")
    stime = time.time()

    L_k, F, hashset= find_frequent_1_itemsets_hash(D, MINSUP)
    check=True
    while True:
        count = defaultdict(lambda: 0)
        C_k = apriori_gen(L_k)
        if not check:
            for t in D:
                C_t = get_subsets(C_k, t)
                for c in C_t:
                    count[c] = count[c] + 1
            L_k=[]
            for i, v in count.items():
                if v<MINSUP:
                    pass
                else:
                    L_k.append(list(i))
                    F.append(i)
        else:
            for c in C_k:
                if tuple(c) not in hashset:
                    pass
                else:
                    F.append(tuple(c))
            L_k = [ c for c in C_k if tuple(c) in hashset]
            check=False
            
        if not L_k:
            break

    etime = time.time()
    print("Frequent ItemSets for Apriori with Hash Mapping")
    print(F)
    print(f"Time taken : {etime-stime}")
    print()



def apriori_with_hash_mapping_and_trans_red():
    print("Running Apriori with Hash Mapping and Transaction Reduction")
    
    stime = time.time()

    D_new = D

    L_k, F, hs= find_frequent_1_itemsets_hash(D_new, MINSUP)
    
    check=True
    
    while True:

        count = defaultdict(lambda: 0)

        D_new = trans_red(D_new, L_k)
        
        C_k = apriori_gen(L_k)

        if not check:
            for t in D_new:
                C_t = get_subsets(C_k, t)
                for c in C_t:
                    count[c] = count[c] + 1
            L_k=[]
            for k, v in count.items():
                if v<MINSUP:
                    pass
                else:
                    L_k.append(list(k))
                    F.append(k)
        else:
            check = False
            for c in C_k:
                if tuple(c) not in hs:
                    pass
                else:
                    F.append(tuple(c))
            L_k = [ c for c in C_k if tuple(c) in hs]
            
        if not L_k:
            break

    etime = time.time()
    print("Frequent ItemSets for Apriori with Hash Mapping and Transaction Reduction")
    print(F)
    print(f"Time taken : {etime-stime}")
    print()

basic_apriori()
apriori_with_transaction_red()
apriori_with_hash_mapping()
apriori_with_hash_mapping_and_trans_red()


