class Vertex:
    def __init__(self, x, y, possible_vertices_number):
        self.x = x
        self.y = y
        self.value = 0
        self.neighbouring_vertices = [False for _ in range(possible_vertices_number)]