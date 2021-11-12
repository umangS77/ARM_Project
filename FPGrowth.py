from tqdm import tqdm
from collections import defaultdict as dd
from itertools import combinations as subset
import time
import numpy as np
import random
import math

class linked_NODE:
    def __init__(self):
        self.head = None

    def deleteNode(self):
        self.head = None

    def add(self,t_NODE):
        if self.head != None:
            newNode = l_NODE(t_NODE = t_NODE,next = self.head.next)
            self.head.next = newNode
        else:
            self.head = l_NODE(t_NODE = t_NODE, next = None)


class l_NODE:
    def __init__(self, t_NODE, next):
        self.t_NODE = t_NODE
        self.next = next

    def deleteNode(self):
        self.head = None

class t_NODE:
    def __init__(self,item,source=None,cnt=0):
        self.setParent(source)
        self.item = item
        self.offspring = []
        self.cnt = cnt

    def setParent(self,source):
        self.source = source

    def deleteNode(self):
        self.head = None

class patternBase:
    def __init__(self, minsupp, preDef=[],top_level=True):
        
        self.preDef = preDef
        self.trans = []
        
        self.head = t_NODE(None)
        self.trans_org = []
        
        self.minSUP = minsupp
        self.tr_cnt = []
        
        self.freqA = dd(int)
        self.tr_cnt_org = []

        self.top_level = top_level
    

    def checkSinglePath(self):
        cr = self.head
        while 1>0:
            cc = len(cr.offspring)
            if cc > 1:
                return False
            elif cc == 0: 
                return True
            
            cr = cr.offspring[0]

    


    def generateFPTree(self):
        self.freqA = dd(int)
        self.trans = []
        self.tr_cnt = []
        for i,tr in enumerate(self.trans_org):
            for j in tr:
                self.freqA[j] = self.freqA[j] + self.tr_cnt_org[i]

        newTrans = sorted(self.freqA.items(), key=lambda item: item[1], reverse=True)

        self.freqA = {ky:val for ky,val in newTrans}
        
        
        for i,tr in enumerate(self.trans_org):
            newTR = []
            for item in tr:
                if self.minSUP > self.freqA[item]:
                    pass
                else:
                    newTR.append(item)
            l = len(newTR) 
            if l == 0:
                pass 
            else:
                # newTR = sorted(newTR, key=lambda x: self.freqA[x], reverse=True)
                self.trans.append(sorted(newTR, key=lambda x: self.freqA[x], reverse=True))
                self.tr_cnt.append(self.tr_cnt_org[i])
                l = len(newTR)

        self.freqA = [[ky,val] for ky,val in self.freqA.items() if self.minSUP <= val]
        self.freqA.reverse()
        self.headers = {ky:linked_NODE() for ky,val in self.freqA}
        l = -1


        self.condPat = {ky:patternBase(self.minSUP,[ky]+self.preDef,False) for ky,val in self.freqA}
        self.head = t_NODE(None)
        for i,tr in enumerate(self.trans):
            c = self.tr_cnt[i]
            cr = self.head
            for i in tr:
                cr = self.generateNext(cr,i)
                cr.cnt = cr.cnt + c

    

    def ansSinglePath(self):
        way = []
        cr = self.head
        cnt = dd(int)
        l = len(cr.offspring)
        if l!=0:
            while 1>0:
                cr = cr.offspring[0]
                way.append(cr.item)
                cnt[cr.item] = cr.cnt
                l = len(cr.offspring)

                if l==0:
                    break
        
        ans = []

        for sz in range(1,len(way)+1):
            c1 = subset(way,sz)
            for c2 in c1:
                ans.append((list(c2)+self.preDef,min([cnt[i] for i in c2])))
        return ans

    def explore(self,t_NODE, it, pf=[]):
        
        pf = pf + [t_NODE.item]
        cc = 0
        for c in t_NODE.offspring:
            cc = cc + c.cnt
            self.explore(c,it,pf)
        if t_NODE.cnt > cc:
            pass 
        else:
            self.condPat[it].add(pf,t_NODE.cnt - cc)

    def mineFrequentItemsets(self):
        self.generateFPTree()
        ans = []
        if not self.head.offspring:
            return ans
        if self.checkSinglePath() == False:
            itr = []
            if self.top_level:
                temp = self.freqA
                itr = tqdm(temp)
            else:
                itr = self.freqA
            for it, cnt in itr:
                v = [it]+self.preDef
                ans.append((v,cnt))
                LNode = self.headers[it].head
                if LNode == None:
                    pass
                else:
                    while 1>0:
                        t_NODE = LNode.t_NODE
                        sf = []
                        cr = t_NODE.source
                        
                        while cr.item is not None:
                            sf.append(cr.item)

                            cr = cr.source
                        sf.reverse()
                        tr = sf
                        l = len(tr)

                        if l == 0:
                            pass
                        else:
                            self.condPat[it].add(tr,t_NODE.cnt)
                        LNode = LNode.next
                        if LNode == None:
                            break
                if self.condPat[it].trans:
                    ans.extend(self.condPat[it].mineFrequentItemsets())
        else:
            return self.ansSinglePath()
        return ans

    def generateNext(self,cr,item):
        
        for c in cr.offspring:
            if c.item != item:
                pass
            else:
                return c

        newNode = t_NODE(item = item, source = cr)
        cr.offspring.append(newNode)
        self.headers[item].add(newNode)
        return newNode

    def add(self,tr,tc):
        self.trans_org.append(tr)
        self.trans.append(tr)
        self.addCount(tc)

    def addCount(self,tc):
        self.tr_cnt.append(tc)
        self.tr_cnt_org.append(tc)





def basicFPGrowth():
    with open('BMS1_spmf.txt', 'r') as file:
        D = file.readlines()
    D = [l[:-7].split(' -1 ') for l in D]
    D = [list(set(l)) for l in D]

    ln = len(D)

    MINSUPPORT = int(0.01*ln)


    print(" ----- Running Basic FP Growth ----- ")
    start=time.time()
    base = patternBase(MINSUPPORT)
    for tr in D:
        base.add(list(set(tr)),1)

    output = sorted(base.mineFrequentItemsets(),key=lambda x: (len(x[0]),x[1]))
    end=time.time()
    print("Frequent ItemSets for FP Growth :")
    print('\n'.join(map(str, output)))
    print("\nTotal time taken for FP Growth= " + str(end-start) + "\n\n------------------ \n\n")

basicFPGrowth()