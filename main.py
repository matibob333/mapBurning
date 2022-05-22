import sys
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.exitAction = None
        self.authorAction = None
        self.descriptionAction = None
        self.setWindowTitle("Wypalanie mapy")
        self.create_menu_bar()
        self.resize(1200, 800)

    def create_menu_bar(self):
        self.descriptionAction = QAction("&Opis aplikacji", self)
        self.descriptionAction.triggered.connect(self.show_description_messagebox)
        self.authorAction = QAction("&Autor", self)
        self.authorAction.triggered.connect(self.show_author_messagebox)
        self.exitAction = QAction("&Wyjście", self)
        self.exitAction.triggered.connect(lambda action: exit())

        menu_bar = self.menuBar()
        additional_info = menu_bar.addMenu("&Informacje dodatkowe")
        additional_info.addAction(self.descriptionAction)
        additional_info.addAction(self.authorAction)
        menu_bar.addAction(self.exitAction)


    @staticmethod
    def show_description_messagebox():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Gra \"Wypalanie mapy\"\n"
                    "wykonana na przedmiot "
                    "\"Języki skryptowe i ich zastosowania\"")
        msg.setWindowTitle("Opis aplikacji")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def show_author_messagebox():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Mateusz Nieścier 175778\n"
                    "semestr 1 mgr KASK")
        msg.setWindowTitle("Autor")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


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

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
