from os.path import exists
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Vertex:
    def __init__(self, x, y, main_window):
        self.x = x
        self.y = y
        self.value = 0
        self.neighbouring_vertices = []
        self.window = main_window
        self.button = Gtk.Button(label=str(self.value))
        self.button.set_size_request(50, 50)
        self.button.connect('clicked', self.change_value_of_vertices)

    def change_value_of_vertices(self, widget):
        self.value += 2
        self.button.set_label(str(self.value))
        lose_achieved = False
        if self.value >= self.window.level_structure.losing_score:
            lose_achieved = True
        for vertex in self.neighbouring_vertices:
            vertex.value += 1
            vertex.button.set_label(str(vertex.value))
            if vertex.value >= self.window.level_structure.losing_score:
                lose_achieved = True
        if lose_achieved:
            self.window.handle_lost()
        elif self.window.level_structure.check_if_win_achieved():
            self.window.handle_win()

    def reset_value(self):
        self.value = 0
        self.button.set_label(str(self.value))


class LevelStructure:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.current_level = 1
        self.winning_score = 0
        self.losing_score = 0
        self.can_go_to_next_level = False
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

    @staticmethod
    def check_level_existence(number):
        return exists("saves/levels/{}.txt".format(number))

    def read_level_file(self, main_window):
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
            self.vertices.append(Vertex(x, y, main_window))

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
            vertex.button.set_sensitive(True)

    def check_if_win_achieved(self):
        for vertex in self.vertices:
            if vertex.value < self.winning_score:
                return False
        return True


class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__()

        self.next_level_button = None
        self.info_label = None
        self.main_space = None

        self.continue_game_button = None
        self.reset_game_button = None

        self.end_of_game = False

        self.__width = 1200
        self.__height = 800
        self.button_radius = 25
        self.__draw_field_x_shift = 25
        self.__draw_field_y_shift = 25

        self.level_structure = LevelStructure()

        self.set_title("Wypalanie mapy")
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(self.__width, self.__height)
        self.set_resizable(False)

        self.all_space = Gtk.VBox(spacing=6)
        self.create_menu_bar()
        # self.main_space = Gtk.Fixed()
        # self.all_space.add(self.main_space)
        self.draw_begin_view()

    def create_menu_bar(self):
        mb = Gtk.MenuBar()
        extended_menu = Gtk.Menu()
        additional_information = Gtk.MenuItem(label="Informacje dodatkowe")
        additional_information.set_submenu(extended_menu)
        description = Gtk.MenuItem(label="Opis aplikacji")
        description.connect_object('button-press-event', self.show_description_messagebox, additional_information)
        extended_menu.append(description)
        author = Gtk.MenuItem(label="Autor")
        author.connect_object('button-press-event', self.show_author_messagebox, additional_information)
        extended_menu.append(author)
        app_quit = Gtk.MenuItem(label="Wyjście")
        app_quit.connect_object('button-press-event', Gtk.main_quit, mb)
        mb.append(additional_information)
        mb.append(app_quit)

        self.all_space.pack_start(mb, False, False, 0)
        self.add(self.all_space)

    def go_to_begin_view(self, widget):
        self.clear_previous_game_view()
        self.draw_begin_view()

    def go_to_game_view(self, widget):
        self.clear_previous_game_view()
        if self.end_of_game:
            self.draw_begin_view()
        else:
            self.draw_game_view()

    def clear_previous_game_view(self):
        self.all_space.remove(self.main_space)

        if self.level_structure.can_go_to_next_level:
            next_level = self.level_structure.current_level + 1
            if self.level_structure.check_level_existence(next_level):
                self.level_structure.write_new_level_number(next_level)
                self.continue_game_button.set_label("GRAJ\nPoziom {}".format(self.level_structure.current_level))
            else:
                self.end_of_game = True
            self.level_structure.can_go_to_next_level = False

    def draw_begin_view(self):
        self.main_space = Gtk.VBox(spacing=6)
        self.all_space.add(self.main_space)

        self.continue_game_button = Gtk.Button(label="GRAJ\nPoziom {}".format(self.level_structure.current_level))
        self.continue_game_button.connect('clicked', self.draw_game_view)
        self.main_space.add(self.continue_game_button)

        self.reset_game_button = Gtk.Button(label="RESETUJ POSTĘP")
        if self.level_structure.current_level <= 1:
            self.reset_game_button.set_sensitive(False)
        self.reset_game_button.connect('clicked', self.serve_reset_button_clicked)
        self.main_space.add(self.reset_game_button)

        self.show_all()

        if self.end_of_game:
            dialog = Gtk.Dialog(title="Gratulacje!", transient_for=self, flags=0)
            dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
            label = Gtk.Label(label="Gratulacje! Przeszedłeś wszystkie dostępne poziomy!")
            box = dialog.get_content_area()
            box.add(label)
            dialog.show_all()
            dialog.run()
            dialog.destroy()
            self.end_of_game = False

    def serve_reset_button_clicked(self, widget):
        dialog = Gtk.Dialog(title="Potwierdzenie", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        label = Gtk.Label(label="Czy na pewno chcesz zresetować swój postęp?")
        box = dialog.get_content_area()
        box.add(label)
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            self.level_structure.write_new_level_number()
            self.continue_game_button.set_label("GRAJ\nPoziom {}".format(self.level_structure.current_level))
            if self.level_structure.current_level <= 1:
                self.reset_game_button.set_sensitive(False)

    def handle_lost(self):
        self.info_label.set_label("Przegrywasz! Kliknij \"od nowa\"")
        for vertex in self.level_structure.vertices:
            vertex.button.set_sensitive(False)

    def handle_win(self):
        for vertex in self.level_structure.vertices:
            vertex.button.set_sensitive(False)
        self.info_label.set_label("Wygrywasz!")
        self.level_structure.can_go_to_next_level = True
        self.next_level_button.set_sensitive(True)

    def reset_level(self, widget):
        self.info_label.set_label("")
        self.level_structure.can_go_to_next_level = False
        self.next_level_button.set_sensitive(False)
        self.level_structure.reset_vertices()

    def draw_edges(self, area, context):
        context.set_line_width(3)
        context.set_source_rgb(0, 0, 0)
        context.rectangle(0, 0, self.__width * 3 // 5, self.__height)
        context.stroke()
        for edge in self.level_structure.edges:
            context.move_to(edge.x1 + self.__draw_field_x_shift,
                            edge.y1 + self.__draw_field_y_shift)
            context.line_to(edge.x2 + self.__draw_field_x_shift,
                            edge.y2 + self.__draw_field_y_shift)
            context.stroke()

    def draw_game_view(self, widget=None):
        x_space, y_space = 100, 20

        self.level_structure.read_level_file(self)

        self.all_space.remove(self.main_space)

        self.main_space = Gtk.Box(spacing=6)
        map_space = Gtk.Fixed()

        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request(self.__width * 3 // 5, self.__height)
        drawing_area.connect("draw", self.draw_edges)

        map_space.put(drawing_area, 0, 0)

        info_space = Gtk.Grid()

        level_title_label = Gtk.Label(label="Poziom")
        level_title_label.set_size_request(x_space, y_space)
        info_space.add(level_title_label)

        level_value_label = Gtk.Label(label=str(self.level_structure.current_level))
        level_value_label.set_size_request(x_space, y_space)
        info_space.attach(level_value_label, 1, 0, 1, 1)

        winning_title_label = Gtk.Label(label="próg wypalenia")
        winning_title_label.set_size_request(x_space, y_space)
        info_space.attach(winning_title_label, 0, 1, 1, 1)

        winning_value_label = Gtk.Label(label=str(self.level_structure.winning_score))
        winning_value_label.set_size_request(x_space, y_space)
        info_space.attach(winning_value_label, 1, 1, 1, 1)

        losing_title_label = Gtk.Label(label="próg przegranej")
        losing_title_label.set_size_request(x_space, y_space)
        info_space.attach(losing_title_label, 0, 2, 1, 1)

        losing_value_label = Gtk.Label(label=str(self.level_structure.losing_score))
        losing_value_label.set_size_request(x_space, y_space)
        info_space.attach(losing_value_label, 1, 2, 1, 1)

        button_space = Gtk.VBox(spacing=6)

        reset_level_button = Gtk.Button(label="od nowa")
        reset_level_button.connect('clicked', self.reset_level)
        button_space.add(reset_level_button)

        self.next_level_button = Gtk.Button(label="kolejny poziom")
        self.next_level_button.connect('clicked', self.go_to_game_view)
        self.next_level_button.set_sensitive(False)
        button_space.add(self.next_level_button)

        main_menu_button = Gtk.Button(label="powrót do głównego menu")
        main_menu_button.connect('clicked', self.go_to_begin_view)
        button_space.add(main_menu_button)

        self.info_label = Gtk.Label()
        button_space.add(self.info_label)

        info_space.attach(button_space, 0, 4, 1, 2)

        self.main_space.add(map_space)
        self.main_space.add(info_space)
        self.all_space.add(self.main_space)

        for vertex in self.level_structure.vertices:
            map_space.put(vertex.button, vertex.x, vertex.y)

        self.show_all()

    def show_description_messagebox(self, widget, event):
        dialog = Gtk.Dialog(title="Opis aplikacji", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        label = Gtk.Label(label="Gra \"Wypalanie mapy\"\n"
                                "wykonana na przedmiot\n"
                                "\"Języki skryptowe i ich zastosowania\"")
        box = dialog.get_content_area()
        box.add(label)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def show_author_messagebox(self, widget, event):
        dialog = Gtk.Dialog(title="Autor", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        label = Gtk.Label(label="Mateusz Nieścier 175778\n"
                                "semestr 1 mgr KASK")
        box = dialog.get_content_area()
        box.add(label)
        dialog.show_all()
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    window = Window()
    window.show_all()
    Gtk.main()
