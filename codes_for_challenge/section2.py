import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

print "Spanning graph / network...","\n"
def valid(n, i, j, kn, comb):
    """
    This method is used to validate wherther move is possible or not.
    There are 8 possible moves:
    comb:0 - (x,y) > (x+a, y+b)
    comb:1 - (x,y) > (x+a, y-b)
    comb:2 - (x,y) > (x-a, y+b)
    comb:3 - (x,y) > (x-a, y-b)
    comb:4 - (x,y) > (x+b, y+a)
    comb:5 - (x,y) > (x+b, y-a)
    comb:6 - (x,y) > (x-b, y+a)
    comb:7 - (x,y) > (x-b, y-a)
    """
    N = n-1
    f = {
            0: (lambda x,y,ab: (x+ab[0],y+ab[1])),
            1: (lambda x,y,ab: (x+ab[0],y-ab[1])),
            2: (lambda x,y,ab: (x-ab[0],y+ab[1])),
            3: (lambda x,y,ab: (x-ab[0],y-ab[1])),
            4: (lambda x,y,ab: (x+ab[1],y+ab[0])),
            5: (lambda x,y,ab: (x+ab[1],y-ab[0])),
            6: (lambda x,y,ab: (x-ab[1],y+ab[0])),
            7: (lambda x,y,ab: (x-ab[1],y-ab[0])),
        }
    xp,yp = f[comb](i,j,kn)
    if xp < 0 or yp < 0 or xp > N or yp > N: return False
    else: return (True, xp, yp)

def span_graph(n,kn,ij=(0,0)):
    """
    This method span a graph which describes the movement of knight(a,b) on an nXn grid.
    """
    w = 1
    G = nx.Graph()
    for i in range(ij[0],ij[0]+n):
        for j in range(ij[1],ij[1]+n):
            for _comb in range(8):
                _v = valid(n,i,j,kn,_comb)
                if _v:
                    a = "(%d,%d)"%(i,j)
                    b = "(%d,%d)"%(_v[1],_v[2])
                    G.add_edge(a, b, weight=w)
                    pass
                pass
            pass
        pass
    return G


# ==========================================================================
#  Estimate shortest path and number of moves for knight(a,b) on a nXn grid
# ==========================================================================
def estimate_shortest_moves(n,a,b,plot=False):
    G = span_graph(n=n,kn=(a,b))
    if plot:
        nx.draw(G)
        plt.show()
        pass
    moves = nx.shortest_path(G, "(0,0)", "(%d,%d)"%(n-1,n-1))
    print "Print sortest paths - knight(%d,%d)"%(a,b), moves, ":: number of moves - ", len(moves)-1, "\n\n\n"
    return moves

# ==================================================================
#  Estimate howmany knights cannot reach (n-1,n-1)
#  Estimate sum of the number of moves for the shortest paths
# ==================================================================
def estimate_total_moves_and_false_knights(n, debg=False):
    _false_knights = 0
    _total_moves = 0
    for _a in range(0,n):
        for _b in range(0,n):
            G = span_graph(n=n,kn=(_a,_b))
            if 0 < _a and _a <= _b: 
                try:
                    moves = nx.shortest_path(G, "(0,0)", "(%d,%d)"%(n-1,n-1))
                    if debg: print "Print sortest paths - knight(%d,%d)"%(_a,_b), moves, ":: number of moves - ", len(moves)-1,"\n"
                    _total_moves += len(moves)-1
                except:
                    if debg: print "Moves not possible - knight(%d,%d)"%(_a,_b),"\n"
                    _false_knights += 1
                    pass
                pass
            elif 0 == _a and _a <= _b:
                try:
                    moves = nx.shortest_path(G, "(0,0)", "(%d,%d)"%(n-1,n-1))
                    if debg: print "Print sortest paths - knight(%d,%d)"%(_a,_b), moves, ":: number of moves - ", len(moves)-1,"\n"
                    _total_moves += len(moves)-1
                except:                                                                                                                                        
                    if debg: print "Moves not possible - knight(%d,%d)"%(_a,_b),"\n"
                    pass
                pass
            else: pass
            pass
        pass
    print "The total false knights - %d"%_false_knights
    print "The sum of the number of moves for the shortest paths - %d"%_total_moves,"\n\n\n"
    return

estimate_shortest_moves(5,1,2,plot=True)
estimate_total_moves_and_false_knights(5)

estimate_shortest_moves(25,4,7,plot=True)
estimate_total_moves_and_false_knights(25)

estimate_shortest_moves(1000,13,23,plot=False)
#estimate_shortest_moves(10000,73,101,plot=False)
