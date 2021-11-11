from itertools import combinations as subset
from collections import defaultdict
import time

def checkCond(x,y):
    if set(x) <= y:
        return True
    return False

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
        F=[]
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


def generateSubsets(C_k, t):
    C_temp=[]
    for c in C_k:
        if checkCond(c,t):
            C_temp.append(tuple(c))
    return C_temp


def generateApriori(L_k):
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


with open('BMS1_spmf.txt', 'r') as fname:
    data = fname.readlines()

MINIMUM_SUP = 0.01


D = [line[:-7].split(' -1 ') for line in data]

print()

l = len(D)

MINSUP = int(MINIMUM_SUP*l)

for i in range(l):
    l2 = len(D[i])
    for j in range(l2):
        v = D[i][j]
        D[i][j] = int(v)
    D[i]=set(D[i])



def basic_apriori():
    print(" ----- Running Basic Apriori ----- ")
    start = time.time()
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
        C_k = generateApriori(L_k)
        cnt = defaultdict(lambda: 0)
        L_k=[]
        for t in D:
            C_sub = generateSubsets(C_k, t)
            for c in C_sub:
                cnt[c] = cnt[c] + 1
        
        for i, v in cnt.items():
            if v<MINSUP:
                pass
            else:
                L_k.append(list(i))
                F.append(i)
        if not L_k:
            break
    end = time.time()
    print("Frequent ItemSets for Basic Apriori :")
    print('\n'.join(map(str, F)))
    print("\nTotal time taken : " + str(end-start) + "\n\n------------------ \n\n")

# def apriori_with_transaction_red():
#     print(" ----- Running Apriori with Transaction Reduction ----- ")
#     start = time.time()
    
#     D_new=D
#     L_k=[]
#     F=[]

#     d = defaultdict(lambda: 0)
#     for trans in D_new:
#         for item in trans:
#             d[item] = d[item] + 1
    
#     for k, v in d.items():
#         if v<MINSUP:
#             pass
#         else:
#             L_k.append([k])
#             F.append(tuple([k]))

#     while True:
#         D2 = D_new

#         D_temp=[]
#         for t in D2:
#             for i in L_k:
#                 if set(i) <= t:
#                     D_temp.append(t)
#                     break
#         D_new = D_temp

#         C_k = generateApriori(L_k)

#         cnt = defaultdict(lambda: 0)
        
#         for t in D_new:
#             C_t = generateSubsets(C_k, t)
#             for i in C_t:
#                 cnt[i] = cnt[i] + 1
#         L_k=[]

#         for i, v in cnt.items():
#             if v<MINSUP:
#                 pass
#             else:
#                 L_k.append(list(i))
#                 F.append(i)
#         if L_k:
#             pass
#         else:
#             break

#     end = time.time()
#     print("Frequent ItemSets for Apriori with Transaction Reduction")
#     print(F)
#     print("Total time taken : " + str(end-start) + "\n\n------------------ \n\n")


def apriori_with_hash_mapping():
    print(" ----- Running Apriori with Hash Mapping ----- ")
    check=True
    start = time.time()

    L_k, F, hashset= find_frequent_1_itemsets_hash(D, MINSUP)
    
    while True:
        
        C_k = generateApriori(L_k)
        cnt = defaultdict(lambda: 0)

        if not check:
            for t in D:
                C_t = generateSubsets(C_k, t)
                for c in C_t:
                    cnt[c] = cnt[c] + 1
            L_k=[]
            for i, v in cnt.items():
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

    end = time.time()
    print("Frequent ItemSets for Apriori with Hash Mapping:")
    print('\n'.join(map(str, F)))
    print("\nTotal time taken = " + str(end-start) + "\n\n------------------ \n\n")



# def apriori_with_hash_mapping_and_trans_red():
#     print(" ----- Running Apriori with Hash Mapping and Transaction Reduction ----- ")
#     check=True

#     start = time.time()

#     D_new = D
#     L_k, F, hs= find_frequent_1_itemsets_hash(D_new, MINSUP)
    
#     while True:
#         D2 = D_new
#         cnt = defaultdict(lambda: 0)

#         D_temp=[]
#         for t in D2:
#             for i in L_k:
#                 if set(i) <= t:
#                     D_temp.append(t)
#                     break
#         D_new = D_temp
        
#         C_k = generateApriori(L_k)

#         if not check:
#             for t in D_new:
#                 C_t = generateSubsets(C_k, t)
#                 for c in C_t:
#                     cnt[c] = cnt[c] + 1
#             L_k=[]
#             for k, v in cnt.items():
#                 if v<MINSUP:
#                     pass
#                 else:
#                     L_k.append(list(k))
#                     F.append(k)
#         else:
#             check = False
#             for c in C_k:
#                 if tuple(c) not in hs:
#                     pass
#                 else:
#                     F.append(tuple(c))
#             L_k = [ c for c in C_k if tuple(c) in hs]
            
#         if not L_k:
#             break

#     end = time.time()
#     print("Frequent ItemSets for Apriori with Hash Mapping and Transaction Reduction : ")
#     print(F)
#     print("Total time taken = " + str(end-start) + "\n\n------------------ \n\n")

basic_apriori()
# apriori_with_transaction_red()
apriori_with_hash_mapping()
# apriori_with_hash_mapping_and_trans_red()


