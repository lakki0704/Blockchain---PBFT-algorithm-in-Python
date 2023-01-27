import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


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
                if(x==False and distance<10):
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



X=[]
Y=[]
for i in range(0,2000):
    miners = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(50)]
    c = Clusters(miners)
    c.grouping(miners)
    final_group = []
    for i, e1 in enumerate(c.groups):
        if (len(c.groups[i]) > 1):
            final_group.append(e1)
    cluster_count = 0
    block_msgs = 0
    for i, e1 in enumerate(final_group):
        bl = Blockchain(len(final_group[i]),random.randint(0,2))  # considering some faulty nodes in each cluster
        for j, e2 in enumerate(final_group[i]):
            bl.request(23)

        block_msgs += len(bl.block)
        if len(bl.block) >= 1:
            cluster_count += 1
    if cluster_count > (len(final_group) / 2):
        X.append(len(final_group))
        Y.append(block_msgs)

# print(X)
X = np.array(X)
X= X.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)


# Train a linear regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Use the model to predict the number of commits for different numbers of clusters on the testing data
y_pred = model.predict(X_test)

# Select the number of clusters that results in the lowest number of commits, according to the predictions of the model
optimal_clusters = X_test[np.argmin(y_pred)]
print(f"The optimal number of clusters is {optimal_clusters}.")
