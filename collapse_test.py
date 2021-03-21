def collapse(graph):
    new_graph = graph
    nodes = graph.nodes()
    processed = []
    for i in range(len(nodes)):
        curr_out_edges = graph.out_edges(nodes[i])
        if(len(curr_out_edges) == 1 and nodes[i] not in processed):
            processed.append(nodes[i])
            start_node = nodes[i]
            (_, next_node) = curr_out_edges[0]
            node = graph.get_node(nodes[i])
            label = node.attr['label']
            stop = False
            while(not stop):
