import sys
import os


# complete the graph by adding in reverse of each edges
def complete_graph(nodes, init_graph):
    graph = {}
    for node in nodes:
        graph[node] = {}

    graph.update(init_graph)

    for node, out_edges in graph.items():
        for neighbor, distance in out_edges.items():
            if graph[neighbor].get(node, False) == False:
                graph[neighbor][node] = distance

    return graph


def complete_turn(nodes, turn):
    temp_turn = {}
    for node in nodes:
        temp_turn[node] = {}

    temp_turn.update(turn)

    for start, junctions in temp_turn.items():
        for junction, ends in junctions.items():
            for end, direct in ends.items():
                if temp_turn[end][junction].get(start, False) == False:
                    temp_turn[end][junction][start] = -direct

    return temp_turn


class Graph(object):
    def __init__(self, nodes, junctions, graph, turn):
        self.nodes = nodes
        self.junctions = junctions
        self.graph = graph
        self.turn = turn

    def get_all_nodes(self):
        all_nodes = list(self.nodes)

        return all_nodes

    def get_all_junc(self):
        all_junc = list(self.junctions)

        return  all_junc

    def get_direction(self, prvs, curr, next):
        return self.turn[prvs][curr][next]

    def get_all_out_edges(self, curr_node):
        out_edges = []

        for node in self.nodes:
            if self.graph[curr_node].get(node, False) != False:
                out_edges.append(node)

        return out_edges

    def distance(self, start, end):
        return self.graph[start][end]


def get_shortest(graph, start):
    unvisited_nodes = list(graph.get_all_nodes())

    shortest_path = {}
    prvs_node = {}

    max_dist = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_dist

    shortest_path[start] = 0

    while unvisited_nodes:
        min_node = None
        for node in unvisited_nodes:
            if min_node == None:
                min_node = node
            elif shortest_path[node] < shortest_path[min_node]:
                min_node = node

        neighbors = graph.get_all_out_edges(min_node)
        for neighbor in neighbors:
            curr_dist = shortest_path[min_node] + graph.distance(min_node, neighbor)
            if curr_dist < shortest_path[neighbor]:
                shortest_path[neighbor] = curr_dist
                prvs_node[neighbor] = min_node

        unvisited_nodes.remove(min_node)

    return prvs_node, shortest_path


def print_result(graph, prvs_node, shortest_path, start, end):
    path = []
    node = end

    while node != start:
        path.append(node)
        node = prvs_node[node]

    path.append(start)

    print("We found the following best path with a value of {}.".format(shortest_path[end]))
    true_path = list(reversed(path))

    junctions = graph.get_all_junc()

    print(" -> ".join(reversed(path)))
    for prvs, curr, next in zip(true_path, true_path[1:], true_path[2:]):
        if curr in junctions:
            dir_value = graph.get_direction(prvs, curr, next)
            print("At {}, go {}".format(curr, direction[dir_value]))

    print("")


def main():
    nodes = ["Middle Entrance", "Stair Entrance and Room 119", "Auditorium Entrance", "Creamery Entrance", "Front Desk",
             "Auditorium", "Workshop", "Entertainment Rooms", "Room 115", "Junction A", "Junction B",
             "Junction C", "Junction D"]

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    # Entrance to junctions
    init_graph["Middle Entrance"]["Front Desk"] = 1
    init_graph["Creamery Entrance"]["Junction A"] = 1
    init_graph["Auditorium Entrance"]["Junction C"] = 1
    init_graph["Stair Entrance and Room 119"]["Junction D"] = 1
    init_graph["Entertainment Rooms"]["Workshop"] = 1

    init_graph["Front Desk"]["Junction D"] = 5

    init_graph["Junction A"]["Junction B"] = 1
    init_graph["Junction A"]["Junction D"] = 1
    init_graph["Junction A"]["Room 115"] = 1

    init_graph["Junction B"]["Junction C"] = 1
    init_graph["Junction B"]["Entertainment Rooms"] = 1

    init_graph["Junction C"]["Auditorium"] = 1

    init_graph["Junction D"]["Junction C"] = 1

    graph_comp = complete_graph(nodes, init_graph)

    turn = {}

    junctions = ["Junction A", "Junction B", "Junction C", "Junction D", "Front Desk"]

    for node in nodes:
        turn[node] = {}

    for node, out_edges in graph_comp.items():
        if node in junctions:
            for neighbor, distance in out_edges.items():
                if graph_comp[neighbor].get(node, False) != False:
                    turn[neighbor][node] = {}

    turn["Middle Entrance"]["Front Desk"]["Junction D"] = 2

    turn["Front Desk"]["Junction D"]["Junction A"] = 0
    turn["Front Desk"]["Junction D"]["Junction C"] = 2
    turn["Front Desk"]["Junction D"]["Stair Entrance and Room 119"] = -2
    turn["Junction C"]["Junction D"]["Stair Entrance and Room 119"] = 0
    turn["Junction C"]["Junction D"]["Junction A"] = 2
    turn["Junction A"]["Junction D"]["Stair Entrance and Room 119"] = 2

    turn["Junction D"]["Junction C"]["Auditorium"] = 0
    turn["Junction D"]["Junction C"]["Auditorium Entrance"] = 2
    turn["Junction D"]["Junction C"]["Junction B"] = -2
    turn["Auditorium Entrance"]["Junction C"]["Auditorium"] = 2
    turn["Auditorium Entrance"]["Junction C"]["Junction B"] = 0
    turn["Auditorium"]["Junction C"]["Junction B"] = 2

    turn["Junction C"]["Junction B"]["Junction A"] = 0
    turn["Junction C"]["Junction B"]["Entertainment Rooms"] = 2
    turn["Junction A"]["Junction B"]["Entertainment Rooms"] = -2

    turn["Room 115"]["Junction A"]["Junction B"] = 0
    turn["Room 115"]["Junction A"]["Junction D"] = 2
    turn["Room 115"]["Junction A"]["Creamery Entrance"] = -2
    turn["Junction D"]["Junction A"]["Junction B"] = 2
    turn["Junction D"]["Junction A"]["Creamery Entrance"] = 0
    turn["Junction B"]["Junction A"]["Creamery Entrance"] = 2

    turn_comp = complete_turn(nodes, turn)

    graph = Graph(nodes, junctions, graph_comp, turn_comp)

    location = {
        0: "Middle Entrance",
        1: "Stair Entrance and Room 119",
        2: "Auditorium Entrance",
        3: "Creamery Entrance",
        4: "Auditorium",
        5: "Entertainment Rooms",
        6: "Workshop",
        7: "Room 115",
    }

    def choose_place(index):
        chosen = location.get(index, "error")
        if chosen == "error":
            print("Index error.")
            exit()
        return chosen

    def print_place_list():

        for key, value in location.items():
            print(key, "\t:\t", value)

    print_place_list()
    print("")
    index_origin = input("Enter index of your current position: ")
    origin = choose_place(int(index_origin))
    index_dest = input("Enter index of your desired destination: ")
    dest = choose_place(int(index_dest))
    print("")

    if index_origin == index_dest:
        print("Same location!")
        print("")
    else:
        previous_nodes, shortest_path = get_shortest(graph, origin)
        print_result(graph, previous_nodes, shortest_path, origin, dest)


direction = {-2: "left", 0: "straight", 2: "right"}
while True:
    main()

    action = input("Press 1 to Navigate Again (to end navigation, enter any other value): ")

    if int(action) != 1:
        break

    os.system('cls')
