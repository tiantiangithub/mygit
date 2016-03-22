import random
import copy

with open('test.txt','r') as f:                  #导入数据
    graph = []
    for line in f.readlines():
	    graph.append(line.strip().split(','))
#    print(graph)
#    print(len(graph))
#    print(graph[0])
#    print(graph[0][0])



class Graph(object):                             #定义无向图 类
    def __init__(self,graph_):
        self.node = graph_[0]
        self.nbr = graph_[1:len(graph_)] 
    def print_nd(self):
        print(self.node,self.nbr)

'''
class Graph(object):                             #定义有向图 类
    def __init__(self,graph_):
        self.node = graph_[0]
        self.idegree = graph_[1]
        self.odegree = graph_[2:len(graph_)]
    def print_nd(self):
        print(self.node,self.idegree,self.odegree)
''' 
     
lnode = []                                        #产生实例化的网络图
lnbr = []
for i in range(len(graph)):       
    lgraph = Graph(graph[i])
    lnode.append(lgraph.node)
    lnbr.append(lgraph.nbr)
#print(lnode)
#print(lnbr)


with open('seed_input.txt','r') as f:            #选种子
    SEED_NUM = int(f.readline())
    SEED_DEGREE = list(f.readline().strip().split(','))
    SEED_COMNBR = list(f.readline().strip().split(','))
    ERROR = float(f.readline())
#print(SEED_DEGREE)

seed_dcan = [[] for i in range(SEED_NUM)]                                     
for i in range(SEED_NUM):
    for j in range(len(lnbr)):
        if len(lnbr[j]) == int(SEED_DEGREE[i]):
            seed_dcan[i].append(lnode[j])
print('筛选度之后：',seed_dcan)
print('---------------------------------------')

seed = [[] for i in range(SEED_NUM)]
seed_can = [[] for i in range(SEED_NUM-1)]
m = 0
_seed_dcan = copy.deepcopy (seed_dcan)
_SEED_COMNBR = copy.deepcopy (SEED_COMNBR)
_seed_dcan.insert(0,[])
while len(_seed_dcan) > 2:
    del _seed_dcan[0]
#    print('second:',_seed_dcan,len(_seed_dcan))
    for p in range(len(_seed_dcan[0])):
        for q in range(len(_seed_dcan[1])):
            if len(set(lnbr[lnode.index(_seed_dcan[0][p])]) & set(lnbr[lnode.index(_seed_dcan[1][q])])) == int(_SEED_COMNBR[0]):
                seed_can[m].append([_seed_dcan[0][p],_seed_dcan[1][q]])
    del _SEED_COMNBR[0]
#    print(m,seed_can[m])
    if len(_seed_dcan) > 2:
        for n in range(2,len(_seed_dcan)):
            for p in range(len(_seed_dcan[0])):
                for q in range(len(_seed_dcan[n])):
                    if len(set(lnbr[lnode.index(_seed_dcan[0][p])]) & set(lnbr[lnode.index(_seed_dcan[n][q])])) == int(_SEED_COMNBR[0]):
                        if _seed_dcan[0][p] in sum(seed_can[m],[])[::2]:
                            seed_can[m].append([_seed_dcan[0][p],_seed_dcan[n][q]])
                            
            del _SEED_COMNBR[0]            
#    print(m,seed_can[m])
    if m == 0:
        seed[m] = list(set(sum(seed_can[m],[])[::2]))
#        print(seed[m])
    elif m >= 1:
        seed[m] = list(set(sum(seed_can[m],[])[::2]) & set(sum(seed_can[0],[])[1::2]))
    if m == SEED_NUM-2:
        for i in range(len(list(set(sum(seed_can[m],[])[1::2])))):
            if list(set(sum(seed_can[m],[])[1::2]))[i] in sum(seed_can[0],[])[1::2]:
                seed[m+1].append(list(set(sum(seed_can[m],[])[1::2]))[i])
    m = m + 1
print('第一次过滤：',seed)
print('---------------------------------------')

n = 0
final_seed = []    
seed_const = random.choice(seed[0])
final_seed.append(seed_const)    
for m in range(len(seed)-1):    
    seed_ran = random.choice(seed[m+1])
    while n < m+1:
        if [final_seed[n],seed_ran] not in seed_can[n]:
            seed_ran = random.choice(seed[m+1])
#            print(seed_ran)
            n = 0
            continue
        n = n + 1
    seed_const = seed_ran
    final_seed.append(seed_const)
#    print(seed_const)
if len(set(final_seed)) != SEED_NUM:
    print('run the process again:')
else:
    print('最后过滤后：',final_seed)
    wseed = ''
    for i in range(len(final_seed)):
        wseed = wseed + final_seed[i] + ','
    with open('seed_output.txt','w') as f:
        f.write(wseed)


    
    
    