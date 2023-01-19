# easy_Mason
an easy python tool to calculate transfer function by Mason formula 
# Usage
## Create a signal graph
```c
G = signal_graph(9) #create a signal with 9 nodes
```
## Add transfer functions
```c
G.add_edge(1, 2, 1) # add a transfer function from node 1 to node 2, which f=1
G.add_edge(2, 3, Symbol("G1"))# add a transfer function from node 2 to node 3, which f=G1 (use sympy Symbol object)
G.add_edge(3, 4, Symbol("G2"))
G.add_edge(4, 5, Symbol("G3"))
G.add_edge(5, 6, Symbol("G4"))
G.add_edge(6, 7, Symbol("G5"))
G.add_edge(7, 8, Symbol("G6"))
G.add_edge(8, 9, 1)
G.add_edge(2, 4, Symbol("G7"))
G.add_edge(3, 7, Symbol("G8"))
G.add_edge(4, 3, -Symbol("H1"))
G.add_edge(7, 4, -Symbol("H4"))
G.add_edge(6, 5, -Symbol("H2"))
G.add_edge(8, 7, -Symbol("H3"))
G.add_edge(8, 2, -Symbol("H5"))
```
## Calculate result
```c
G.get_transfer_function(1, 9) #get transfer function H=N9/N1
print(G.transfer_func)
```
output:
```c
added transfer function 1 from 1 to 2
added transfer function G1 from 2 to 3
added transfer function G2 from 3 to 4
added transfer function G3 from 4 to 5
added transfer function G4 from 5 to 6
added transfer function G5 from 6 to 7
added transfer function G6 from 7 to 8
added transfer function 1 from 8 to 9
added transfer function G7 from 2 to 4
added transfer function G8 from 3 to 7
added transfer function -H1 from 4 to 3
added transfer function -H4 from 7 to 4
added transfer function -H2 from 6 to 5
added transfer function -H3 from 8 to 7
added transfer function -H5 from 8 to 2
(G1*G2*G3*G4*G5*G6 + G1*G4*G6*G8*H2 + G3*G4*G5*G6*G7 - G4*G6*G7*G8*H1*H2)/(G1*G2*G3*G4*G5*G6*H5 + G1*G4*G6*G8*H2*H5 + G1*G6*G8*H5 + G2*G4*G6*H1*H2*H3 + G2*G4*H1*H2 + G2*G6*H1*H3 + G2*H1 + G3*G4*G5*G6*G7*H5 + G3*G4*G5*H4 - G4*G6*G7*G8*H1*H2*H5 + G4*G6*H2*H3 - G4*G8*H1*H2*H4 + G4*H2 - G6*G7*G8*H1*H5 + G6*H3 - G8*H1*H4 - 1)

```
