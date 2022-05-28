import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    def __init__(self, level_structure, parent=None):
        super().__init__(parent)

        self.reset_game_button = None
        self.continue_game_button = None
        self.level_structure = level_structure
        self.__width = 1200
        self.__height = 800
        self.__font = 'Calibri'

        self.exitAction = None
        self.authorAction = None
        self.descriptionAction = None
        self.setWindowTitle("Wypalanie mapy")
        self.create_menu_bar()
        self.draw_begin_view()
        self.resize(self.__width, self.__height)

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

    def draw_begin_view(self):
        self.reset_game_button = QPushButton("RESETUJ POSTĘP", self)
        self.reset_game_button.setFont(QFont(self.__font, 15))
        self.reset_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 + 100, 200, 200)
        self.reset_game_button.setStyleSheet("border-radius : 100; "
                                             "border: 2px solid black; "
                                             "background-color: yellow;")
        self.reset_game_button.clicked.connect(self.serve_reset_button_clicked)

        self.continue_game_button = QPushButton("GRAJ\nPoziom {}".format(self.level_structure.current_level), self)
        self.continue_game_button.setFont(QFont(self.__font, 15))
        self.continue_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 - 300, 200, 200)
        self.continue_game_button.setStyleSheet("border-radius : 100; "
                                                "border: 2px solid black; "
                                                "background-color: green;")
        self.continue_game_button.clicked.connect(self.continue_game_button.deleteLater)

    def serve_reset_button_clicked(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Czy na pewno chcesz zresetować swój postęp?")
        msg.setWindowTitle("Potwierdzenie")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return_value = msg.exec()
        if return_value == QMessageBox.Ok:
            self.level_structure.write_new_level_number()
            self.continue_game_button.setText("GRAJ\nPoziom {}".format(self.level_structure.current_level))

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


class LevelStructure:
    def __init__(self):
        self.vertices = None
        self.edges = None
        self.current_level = None
        self.read_which_level_to_open()
        self.read_level_file()

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

    def read_level_file(self):
        with open("saves/levels/{}.txt".format(self.current_level)) as f:
            lines = f.readlines()
        if len(lines) < 2:
            print("error in level file")
            exit(1)
    
        self.vertices = []
        vertices_combined = lines[0].strip().split(";")
        possible_connections = len(vertices_combined)
        for vertex_combined in vertices_combined:
            vertex_split = vertex_combined.strip().split(",")
            if len(vertex_split) != 2:
                print("error in level file - bad vertices")
                exit(1)
            x, y = int(vertex_split[0]), int(vertex_split[1])
            self.vertices.append(Vertex(x, y, possible_connections))
    
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
                    self.vertices[i].neighbouring_vertices[j] = True
                    self.vertices[j].neighbouring_vertices[i] = True


if __name__ == "__main__":
    level_structure = LevelStructure()

    app = QApplication(sys.argv)
    win = Window(level_structure)
    win.show()
    sys.exit(app.exec_())
