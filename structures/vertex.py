from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Vertex:
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.value = 0
        self.neighbouring_vertices = []
        self.window = window
        self.button = QPushButton(window)
        self.button.setText(str(self.value))
        window.set_button_stylesheet(self)
        self.button.clicked.connect(self.change_value_of_vertices)

    def change_value_of_vertices(self):
        self.value += 2
        self.window.set_button_stylesheet(self)
        self.button.setText(str(self.value))
        lose_achieved = False
        if self.value >= self.window.level_structure.losing_score:
            lose_achieved = True
        for vertex in self.neighbouring_vertices:
            vertex.value += 1
            self.window.set_button_stylesheet(vertex)
            vertex.button.setText(str(vertex.value))
            if vertex.value >= self.window.level_structure.losing_score:
                lose_achieved = True
        if lose_achieved:
            self.window.handle_lost()
        elif self.window.level_structure.check_if_win_achieved():
            self.window.handle_win()

    def reset_value(self):
        self.value = 0
        self.window.set_button_stylesheet(self)
        self.button.setText(str(self.value))
