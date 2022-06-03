import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from structures.level_structure import LevelStructure


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__width = 1200
        self.__height = 800
        self.button_radius = 25
        self.__draw_field_x_shift = 10
        self.__draw_field_y_shift = 30
        self.__font = 'Calibri'

        self.level_structure = LevelStructure()

        self.exitAction = QAction(self)
        self.authorAction = QAction(self)
        self.descriptionAction = QAction(self)

        self.draw_label = QLabel(self)
        self.reset_game_button = QPushButton(self)
        self.continue_game_button = QPushButton(self)

        self.setWindowTitle("Wypalanie mapy")
        self.create_menu_bar()
        self.draw_begin_view()
        self.setFixedSize(self.__width, self.__height)

    def set_button_stylesheet(self, vertex):
        if vertex.value == 0:
            color = "Mintcream"
        else:
            color = "Cyan"
        vertex.button.setStyleSheet("border-radius : {}; "
                                    "border: 2px solid black; "
                                    "background-color: {};"
                                    .format(self.button_radius, color))

    def create_menu_bar(self):
        self.descriptionAction.setText("&Opis aplikacji")
        self.descriptionAction.triggered.connect(self.show_description_messagebox)
        self.authorAction.setText("&Autor")
        self.authorAction.triggered.connect(self.show_author_messagebox)
        self.exitAction.setText("&Wyjście")
        self.exitAction.triggered.connect(lambda action: exit())

        menu_bar = self.menuBar()
        additional_info = menu_bar.addMenu("&Informacje dodatkowe")
        additional_info.addAction(self.descriptionAction)
        additional_info.addAction(self.authorAction)
        menu_bar.addAction(self.exitAction)

    def draw_begin_view(self):
        self.reset_game_button.setText("RESETUJ POSTĘP")
        self.reset_game_button.setFont(QFont(self.__font, 15))
        self.reset_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 + 100, 200, 200)
        self.reset_game_button.setStyleSheet("border-radius : 100; "
                                             "border: 2px solid black; "
                                             "background-color: yellow;")
        self.reset_game_button.clicked.connect(self.serve_reset_button_clicked)

        self.continue_game_button.setText("GRAJ\nPoziom {}".format(self.level_structure.current_level))
        self.continue_game_button.setFont(QFont(self.__font, 15))
        self.continue_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 - 300, 200, 200)
        self.continue_game_button.setStyleSheet("border-radius : 100; "
                                                "border: 2px solid black; "
                                                "background-color: green;")
        self.continue_game_button.clicked.connect(self.draw_game_view)

    def draw_game_view(self):
        self.continue_game_button.deleteLater()
        self.reset_game_button.deleteLater()
        for vertex in self.level_structure.vertices:
            vertex.button.deleteLater()
        self.level_structure.read_level_file(self)

        self.draw_label.setGeometry(self.__draw_field_x_shift, self.__draw_field_y_shift,
                                    self.__width * 3 // 5 - 2 * self.__draw_field_x_shift,
                                    self.__height - 2 * self.__draw_field_y_shift)
        self.draw_label.setStyleSheet("border :2px solid black;")
        canvas = QPixmap(self.__width * 3 // 5 - 2 * self.__draw_field_x_shift,
                         self.__height - 2 * self.__draw_field_y_shift)
        canvas.fill(QColor("white"))
        self.draw_label.setPixmap(canvas)
        painter = QPainter(self.draw_label.pixmap())
        painter.setPen(QPen(QColor("black"), 3))

        for edge in self.level_structure.edges:
            painter.drawLine(edge.x1 - self.__draw_field_x_shift + self.button_radius,
                             edge.y1 - self.__draw_field_y_shift + self.button_radius,
                             edge.x2 - self.__draw_field_x_shift + self.button_radius,
                             edge.y2 - self.__draw_field_y_shift + self.button_radius)
        painter.end()

        for vertex in self.level_structure.vertices:
            vertex.button.setFont(QFont(self.__font, 12))
            vertex.button.setGeometry(vertex.x, vertex.y, 2 * self.button_radius, 2 * self.button_radius)
            vertex.button.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
