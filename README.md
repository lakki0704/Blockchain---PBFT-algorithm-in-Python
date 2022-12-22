# Blockchain---PBFT-algorithm-in-Python
Implementation of PBFT in python.
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

This is a very basic implementation of PBFT. In practical applications, complex hasing methods are involved for privacy purposes and to hinder faulty nodes from breaking the blockchain
