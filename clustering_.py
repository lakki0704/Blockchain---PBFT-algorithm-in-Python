import random

class Blockchain:
    def __init__(self,n,f):
        self.n= n #total nodes
        self.f=f  #total faulty nodes
        self.value=0
        self.view=0
        self.seq=0
        self.req_log=[]
        self.pre_prepare_msg=[]
        self.prepare_msg=[]
        self.commit_msg=[]
        self.block =[]

    def request(self,value):
        self.seq=self.seq+1
        message = (self.seq,value)
        self.req_log.append(message)
        self.pre_prepare(self.seq,value)

    def pre_prepare(self,seq,value):
        message = (seq,value)
        self.pre_prepare_msg.append(message)
        self.prepare(seq,value)

    def prepare(self,seq,value):
        message =(seq,value)
        self.prepare_msg.append(message)
        if(len(self.prepare_msg)>(2*self.f+1)):
            self.commit(seq,value)
        # else:
        #     print(self.seq," Not enough prepare message received to update the value of the primary node \n")

    def commit(self,seq,value):
        message=(seq,value)
        self.commit_msg.append(message)
        self.execute(seq,value)

    def execute(self,seq,value):
        id = (seq+2)**8+9/12 # a random formula for generating an ID
        block = (id,seq,value)
        if(len(self.commit_msg)> (2*self.f+1)):
            self.block.append(block)
            self.value=value
        # else:
        #     print(self.seq," Not enough ack received to commit the block into the blockchain\n")


class Clusters:
    def __init__(self,miners):
        self.groups=[]

    def grouping(self,miners):
        for i, e1 in enumerate(miners):
            z=self.check(e1)
            if z== False:
                self.groups.append([e1])
            else:
                self.groups.append([])
            for j, e2 in enumerate(miners[i+1:]):
                distance = self.euclidean(e1, e2)
                x= self.check(e2)
                if(x==False and distance<58):
                    self.groups[i].append(e2)
                    # print(self.groups)
                else:
                    continue

    def euclidean(self,e1,e2):
        x1,y1=e1
        x2,y2=e2
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    def check(self,y):
        x= False
        for i,e1 in enumerate(self.groups):
            for j,e2 in enumerate(self.groups[i][1:]):
                if(y==e2):
                    x= True

        return x

# miners= [(0, 0),(3, 4),(5, 12),(7, 24),(8, 5)]
miners = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(50)]
c= Clusters(miners)
c.grouping(miners)
print("total groups : ",c.groups)
final_group =[]
for i,e1 in enumerate(c.groups):
    if(len(c.groups[i])>1):
        final_group.append(e1)

print("Final group : \n", final_group)

total_nodes=0
for i,e in enumerate(final_group):
    for j,f in enumerate(final_group[i]):
       total_nodes+=1


cluster_count=0
faulty_nodes =0
block_msgs = 0
for i,e1 in enumerate(final_group):
    bl = Blockchain(len(final_group[i]),3) #considering 4 faulty nodes in each cluster
    faulty_nodes+=3
    for j,e2 in enumerate(final_group[i]):
        bl.request(23)
    print("Blockchain : ", bl.block)
    block_msgs+= len(bl.block)
    if len(bl.block)>=1:
        cluster_count+=1 #if the blockchain's array has some value then node count increases

print("Total nodes present = ",total_nodes)
print("Total faulty nodes present = ",faulty_nodes)
print("Total block messages = ", block_msgs)
print("Total clusters agreeing to update a new value = ", cluster_count)
print("Total number of clusters formed = ", len(final_group))
if cluster_count>(len(final_group)/2):
    print("Value updated")
else:
    print("Since enough nodes arent agreeing , value's not updated")