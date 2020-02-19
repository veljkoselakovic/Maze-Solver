from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import time

ime = input()
im = Image.open(ime+".bmp")

sirina = im.size[0]
visina = im.size[1]
print(sirina)
G = nx.Graph()


def nadji_cvor(atr, vr):
    return any([node for node in G.nodes(data=True) if node[1][atr] == vr])


pixeli = list(im.getdata(0))
n = sirina
final = [pixeli[i * n:(i + 1) * n] for i in range((len(pixeli) + n - 1) // n)]

for x in range(1, sirina - 1):

    if final[0][x] == 0:
        G.add_node(0, pos=(x, 0), num=0)
        break

k = 1
pos = {}

last_node_k_y = 0
last_node_k_x = [0] * visina
print(last_node_k_x[0])
last_zid_y = 0
last_zid_x = [0] * visina
prekraja = 0
oznaka = 0
for y in range(1, visina - 1):
    for x in range(1, sirina - 1):
        if final[x][y] == 0:
            if x == visina - 2:
                if final[x + 1][y] == 0:
                    oznaka = k
            if x == 1:
                if final[x - 1][y] == 0:
                    oznaka_ = k

            sum = final[x + 1][y] + final[x][y + 1] + final[x - 1][y] + final[x][y - 1]
            if sum == 2:
                if final[x + 1][y] + final[x - 1][y] == 2:
                    pass
                elif final[x][y + 1] + final[x][y - 1] == 2:
                    pass
                else:
                    sum += 1
            if sum < 2 or sum == 3:
                G.add_node(k, pos=(y, x), num=k)
                if G.node[last_node_k_y]['pos'][0] == y and last_zid_y < G.node[last_node_k_y]['pos'][1]:
                    G.add_edge(last_node_k_y, k)
                if G.node[last_node_k_x[x]]['pos'][1] == x and last_zid_x[x] < G.node[last_node_k_x[x]]['pos'][0]:
                    G.add_edge(last_node_k_x[x], k)

                last_node_k_x[x] = k
                last_node_k_y = k
                k += 1


        else:
            last_zid_y = x
            last_zid_x[x] = y

    last_zid_y = 0
for x in range(1, sirina - 1):

    if final[visina - 1][x] == 0:
        G.add_node(k, pos=(x, visina - 1), num=k)
        break

G.add_edge(0, oznaka_)
G.add_edge(oznaka, k)

# print(G.nodes())
pos = nx.get_node_attributes(G, 'pos')

# print(pos)
img = plt.imread(ime+".bmp")
fig, ax = plt.subplots()
ax.imshow(img)


def split_(lis):
    ret = []
    for i in range(0, len(lis)-1):
        ret.append((lis[i], lis[i+1]))
    return ret


def nodes_connected(u, v):
    return u in G.neighbors(v)



#nx.draw_networkx_nodes(G, pos, node_color='black', node_size=5)
start_dijkstra = time.time()
red = (split_(nx.dijkstra_path(G, source=0, target=k)))
end_dijkstra = time.time()
print("Dijkstra: " + str(end_dijkstra - start_dijkstra))


nx.draw_networkx_edges(G, pos, edgelist=red, edge_color='r', alpha=0.5, width=5)

#nx.draw_networkx_edges(G, pos, edge_color='black')
#nx.draw_networkx_labels(G, pos, font_color='white')
plt.savefig(ime+"reseno" + '.png')

plt.show()
