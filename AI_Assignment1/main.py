import sys

from collections import defaultdict


def uniform_search(Graph, Start, End):
    path = []  # path to keep track
    explored = []  # explored node
    path.append(Start)  # append first node to the path aka starting node
    frontier = [(path, str(0.0))]  # add the path and path cost to fringe
    # while frontier isn't empty
    node_generated = 1
    node_expanded = 0
    nopath = False
    fringe = [[Start, '0.0']]
    while frontier:
        fringe.pop(0)
        current_path, current_cost = frontier.pop(0)  # pop the current path and frontier
        current_node = current_path[-1]  # get the last node in the path aka current node
        # if current node is equal to goal return the path and cost
        if current_node == End:
            node_expanded += 1
            print("Nodes expanded: " + str(node_expanded))
            print("Nodes generated: " + str(node_generated))
            print("Distance: " + current_cost + " km")
            print("route:")
            index = 0
            while index < len(current_path) - 1:
                for items in Graph[current_path[index]]:
                    if items[0] == current_path[index + 1]:
                        print(current_path[index] + " to " + current_path[index + 1] + " : " + items[1] + ' km.')
                index += 1
            return current_path
        # if current node is already explored skip
        # if not explored for each neighbour in Graph calculate the path and cost to fringe
        if current_node not in explored:
            for neighbour in Graph[current_node]:
                # if neighbour[0] not in explored:
                new_path = current_path.copy()  # copy the existing path
                new_path.append(neighbour[0])  # add new node to the path
                new_path_cost = (float(neighbour[1]) + float(current_cost))  # add total cost of the path
                frontier.append([new_path, str(new_path_cost)])  # add the new path and cost to fringe
                fringe.append([neighbour[0],str(new_path_cost)])
                node_generated += 1  # note_generated
            node_expanded += 1  # add note expanded
        else:
            node_expanded += 1

        frontier.sort(key=lambda x: float(x[1]))  # sort the fringe according to the value of cost
        fringe.sort(key=lambda x: float(x[1]))
        explored.append(current_node)  # add new node to explored/expanded list

    nopath = True
    if nopath:
        print("Nodes expanded: " + str(node_expanded))
        print("Nodes generated: " + str(node_generated))
        print("Distance: infinity")
        print('route: \nNone')


def informed_search(Graph, Start, End, heuristic):
    path = []  # path to keep track
    explored = []  # explored node
    path.append(Start)  # append first node to the path aka starting node
    frontier = [(path, str(0.0), str(heuristic[Start]))]  # add the path and path cost to fringe
    # while frontier isn't empty
    node_generated = 1
    node_expanded = 0
    nopath = False
    fringe = [[Start, '0.0', str(heuristic[Start])]]
    while frontier:
        fringe.pop(0)
        current_path, current_cost, current_hvalue = frontier.pop(0)  # pop the current path and frontier
        current_node = current_path[-1]  # get the last node in the path aka current node
        # if current node is equal to goal return the path and cost
        if current_node == End:
            node_expanded += 1
            print("Nodes expanded: " + str(node_expanded))
            print("Nodes generated: " + str(node_generated))
            print("Distance: " + current_cost + " km")
            print("route:")
            index = 0
            while index < len(current_path) - 1:
                for items in Graph[current_path[index]]:
                    if items[0] == current_path[index + 1]:
                        print(current_path[index] + " to " + current_path[index + 1] + " : " + items[1] + ' km.')
                index += 1
            return current_path
        # if current node is already explored skip
        # if not explored for each neighbour in Graph calculate the path and cost to fringe
        if current_node not in explored:
            for neighbour in Graph[current_node]:
                # if neighbour[0] not in explored:
                new_path = current_path.copy()  # copy the existing path
                new_path.append(neighbour[0])  # add new node to the path
                new_path_cost = float(neighbour[1]) + float(current_cost)  # add total cost of the path
                new_hvalue_cost = new_path_cost + float(heuristic[neighbour[0]])
                frontier.append(
                    [new_path, str(new_path_cost), str(new_hvalue_cost)])  # add the new path and cost to fringe
                fringe.append([neighbour[0], str(new_path_cost), str(new_hvalue_cost)])
                node_generated += 1  # note_generated
            node_expanded += 1  # add note expanded
        else:
            node_expanded += 1

        frontier.sort(key=lambda x: float(x[2]))  # sort the fringe according to the value of cost
        fringe.sort(key=lambda x: float(x[2]))
        explored.append(current_node)  # add new node to explored/expanded list

    nopath = True
    if nopath:
        print("Nodes expanded: " + str(node_expanded))
        print("Nodes generated: " + str(node_generated))
        print("Distance: infinity")
        print('route: \nNone')


def generate_graph(inputfile):
    edges = []
    # graph = {}
    graph = defaultdict(list)
    fp = open(inputfile, 'r')
    for line in fp:
        line = line.strip('\n')
        if line == 'END OF INPUT':
            return graph
        else:
            data = line.split()
            edges.append(data)
            graph[data[0]].append([data[1], data[2]])
            graph[data[1]].append([data[0], data[2]])


def heuristic(filename):
    hvalue = {}
    fp = open(filename, 'r')
    for line in fp:
        line = line.strip('\n')
        if line == 'END OF INPUT':
            return hvalue
        else:
            data = line.split()
            hvalue[data[0]] = float(data[1])


def main():
    try:
        fname = sys.argv[1]
        source = sys.argv[2]
        destination = sys.argv[3]
        graph = generate_graph(fname)
        if len(sys.argv) == 5:
            hname = sys.argv[4]
            hvalue = heuristic(hname)
            informed_search(graph, source, destination, hvalue)
        else:
            uniform_search(graph, source, destination)

    except Exception as e:
        print(e)
    uniform_search(graph, 'A', 'G')



if __name__ == '__main__':
    main()
