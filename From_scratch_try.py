
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
        if(len(self.prepare_msg)>(self.n -self.f)):
            self.commit(seq,value)
        else:
            print(self.seq," Not enough prepare message received to update the value of the primary node \n")

    def commit(self,seq,value):
        message=(seq,value)
        self.commit_msg.append(message)
        self.execute(seq,value)

    def execute(self,seq,value):
        id = (seq+2)**8+9/12
        block = (id,seq,value)
        if(len(self.commit_msg)> (self.n- self.f)):
            self.block.append(block)
            self.value=value
        else:
            print(self.seq," Not enough ack received to commit the block into the blockchain\n")



pbft = Blockchain(5,3)
pbft.request(23)
pbft.request(43)
pbft.request(83)
pbft.request(73)
pbft.request(48)
pbft.request(43)

print("request messages : ", pbft.req_log)
print("Prepare messages : ", pbft.prepare_msg)
print("Blockchain : ", pbft.block)


"""

1.A client sends a request to propose a new value to the network.

2.The primary node, which is responsible for coordinating the consensus process, sends a pre-prepare message containing 
the proposed value to all other nodes in the network.

3.Each node that receives the pre-prepare message sends a prepare message back to the primary node to acknowledge 
receipt of the pre-prepare message.

4.If the primary node receives enough prepare messages (at least n - f where n is the total number of nodes in the 
network and f is the maximum number of faulty nodes), it sends a commit message to all other nodes.

5.Each node that receives the commit message sends an acknowledgement (ACK) message back to the primary node.

6.If the primary node receives enough ACK messages (at least n - f), it considers the value to be committed and 
updates its own copy of the distributed ledger. It then sends a reply to the client to confirm that the value has 
been committed.

"""