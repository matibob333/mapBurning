class Vertex:
    def __init__(self, x, y, possible_vertices_number):
        self.x = x
        self.y = y
        self.value = 0
        self.neighbouring_vertices = [False for _ in range(possible_vertices_number)]


class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def read_which_level_to_open():
    with open("saves/current_level.txt") as f:
        lines = f.readlines()
    if len(lines) < 1:
        print("error in searching for level")
        exit(1)
    return int(lines[0].strip())


def read_level_file(current_level_number):
    with open("saves/levels/{}.txt".format(current_level_number)) as f:
        lines = f.readlines()
    if len(lines) < 2:
        print("error in level file")
        exit(1)

    vertices_for_output = []
    vertices_combined = lines[0].strip().split(";")
    possible_connections = len(vertices_combined)
    for vertex_combined in vertices_combined:
        vertex_split = vertex_combined.strip().split(",")
        if len(vertex_split) != 2:
            print("error in level file - bad vertices")
            exit(1)
        x, y = int(vertex_split[0]), int(vertex_split[1])
        vertices_for_output.append(Vertex(x, y, possible_connections))

    edges_for_output = []
    edges_combined = lines[1].strip().split(";")
    if len(edges_combined) != possible_connections - 1:
        print("error in level file - bad edges length")
        exit(1)
    for i in range(len(edges_combined)):
        if len(edges_combined[i]) != possible_connections - 1 - i:
            print("error in level file - bad edges length")
            exit(1)
        begin_value = possible_connections - len(edges_combined[i])
        for j in range(begin_value, possible_connections):
            if edges_combined[i][j - begin_value] == '|':
                edges_for_output.append(Edge(vertices_for_output[i].x, vertices_for_output[i].y,
                                             vertices_for_output[j].x, vertices_for_output[j].y))
                vertices_for_output[i].neighbouring_vertices[j] = True
                vertices_for_output[j].neighbouring_vertices[i] = True

    return vertices_for_output, edges_for_output


if __name__ == "__main__":
    current_level = read_which_level_to_open()
    vertices, edges = read_level_file(current_level)

    print()
