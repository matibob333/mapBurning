import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from structures.level_structure import LevelStructure


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.end_of_game = False

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

        self.background_label = QLabel(self)
        self.reset_game_button = QPushButton(self)
        self.continue_game_button = QPushButton(self)
        self.reset_game_button.hide()
        self.continue_game_button.hide()

        self.draw_label = QLabel(self)
        self.level_title_label = QLabel(self)
        self.level_value_label = QLabel(self)
        self.winning_title_label = QLabel(self)
        self.winning_value_label = QLabel(self)
        self.losing_title_label = QLabel(self)
        self.losing_value_label = QLabel(self)
        self.info_label = QLabel(self)
        self.reset_level_button = QPushButton(self)
        self.next_level_button = QPushButton(self)
        self.main_menu_button = QPushButton(self)
        self.reset_level_button.hide()
        self.next_level_button.hide()
        self.main_menu_button.hide()

        self.setWindowTitle("Wypalanie mapy")
        self.create_menu_bar()
        self.draw_begin_view()
        self.setFixedSize(self.__width, self.__height)

    def set_reset_button_availability(self):
        if self.level_structure.current_level <= 1:
            self.reset_game_button.setEnabled(False)
            self.reset_game_button.setStyleSheet("border-radius : 100; "
                                                 "border: 2px solid grey; "
                                                 "background-color: Gainsboro;"
                                                 "color: grey")
        else:
            self.reset_game_button.setStyleSheet("border-radius : 100; "
                                                 "border: 2px solid black; "
                                                 "background-color: yellow;")

    def set_button_stylesheet(self, vertex):
        if vertex.value == 0:
            color = "Mintcream"
        elif vertex.value < self.level_structure.winning_score:
            color = "Cyan"
        elif vertex.value == self.level_structure.winning_score:
            color = "Lime"
        elif vertex.value < self.level_structure.losing_score:
            color = "Gold"
        else:
            color = "Orangered"
        vertex.button.setStyleSheet("border-radius : {}; "
                                    "border: 2px solid black; "
                                    "background-color: {};"
                                    .format(self.button_radius, color))

    def handle_lost(self):
        self.info_label.setText("Przegrywasz! Kliknij \"od nowa\"")
        self.info_label.show()
        for vertex in self.level_structure.vertices:
            vertex.button.setEnabled(False)

    def handle_win(self):
        for vertex in self.level_structure.vertices:
            vertex.button.setEnabled(False)
        self.info_label.setText("Wygrywasz!")
        self.info_label.show()
        self.level_structure.can_go_to_next_level = True
        self.next_level_button.setStyleSheet("border: 2px solid black; "
                                             "background-color: Greenyellow;")
        self.next_level_button.setEnabled(True)

    def reset_level(self):
        self.info_label.setText("")
        self.info_label.show()
        self.next_level_button.setStyleSheet("border: 2px solid grey; "
                                             "background-color: Gainsboro;"
                                             "color: grey")
        self.level_structure.can_go_to_next_level = False
        self.next_level_button.setEnabled(False)
        self.level_structure.reset_vertices()

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

    def go_to_begin_view(self):
        self.clear_previous_game_view()
        self.draw_begin_view()

    def go_to_game_view(self):
        self.clear_previous_game_view()
        if self.end_of_game:
            self.draw_begin_view()
        else:
            self.draw_game_view()

    def clear_previous_game_view(self):
        self.draw_label.hide()
        self.level_title_label.hide()
        self.level_value_label.hide()
        self.winning_title_label.hide()
        self.winning_value_label.hide()
        self.losing_title_label.hide()
        self.losing_value_label.hide()
        self.info_label.hide()
        self.reset_level_button.hide()
        self.next_level_button.hide()
        self.main_menu_button.hide()

        self.draw_label = QLabel(self)
        self.level_title_label = QLabel(self)
        self.level_value_label = QLabel(self)
        self.winning_title_label = QLabel(self)
        self.winning_value_label = QLabel(self)
        self.losing_title_label = QLabel(self)
        self.losing_value_label = QLabel(self)
        self.reset_level_button = QPushButton(self)
        self.next_level_button = QPushButton(self)
        self.main_menu_button = QPushButton(self)

        for vertex in self.level_structure.vertices:
            vertex.button.hide()
            vertex.button = QPushButton(self)

        if self.level_structure.can_go_to_next_level:
            next_level = self.level_structure.current_level + 1
            if self.level_structure.check_level_existence(next_level):
                self.level_structure.write_new_level_number(next_level)
                self.continue_game_button.setText("GRAJ\nPoziom {}".format(self.level_structure.current_level))
            else:
                self.end_of_game = True
            self.level_structure.can_go_to_next_level = False

    def draw_begin_view(self):
        self.continue_game_button.show()
        self.reset_game_button.show()
        self.background_label.show()

        for vertex in self.level_structure.vertices:
            vertex.button.deleteLater()

        self.background_label.setGeometry(10, 30, self.__width - 20, self.__height - 60)
        self.background_label.setStyleSheet("border: 2px solid black; background-color: white")

        self.reset_game_button.setText("RESETUJ POSTĘP")
        self.reset_game_button.setFont(QFont(self.__font, 15))
        self.reset_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 + 100, 200, 200)
        self.set_reset_button_availability()
        self.reset_game_button.clicked.connect(self.serve_reset_button_clicked)

        self.continue_game_button.setText("GRAJ\nPoziom {}".format(self.level_structure.current_level))
        self.continue_game_button.setFont(QFont(self.__font, 15))
        self.continue_game_button.setGeometry(self.__width // 2 - 100, self.__height // 2 - 300, 200, 200)
        self.continue_game_button.setStyleSheet("border-radius : 100; "
                                                "border: 2px solid black; "
                                                "background-color: green;")
        self.continue_game_button.clicked.connect(self.draw_game_view)

        if self.end_of_game:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Gratulacje! Przeszedłeś wszystkie dostępne poziomy!")
            msg.setWindowTitle("Opis aplikacji")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.end_of_game = False

    def draw_game_view(self):
        self.continue_game_button.hide()
        self.reset_game_button.hide()
        self.background_label.hide()
        self.continue_game_button = QPushButton(self)
        self.reset_game_button = QPushButton(self)
        self.level_structure.read_level_file(self)

        self.level_title_label.setText("Poziom")
        self.level_title_label.setFont(QFont(self.__font, 12))
        self.level_title_label.move(self.__width * 3 // 5 + 10, 50)
        self.level_title_label.show()

        self.level_value_label.setText(str(self.level_structure.current_level))
        self.level_value_label.setFont(QFont(self.__font, 12))
        self.level_value_label.move(self.__width * 3 // 5 + 300, 50)
        self.level_value_label.show()

        self.winning_title_label.setText("próg wypalenia")
        self.winning_title_label.setFont(QFont(self.__font, 12))
        self.winning_title_label.move(self.__width * 3 // 5 + 10, 70)
        self.winning_title_label.show()

        self.winning_value_label.setText(str(self.level_structure.winning_score))
        self.winning_value_label.setFont(QFont(self.__font, 12))
        self.winning_value_label.move(self.__width * 3 // 5 + 300, 70)
        self.winning_value_label.show()

        self.losing_title_label.setText("próg przegranej")
        self.losing_title_label.setFont(QFont(self.__font, 12))
        self.losing_title_label.move(self.__width * 3 // 5 + 10, 90)
        self.losing_title_label.show()

        self.losing_value_label.setText(str(self.level_structure.losing_score))
        self.losing_value_label.setFont(QFont(self.__font, 12))
        self.losing_value_label.move(self.__width * 3 // 5 + 300, 90)
        self.losing_value_label.show()

        self.info_label.setFont(QFont(self.__font, 12))
        self.info_label.setGeometry(self.__width * 3 // 5 + 10, 110, 450, 50)
        self.losing_value_label.show()

        self.reset_level_button.setText("od nowa")
        self.reset_level_button.setFont(QFont(self.__font, 12))
        self.reset_level_button.setGeometry(self.__width * 3 // 5 + 10, 300, 450, 50)
        self.reset_level_button.setStyleSheet("border: 2px solid black; "
                                              "background-color: Greenyellow;")
        self.reset_level_button.clicked.connect(self.reset_level)
        self.reset_level_button.show()

        self.next_level_button.setText("kolejny poziom")
        self.next_level_button.setFont(QFont(self.__font, 12))
        self.next_level_button.setGeometry(self.__width * 3 // 5 + 10, 400, 450, 50)
        self.next_level_button.setStyleSheet("border: 2px solid grey; "
                                             "background-color: Gainsboro;"
                                             "color: grey")
        self.next_level_button.clicked.connect(self.go_to_game_view)
        self.next_level_button.setEnabled(False)
        self.next_level_button.show()

        self.main_menu_button.setText("powrót do głównego menu")
        self.main_menu_button.setFont(QFont(self.__font, 12))
        self.main_menu_button.setGeometry(self.__width * 3 // 5 + 10, 600, 450, 50)
        self.main_menu_button.setStyleSheet("border: 2px solid black; "
                                            "background-color: Greenyellow;")
        self.main_menu_button.clicked.connect(self.go_to_begin_view)
        self.main_menu_button.show()

        self.draw_label.show()
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
            self.set_reset_button_availability()

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
