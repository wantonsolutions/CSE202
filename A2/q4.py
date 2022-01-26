import igraph as ig
import random

## Generate graph with 8 vertices and no edges
g = ig.Graph.GRG(100,0.2)
for e in g.es:
    e["weight"]=random.randint(1,50)
    e["color"]="black"

start = g.vs[0]
start["color"]="green"
end = g.vs[len(g.vs)-1]
end["color"]="blue"

#how to color an edge
#g.es[25]["color"]="blue"

print(start)
print(end)



## random walk path

current=start
path=[]
frontier=[]
frontier.append(current)
i=0
while current != end:
    edges = current.all_edges()
    for e in edges:
        #place more verticies on the queue
        if e["color"] != "green":
            if g.vs[e.tuple[0]] != current:
                frontier.append(g.vs[e.tuple[0]])
            else:
                frontier.append(g.vs[e.tuple[1]])
            e["color"]="green"
            e["width"]=3
    current=frontier.pop()
    i=i+1
    output="%03d" % i
    ig.plot(g,output+".png")


