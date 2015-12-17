from pyglet.text import Label
from pyglet import image
import cv2
import imutils
import numpy
from pygarrayimage.arrayimage import ArrayInterfaceImage

from sympy import Polygon, Point

class Menu:
    def __init__(self, window):
        self.window = window
        self.selected_option = 0

    def draw(self):
        menu_label = Label('Menu', font_name='Times New Roman',
                               font_size=50, x=self.window.width/2,
                                y=self.window.height-100, anchor_x='center',
                                anchor_y='center')

        new_game_label = Label('New game', font_name='Times New Roman',
                                    font_size=32, x=self.window.width/2,
                                    y=self.window.height-200, anchor_x='center',
                                    anchor_y='center')

        quit_label = Label('Quit', font_name='Times New Roman',
                                    font_size=32, x=self.window.width/2,
                                    y=self.window.height-270, anchor_x='center',
                                    anchor_y='center')

        new_game_label.set_style("color", (255, 255, 255, 255))
        quit_label.set_style("color", (255, 255, 255, 255))

        if self.selected_option == 0:
            new_game_label.set_style("color", (0, 255, 0, 255))
        elif self.selected_option == 1:
            quit_label.set_style("color", (0, 255, 0, 255))

        menu_label.draw()
        new_game_label.draw()
        quit_label.draw()


class Playing:
    def __init__(self, window):
        self.window = window
        self.camera = cv2.VideoCapture(0)
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

    def rect_collide(self, rect1, rect2):
        rect1_p1 = Point(*rect1['point1'])
        rect1_p2 = Point(*rect1['point2'])
        rect2_vertex1 = Point(*rect2['point1'])
        rect2_vertex2 = Point(*rect2['point1'])
        rect2_vertex3 = Point(rect2['point1'][0], rect2['point2'][1])
        rect2_vertex4 = Point(rect2['point2'][0], rect2['point1'][1])

        vertex1_inside = rect1_p1.x < rect2_vertex1.x and rect1_p2.x > rect2_vertex1.x and rect1_p1.y < rect2_vertex1.y and rect1_p2.y > rect2_vertex1.y
        vertex2_inside = rect1_p1.x < rect2_vertex2.x and rect1_p2.x > rect2_vertex2.x and rect1_p1.y < rect2_vertex2.y and rect1_p2.y > rect2_vertex2.y
        vertex3_inside = rect1_p1.x < rect2_vertex3.x and rect1_p2.x > rect2_vertex3.x and rect1_p1.y < rect2_vertex3.y and rect1_p2.y > rect2_vertex3.y
        vertex4_inside = rect1_p1.x < rect2_vertex4.x and rect1_p2.x > rect2_vertex4.x and rect1_p1.y < rect2_vertex4.y and rect1_p2.y > rect2_vertex4.y

        return vertex1_inside or vertex2_inside or vertex3_inside or vertex4_inside

    def draw(self):
        (grabbed, frame) = self.camera.read()
        if grabbed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = numpy.rot90(frame, 2)

            frame = imutils.resize(frame, width=self.window.width, height=self.window.height)
            fgmask = self.fgbg.apply(frame)
            fgmask = cv2.blur(fgmask, (self.window.width/100, self.window.width/100))
            fgmask = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]

            (cnts, _) = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            blue_rect = {
                "point1": (100, 100),
                "point2": (300, 300)
            }
            blue_border = {
                "point1": (95, 95),
                "point2": (305, 305)
            }
            green_rect = {
                "point1": (100, self.window.height - 300),
                "point2": (300, self.window.height - 100)
            }
            green_border = {
                "point1": (95, self.window.height - 305),
                "point2": (305, self.window.height - 95)
            }
            red_rect = {
                "point1": (self.window.width - 300, self.window.height - 100),
                "point2": (self.window.width - 100, self.window.height - 300)
            }
            red_border = {
                "point1": (self.window.width - 305, self.window.height - 95),
                "point2": (self.window.width - 95, self.window.height - 305)
            }
            yellow_rect = {
                "point1": (self.window.width - 300, 100),
                "point2": (self.window.width - 100, 300)
            }
            yellow_border = {
                "point1": (self.window.width - 305, 95),
                "point2": (self.window.width - 95, 305)
            }

            cv2.rectangle(frame, blue_rect['point1'], blue_rect['point2'], (0, 0, 255), cv2.FILLED)
            cv2.rectangle(frame, green_rect['point1'], green_rect['point2'], (0, 255, 0), cv2.FILLED)
            cv2.rectangle(frame, red_rect['point1'], red_rect['point2'], (255, 0, 0), cv2.FILLED)
            cv2.rectangle(frame, yellow_rect['point1'], yellow_rect['point2'], (255, 255, 0), cv2.FILLED)

            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                area = cv2.contourArea(c)
                if area < (self.window.width * self.window.height) * 0.005:
                    continue

                rect = {
                    "point1": (x, y),
                    "point2": (x + w, y + h)
                }

                if self.rect_collide(rect, blue_rect):
                    cv2.rectangle(frame, blue_border['point1'], blue_border['point2'], (0, 0, 255), 2)

                if self.rect_collide(rect, green_rect):
                    cv2.rectangle(frame, green_border['point1'], green_border['point2'], (0, 255, 0), 2)

                if self.rect_collide(rect, red_rect):
                    cv2.rectangle(frame, red_border['point1'], red_border['point2'], (255, 0, 0), 2)

                if self.rect_collide(rect, yellow_rect):
                    cv2.rectangle(frame, yellow_border['point1'], yellow_border['point2'], (255, 255, 0), 2)

            webcam = ArrayInterfaceImage(frame)
            webcam.blit(0, 0)
