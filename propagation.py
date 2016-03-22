import random
import copy
theta = 0.8                            #theta 的值对结果影响很大！

with open('seed_output.txt','r') as f:                  #导入种子数据
    seed = []
    seed = f.readline().rstrip(',').split(',') 
#    print(seed)
mapping = {}
for i in range(len(seed)):
    mapping[seed[i]] = seed[i]                          #mapping is 'dict'
print('The mapped nodes are:',mapping)
print('------------------------------------------------')


class Graph(object):                                    #定义有向图 类
    def __init__(self,graph):
        self.node = graph[0]
        self.idegree = graph[1].split(',')
        self.odegree = graph[2].strip().split(',')
    def print_nd(self):
        print(self.node,self.idegree,self.odegree)


with open('lgraph.txt','r') as f:                       #导入左图数据并创建实例
    graph = []
    for line in f.readlines():
        graph.append(line.split(' '))
lnode = []
lidegree = []
lodegree = []
for i in range(len(graph)):       
    lgraph = Graph(graph[i])
    lnode.append(lgraph.node)
    lidegree.append(lgraph.idegree)
    lodegree.append(lgraph.odegree)
#print(lnode,lidegree)

with open('rgraph.txt','r') as f:                       #导入右图数据并创建实例
    graph = []
    for line in f.readlines():
        graph.append(line.split(' '))
rnode = []
ridegree = []
rodegree = []
for i in range(len(graph)):       
    rgraph = Graph(graph[i])
    rnode.append(rgraph.node)
    ridegree.append(rgraph.idegree)
    rodegree.append(rgraph.odegree)
#print(rnode,ridegree)


def Invert(mapping):
    inv_mapping = {value:key for key,value in mapping.items()}
    return inv_mapping     

def MatchScores(lnode,lidegree,lodegree,rnode,ridegree,rodegree,mapping,lnum):
    scores = [0 for i in range(len(rnode))]                                         # scores here is 'list'
    for n in range(len(rnode)):
        if rnode[n] not in Invert(mapping):
            #print('rnode[n]:',rnode[n],lidegree[lnum])
            for i in range(len(lidegree[lnum])):
                if lidegree[lnum][i] not in mapping:
                    continue
                rnbr = mapping[lidegree[lnum][i]]
                #print('rnbr:',rnbr)
                for j in range(len(rodegree[rnode.index(rnbr)])):
                    if rodegree[rnode.index(rnbr)][j] != rnode[n]:
                        continue
                    #print('j,rnode[n]',j,rnode[n])
                    scores[n] += 1/len(ridegree[n])**0.5
                    #print(n,scores[n])
            for i in range(len(lodegree[lnum])):
                if lodegree[lnum][i] not in mapping:
                    continue
                rnbr = mapping[lodegree[lnum][i]]
                #print('rnbr2:',rnbr)
                for j in range(len(ridegree[rnode.index(rnbr)])):
                    if ridegree[rnode.index(rnbr)][j] != rnode[n]:
                        continue
                    scores[n] += 1/len(rodegree[n])**0.5
                    #print('n,scores[n]:',n,scores[n])
    return scores

def Std_Dev(a):
    l = len(a)
    avg = sum(a)/l
    suma = 0
    for i in a: 
        suma += (i-avg)**2
    stddev = (suma/l)**0.5
    return stddev    
    
def Eccentricity(item):
    _item = copy.deepcopy(item)
    stddev = Std_Dev(_item)
    _item.sort()
    max1 = _item[-1]
    max2 = _item[-2]
    eccen = (max1 -max2) / stddev   
    #print('eccen:',eccen)
    return eccen
    
def PropagationStep(lnode,lidegree,lodegree,rnode,ridegree,rodegree,mapping):
    scores = {}
    _scores = {}
    for l_node in lnode:
        if l_node not in mapping:
            scores[l_node] = MatchScores(lnode,lidegree,lodegree,rnode,ridegree,rodegree,mapping,lnode.index(l_node))    #scores is 'dict' , scores[] is 'list'
            #print(l_node,scores[l_node])
            if Eccentricity(scores[l_node]) < theta:
                continue
            #print('满足eccen：',l_node,scores[l_node])
            r_node = rnode[scores[l_node].index(max(scores[l_node]))]
            #print('index & r_node:',scores[l_node].index(max(scores[l_node])),r_node)
            _scores[r_node] = MatchScores(rnode,ridegree,rodegree,lnode,lidegree,lodegree,Invert(mapping),rnode.index(r_node))
            if Eccentricity(_scores[r_node]) < theta:
                continue
            #print('满足eccen 2：',r_node,_scores[r_node])
            reverse_match = lnode[_scores[r_node].index(max(_scores[r_node]))]
            
            if reverse_match != l_node:
                continue
            mapping[l_node] = r_node        
            #print('r_node 2',r_node)

mapped_num = len(mapping)
#print('mapped_num******************:',mapped_num)
PropagationStep(lnode,lidegree,lodegree,rnode,ridegree,rodegree,mapping)
mapped_new = len(mapping)
#print('mapped_new&&&&&&&&&&&&&&&&&&:',mapped_new)
while mapped_num != mapped_new:
    print('**:',mapping)
    mapped_num = mapped_new
    PropagationStep(lnode,lidegree,lodegree,rnode,ridegree,rodegree,mapping)
    mapped_new = len(mapping)
print('------------------------------------------------')
print('The final mapping is :',mapping)    
    
    