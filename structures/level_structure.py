from .vertex import Vertex
from .edge import Edge


class LevelStructure:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.current_level = 1
        self.winning_score = 0
        self.losing_score = 0
        self.read_which_level_to_open()

    def read_which_level_to_open(self):
        with open("saves/current_level.txt") as f:
            lines = f.readlines()
        if len(lines) < 1:
            print("error in searching for level")
            exit(1)
        self.current_level = int(lines[0].strip())

    def write_new_level_number(self, number=1):
        f = open("saves/current_level.txt", "w")
        f.write(str(number))
        f.close()
        self.current_level = number

    def read_level_file(self, window):
        with open("saves/levels/{}.txt".format(self.current_level)) as f:
            lines = f.readlines()
        if len(lines) < 4:
            print("error in level file")
            exit(1)
        self.winning_score = int(lines[2].strip())
        self.losing_score = int(lines[3].strip())

        self.vertices = []
        vertices_combined = lines[0].strip().split(";")
        possible_connections = len(vertices_combined)
        for vertex_combined in vertices_combined:
            vertex_split = vertex_combined.strip().split(",")
            if len(vertex_split) != 2:
                print("error in level file - bad vertices")
                exit(1)
            x, y = int(vertex_split[0]), int(vertex_split[1])
            self.vertices.append(Vertex(x, y, window))

        self.edges = []
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
                    self.edges.append(Edge(self.vertices[i].x, self.vertices[i].y,
                                           self.vertices[j].x, self.vertices[j].y))
                    self.vertices[i].neighbouring_vertices.append(self.vertices[j])
                    self.vertices[j].neighbouring_vertices.append(self.vertices[i])

    def reset_vertices(self):
        for vertex in self.vertices:
            vertex.reset_value()
            vertex.button.setEnabled(True)
