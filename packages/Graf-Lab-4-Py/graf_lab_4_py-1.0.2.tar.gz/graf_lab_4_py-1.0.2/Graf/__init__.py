from .Matrix.Incidence_matrix import *
from .Matrix.Adjacency_matrix import *
from .Matrix.Vis_matrix import *
from .Algorithm.euler import *
from .Algorithm.dijkstra import *
from .Algorithm.floyd_warshall import *

def Help():
    print('hello this is <name> lib')
    print('To test graf, write ')
    code = 'from Graf.floyd_warshall import * \n'
    code += 'test()'
    print('to see log of you test,call test True')