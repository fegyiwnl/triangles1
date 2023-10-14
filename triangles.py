import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPolygonF
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPointF


class TriangleGameView(QGraphicsView):
    def wheelEvent(self, event):
        event.ignore()


class TriangleGameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подсчет треугольников")
        self.setWindowIcon(QtGui.QIcon('image_logo.png'))
        self.setGeometry(100, 100, 850, 600)
        self.setFixedSize(850, 600)
        self.scene = QGraphicsScene()
        self.view = TriangleGameView(self.scene, self)
        self.view.setAlignment(Qt.AlignTop)
        self.view.setGeometry(0, 0, 850, 500)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.level = 1
        self.triangle_count = 1
        self.current_guess = None
        self.outer_triangle = None

        self.guess_label = QLabel("Введите количество треугольников:", self)
        self.guess_label.setGeometry(300, 550, 200, 30)

        self.guess_input = QLineEdit(self)
        self.guess_input.setGeometry(500, 550, 50, 30)

        self.submit_button = QPushButton("Проверить", self)
        self.submit_button.setGeometry(570, 550, 80, 30)
        self.submit_button.clicked.connect(self.check_guess)

        self.reset_button = QPushButton("Заново", self)
        self.reset_button.setGeometry(660, 550, 80, 30)
        self.reset_button.clicked.connect(self.reset_game)

        self.triangle_count_label = QLabel("", self)
        self.triangle_count_label.setGeometry(20, 520, 200, 30)

        self.generate_triangles()

    def generate_triangles(self):
        pixmap = QPixmap(800, 500)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        self.outer_triangle = QPolygonF([QPointF(400, 0), QPointF(0, 495), QPointF(800, 495)])
        painter.setPen(Qt.black)
        painter.drawPolygon(self.outer_triangle)

        if self.level >= 2:
            self.triangle_count = 3

            vertex_index = random.randint(0, 2)
            vertex = self.outer_triangle[vertex_index]

            mid_point = (self.outer_triangle[(vertex_index + 1) % 3] + self.outer_triangle[(vertex_index + 2) % 3]) / 2
            painter.drawLine(vertex, mid_point)

        if self.level >= 3:
            self.triangle_count = 8

            other_vertex_index = (vertex_index + 1) % 3
            other_vertex = self.outer_triangle[other_vertex_index]
            second_mid_point = (self.outer_triangle[(other_vertex_index + 1) % 3] + self.outer_triangle[
                (other_vertex_index + 2) % 3]) / 2
            painter.drawLine(other_vertex, second_mid_point)

        if self.level >= 4:
            self.triangle_count = 16

            remaining_vertex_index = (vertex_index + 2) % 3
            remaining_vertex = self.outer_triangle[remaining_vertex_index]
            third_mid_point = (self.outer_triangle[(remaining_vertex_index + 1) % 3] + self.outer_triangle[
                (remaining_vertex_index + 2) % 3]) / 2
            painter.drawLine(remaining_vertex, third_mid_point)

        if self.level >= 5:
            self.triangle_count = 31

            new_triangles = []
            for triangle in [self.outer_triangle]:
                mid_points = [(triangle[0] + triangle[1]) / 2, (triangle[1] + triangle[2]) / 2,
                              (triangle[0] + triangle[2]) / 2]
                new_triangles.extend([QPolygonF([triangle[0], mid_points[0], mid_points[2]]),
                                      QPolygonF([triangle[1], mid_points[0], mid_points[1]]),
                                      QPolygonF([triangle[2], mid_points[1], mid_points[2]])])

            for new_triangle in new_triangles:
                mid_point = (new_triangle[0] + new_triangle[1] + new_triangle[2]) / 3
                painter.setPen(Qt.black)
                painter.drawPolyline(new_triangle + QPolygonF([mid_point]))

        if self.level >= 6:
            self.triangle_count_label.setText("Вы прошли все уровни!")
            self.triangle_count_label.setStyleSheet('color: green; border: none;')
            self.triangle_count_label.setGeometry(100, 550, 200, 30)

        painter.end()

        self.scene.clear()
        self.scene.addPixmap(pixmap)

    def check_guess(self):
        if self.triangle_count is not None:
            guessed_value = self.guess_input.text()
            try:
                guessed_value = int(guessed_value)
            except ValueError:
                guessed_value = None

            if guessed_value == self.triangle_count:
                self.level += 1
                self.generate_triangles()
                self.guess_input.clear()

    def reset_game(self):
        self.level = 1
        self.triangle_count = 1
        self.generate_triangles()
        self.triangle_count_label.clear()
        self.guess_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)

    app.setStyle('Fusion')

    window = TriangleGameApp()
    window.show()
    sys.exit(app.exec_())
