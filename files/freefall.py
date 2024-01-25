import pygame
import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('uis/freefallsettings.ui', self)
        self.setWindowIcon(QtGui.QIcon('pics/settingsicon.png'))

        self.bouncemultconfig.valueChanged.connect(self.bconfpressed)
        self.savebutton.clicked.connect(self.savesettings)
        self.exitbutton.clicked.connect(sys.exit)
        self.show()

    def savesettings(self):
        global gravforce, physobjsize, bouncemult, tickrate
        gravforce = int(self.gravforceconfig.text())
        physobjsize = int(self.physobjsizeconfig.text())
        # красивый ui - пользователь видит 5%, которые приводятся к множителю в 0.95
        bouncemult = 1 - (int(self.bouncemultconfig.value()) / 100)
        tickrate = int(self.tickrateconfig.text())

        self.close()

    def bconfpressed(self):
        self.percentlabel.setText(str(self.bouncemultconfig.value()) + "%")


def configscreen():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


def drawphysobj():
    # physobj[position][0][1] это y(игрек) координата объекта
    for position in range(len(physobj)):
        # проверка паузы
        if not paused:
            t = physobj[position][1]
            if t > 0:
                physobj[position][0][1] += gravforce * t * t  # свободное падение, h -= (gt^2)/2
            else:
                physobj[position][0][1] -= gravforce * t * t  # отскок если t < 0
                # КОСТЫЛЬ, if потому что t^2 == (-t)^2 и приходится расписывать действия на оба случая (t > 0 и t < 0)

            # проверяем, ударился ли объект о поверхность
            border = size[1] - framesize - physobjsize
            if physobj[position][0][1] > border:
                # выталкиваем объект из-за границ
                physobj[position][0][1] = border
                if physobj[position][1] * bouncemult > 0.001:
                    physobj[position][1] *= -bouncemult  # объект отскакивает назад, теряя скорость
                else:
                    physobj[position][1] = 0
            physobj[position][1] += round(1 / tickrate, 3)  # плавное прибавление переменной t, привязанное к FPS

        pygame.draw.circle(screen, WHITE, physobj[position][0], physobjsize)


def reloadscreen():
    width = size[0]
    height = size[1]
    # рисуем красивую рамочку по длине экрана
    screen.fill(BLUE)
    pygame.draw.rect(screen, WHITE, pygame.Rect((0, 0), (width, height)), framesize)


# константы
WHITE = (250, 241, 245)
BLUE = (25, 41, 88)
framesize = 10
size = [1000, 800]
middle = size[0] // 2
fontsize = 50

# переменные
paused = False
physobj = []

gravforce = 100
physobjsize = 40
bouncemult = 0.95
tickrate = 60
pausewhen = 10

# Первым делом соберем настройки пользователя
configscreen()

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Свободное падение')
pygame.display.set_icon(pygame.image.load("pics/icon.png"))
clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Arial', fontsize)
pausetext = my_font.render('PAUSED', False, WHITE)
pausecenter = pausetext.get_rect(center=(middle, fontsize + 30))

running = True
while running:
    reloadscreen()
    drawphysobj()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            physobj.append([list(pos), 0])
            # записываем в список физических объектов положение объекта и переменную t

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                physobj = []
            if event.key == pygame.K_s:
                paused = True
                screen.blit(pausetext, pausecenter)
                pygame.display.flip()
                configscreen()
            if event.key == pygame.K_BACKSPACE and len(physobj) > 0:
                physobj.pop()
    if paused:
        screen.blit(pausetext, pausecenter)
    pygame.display.flip()
    clock.tick(tickrate)
pygame.quit()
