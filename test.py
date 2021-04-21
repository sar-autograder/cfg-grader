from pycfg.pycfg import PyCFG, CFGNode, slurp
from pycfg_ex import generate_cfg
from munkres import Munkres, print_matrix
from collapse_test import collapse

def create_cost_matrix(graph1,graph2):
	nodes1 = graph1.nodes()
	nodes2 = graph2.nodes()
	costMatrix = [[0 for col in range(len(nodes1) + len(nodes2))] for row in range(len(nodes1) + len(nodes2))]

	# Fill section 1 (real node to real node)
	for i in range(len(nodes1)):
		for j in range(len(nodes2)):
			in1 = len(graph1.in_neighbors(nodes1[i]))
			in2 = len(graph2.in_neighbors(nodes2[j]))
			out1 = len(graph1.out_neighbors(nodes1[i]))
			out2 = len(graph2.out_neighbors(nodes2[j]))
			costMatrix[i][j] = (out1 + out2 - (2 * min(out1,out2))) + (in1 + in2 - (2 * min(in1,in2)))

	# Fill section 2 (delete node in graph 1)
	for i in range(len(nodes1)):
		for j in range(len(nodes1)):
			if(i == j):
				oe = len(graph1.out_edges(nodes1[i]))
				ie = len(graph1.in_edges(nodes1[i]))
				costMatrix[i][len(nodes2)+j] = 1 + oe + ie
			else:
				costMatrix[i][len(nodes2)+j] = 999

	# Fill section 3 (delete node in graph 2)
	for i in range(len(nodes2)):
		for j in range(len(nodes2)):
			if(i == j):
				oe = len(graph2.out_edges(nodes2[i]))
				ie = len(graph2.in_edges(nodes2[i]))
				costMatrix[len(nodes1)+i][j] = 1 + oe + ie
			else:
				costMatrix[len(nodes1)+i][j] = 999

	return costMatrix

def compare(g1, g2):
	# filename = 'segiempat104.py'
	# filename2 = 'segiempat105.py'
	# g1 = generate_cfg(filename)
	# g2 = generate_cfg(filename2)
	# g1 = collapse(generate_cfg(filename))
	# g2 = collapse(generate_cfg(filename2))
	# print('g1 = ',g1)
	# print('g2 = ',g2)
	# g1.draw(filename + '.png', prog ='dot')
	# g2.draw(filename2 + '.png', prog ='dot') 
	m = Munkres()
	costMatrix = create_cost_matrix(g1,g2)
	# print(costMatrix)
	indexes = m.compute(costMatrix)
	# print_matrix(costMatrix, msg='Lowest cost through this matrix:')
	total = 0
	details = []
	for row, column in indexes:
		value = costMatrix[row][column]
		total += value
		# print(f'({row}, {column}) -> {value}')
		details.append([row, column, value])
	# print(f'total cost: {total}')

	final_score = (1 - (total / (len(g1.nodes()) + len(g2.nodes()) + len(g1.edges()) +len(g2.edges())))) * 100
	# print('Final score = ',final_score)
	return final_score, total, details

# compare()