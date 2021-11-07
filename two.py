import numpy as np
from collections import defaultdict as dd
from itertools import combinations as subset
from tqdm import tqdm
import time


class t_node:
    def __init__(self,item,parent=None,count=0):
        self.item = item
        self.parent = parent
        self.count = count
        self.children = []
        self.vis = False

    def printnode():
        print(item)
        print(parent)
        print(count)
        print(children)

class l_node:
    def __init__(self, t_node, next=None):
        self.t_node = t_node
        self.next = next

    def printnode():
        self.t_node.printnode()

class link:
    def __init__(self):
        self.head = None

    def add(self,t_node):
        if self.head == None:
            self.head = l_node(t_node)
        else:
            tempNode = l_node(t_node,self.head.next)
            self.head.next = tempNode

    def printnode():
        self.head.printnode()

class pattern_base:
    def __init__(self, min_sup, top_down=False,pre_defined=[],top_level=True):
        self.transactions = []
        self.transactions_original = []
        self.tr_cnt = []
        self.tr_cnt_org = []
        self.pre_defined = pre_defined
        self.head = t_node(None)
        self.MINSUP = min_sup
        self.freqA = dd(int)
        self.top_down = top_down
        self.top_level = top_level

    def add(self,t,tc):
        self.transactions.append(t)
        self.transactions_original.append(t)
        self.tr_cnt.append(tc)
        self.tr_cnt_org.append(tc)
    
    # def gen_list_f1(self):
    #     self.freqA = dd(int)
    #     for i,t in enumerate(self.transactions_original):
    #         for item in t:
    #             self.freqA[item] += self.tr_cnt_org[i]
    #     self.freqA = {k: v for k, v in sorted(self.freqA.items(), key=lambda item: item[1], reverse=True)}

    # def filter_transactions(self):
    #     # self.gen_list_f1()

    #     self.freqA = dd(int)
    #     for i,t in enumerate(self.transactions_original):
    #         for item in t:
    #             self.freqA[item] += self.tr_cnt_org[i]
    #     self.freqA = {k: v for k, v in sorted(self.freqA.items(), key=lambda item: item[1], reverse=True)}


    #     self.transactions = []
    #     self.tr_cnt = []

    #     for i,t in enumerate(self.transactions_original):
    #         new_trans = []
    #         for item in t:
    #             if self.freqA[item] >= self.MINSUP:
    #                 new_trans.append(item)
    #         if len(new_trans) != 0:
    #             new_trans = sorted(new_trans, key=lambda x: self.freqA[x], reverse=True)
    #             self.transactions.append(new_trans)
    #             self.tr_cnt.append(self.tr_cnt_org[i])
    #     self.freqA = [[k,v] for k,v in self.freqA.items() if v>=self.MINSUP]
    #     if not self.top_down:
    #         self.freqA.reverse()
    #     self.headers = {k:link() for k,v in self.freqA}
    #     self.conditional_patterns = {k:pattern_base(self.MINSUP,self.top_down,[k]+self.pre_defined,False) for k,v in self.freqA}

    def get_next(self,current,item):
        for c in current.children:
            if c.item == item:
                return c
        tempNode = t_node(item,current)
        current.children.append(tempNode)
        self.headers[item].add(tempNode)
        return tempNode
    
    # def add_trans_to_tree(self,trans,count):
    #     current = self.head
    #     for item in trans:
    #         current = self.get_next(current,item)
    #         current.count += count


    def gen_fp_tree(self):
        # self.filter_transactions()


        #####################################

        self.freqA = dd(int)
        for i,t in enumerate(self.transactions_original):
            for item in t:
                self.freqA[item] += self.tr_cnt_org[i]
        self.freqA = {k: v for k, v in sorted(self.freqA.items(), key=lambda item: item[1], reverse=True)}


        self.transactions = []
        self.tr_cnt = []

        for i,t in enumerate(self.transactions_original):
            new_trans = []
            for item in t:
                if self.freqA[item] >= self.MINSUP:
                    new_trans.append(item)
            if len(new_trans) != 0:
                new_trans = sorted(new_trans, key=lambda x: self.freqA[x], reverse=True)
                self.transactions.append(new_trans)
                self.tr_cnt.append(self.tr_cnt_org[i])
        self.freqA = [[k,v] for k,v in self.freqA.items() if v>=self.MINSUP]
        if not self.top_down:
            self.freqA.reverse()
        self.headers = {k:link() for k,v in self.freqA}
        self.conditional_patterns = {k:pattern_base(self.MINSUP,self.top_down,[k]+self.pre_defined,False) for k,v in self.freqA}

        #####################################



        self.head = t_node(None)
        for i,trans in enumerate(self.transactions):
            # self.add_trans_to_tree(trans,self.tr_cnt[i])

            ##############################


            count = self.tr_cnt[i]
            current = self.head
            for item in trans:
                current = self.get_next(current,item)
                current.count += count



            ##############################

    def check_if_single_path(self):
        current = self.head
        while True:
            child_count = len(current.children)
            if child_count == 0: 
                return True
            if child_count > 1:
                return False
            current = current.children[0]

    # def single_path_results(self):
    #     results = []
    #     current = self.head
    #     path = []
    #     count = dd(int)
    #     while len(current.children) != 0:
    #         current = current.children[0]
    #         path.append(current.item)
    #         count[current.item] = current.count
    #     for size in range(1,len(path)+1):
    #         combination = subset(path,size)
    #         for comb in combination:
    #             comb_count = min([count[item] for item in comb])
    #             results.append((list(comb)+self.pre_defined,comb_count))
    #     return results
            

    def get_conditional_pattern(self,t_node):
        current = t_node.parent
        suffix = []
        while current.item is not None:
            suffix.append(current.item)
            current = current.parent
        suffix.reverse()
        return suffix

    def explore(self,t_node,ai, prefix=[]):
        child_count = 0

        prefix = prefix + [t_node.item]
        for child in t_node.children:
            child_count += child.count
            self.explore(child,ai,prefix)
        if t_node.count > child_count:
            self.conditional_patterns[ai].add(prefix,t_node.count - child_count)
    
    def get_conditional_pattern_top_down(self,t_node,ai):
        results = []
        for child in t_node.children:
            self.explore(child,ai)

    def mine_fq_itemsets(self):
        self.gen_fp_tree()
        if not self.head.children:
            return []    
        results = []
        if self.check_if_single_path():
            # return self.single_path_results()
            # results = []
            current = self.head
            p = []
            count = dd(int)
            while len(current.children) != 0:
                current = current.children[0]
                p.append(current.item)
                count[current.item] = current.count
            for size in range(1,len(p)+1):
                combination = subset(p,size)
                for comb in combination:
                    comb_count = min([count[item] for item in comb])
                    results.append((list(comb)+self.pre_defined,comb_count))
            return results
        else:
            it = self.freqA
            if self.top_level:
                it = tqdm(it)
            for ai,c in it:
                results.append(([ai]+self.pre_defined,c))
                lNode = self.headers[ai].head
                while lNode is not None:
                    t_node = lNode.t_node
                    if self.top_down == False:
                        trans = self.get_conditional_pattern(t_node)
                        if len(trans) == 0:
                            pass
                        else:
                            self.conditional_patterns[ai].add(trans,t_node.count)
                    else:
                        multiple_trans = self.get_conditional_pattern_top_down(t_node,ai)
                    lNode = lNode.next
                if self.conditional_patterns[ai].transactions:
                    results.extend(self.conditional_patterns[ai].mine_fq_itemsets())
        return results


with open('BMS1_spmf.txt', 'r') as f:
    D = f.readlines()

D = [line[:-7].split(' -1 ') for line in D]

D = [list(set(line)) for line in D]

l = len(D)


MINIMUM_SUP = 0.01
MINSUP = int(MINIMUM_SUP*l)



def basic_FP_growth():
    print("Running Basic FP Growth")
    start=time.time()

    initial_base = pattern_base(MINSUP)

    for t in D:
        t = list(set(t))
        initial_base.add(t,1)

    F = initial_base.mine_fq_itemsets()
    F = sorted(F,key=lambda x: (len(x[0]),x[1]))

    end=time.time()
    print("Frequent ItemSets for FP Growth with Top Down Projection")
    print(F)
    print("Total time taken : " + str(end-start) + "\n\n ------------------ \n\n")


def FP_growth_topDown_projection():
    print("Running FP Growth with top down projection")

    start = time.time()
    initial_base_topdown = pattern_base(MINSUP,True)

    for trans in D:
        initial_base_topdown.add(trans,1)

    F_topdown = initial_base_topdown.mine_fq_itemsets()
    F_topdown = sorted(F_topdown,key=lambda x: (len(x[0]),x[1]))

    end=time.time()
    print(" Frequent ItemSets for FP Growth with Top Down Projection")
    print(F_topdown)
    print("Total time taken : " + str(end-start) + "\n\n ------------------ \n\n")


basic_FP_growth()
FP_growth_topDown_projection()



