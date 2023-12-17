import pygame
import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication


def menuwindow():
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()


def launchfreefall():
    FreeFall()


class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        uic.loadUi('uis/mainmenu.ui', self)
        self.setWindowIcon(QtGui.QIcon('pics/settingsicon.png'))
        self.freefall.clicked.connect(launchfreefall)
        self.exit.clicked.connect(sys.exit)
        self.show()


class FreeFallSettings(QtWidgets.QMainWindow):
    def __init__(self):
        super(FreeFallSettings, self).__init__()
        uic.loadUi('uis/freefallsettings.ui', self)
        self.setWindowIcon(QtGui.QIcon('pics/settingsicon.png'))

        self.bouncemultconfig.valueChanged.connect(self.bconfpressed)
        self.savebutton.clicked.connect(self.savesettings)
        self.exitbutton.clicked.connect(sys.exit)
        self.show()

    def savesettings(self):
        FreeFall.gravforce = int(self.gravforceconfig.text())
        FreeFall.physobjsize = int(self.physobjsizeconfig.text())
        # красивый ui - пользователь видит 5%, которые приводятся к множителю в 0.95
        FreeFall.bouncemult = 1 - (int(self.bouncemultconfig.value()) / 100)
        FreeFall.tickrate = int(self.tickrateconfig.text())
        self.close()

    def bconfpressed(self):
        self.percentlabel.setText(str(self.bouncemultconfig.value()) + "%")


class FreeFall:
    def __init__(self):
        # константы
        self.WHITE = (250, 241, 245)
        self.BLUE = (25, 41, 88)
        self.framesize = 10
        self.size = [1000, 800]
        self.middle = self.size[0] // 2
        self.fontsize = 50

        # переменные
        self.paused = False
        self.physobj = []

        # Первым делом соберем настройки пользователя
        self.configscreen()
        self.screen = pygame.display.set_mode(self.size)
        self.freefallmain()

    def configscreen(self):
        app = QApplication(sys.argv)
        window = FreeFallSettings()
        app.exec_()

    def drawphysobj(self):
        # physobj[position][0][1] это y(игрек) координата объекта
        for position in range(len(self.physobj)):
            # проверка паузы
            if not self.paused:
                t = self.physobj[position][1]
                if t > 0:
                    self.physobj[position][0][1] += self.gravforce * t * t  # свободное падение, h -= (gt^2)/2
                else:
                    self.physobj[position][0][1] -= self.gravforce * t * t  # отскок если t < 0
                    # КОСТЫЛЬ, if потому что t^2 == (-t)^2
                    # приходится расписывать действия на оба случая (t > 0 и t < 0)

                # проверяем, ударился ли объект о поверхность
                border = self.size[1] - self.framesize - self.physobjsize
                if self.physobj[position][0][1] > border:
                    # выталкиваем объект из-за границ
                    self.physobj[position][0][1] = border
                    if self.physobj[position][1] * self.bouncemult > 0.001:
                        self.physobj[position][1] *= -self.bouncemult  # объект отскакивает назад, теряя скорость
                    else:
                        self.physobj[position][1] = 0
                self.physobj[position][1] += round(1 / self.tickrate, 3)
                # плавное прибавление переменной t, привязанное к FPS

            pygame.draw.circle(self.screen, self.WHITE, self.physobj[position][0], self.physobjsize)

    def reloadscreen(self):
        width = self.size[0]
        height = self.size[1]
        # рисуем красивую рамочку по длине экрана
        self.screen.fill(self.BLUE)
        pygame.draw.rect(self.screen, self.WHITE, pygame.Rect((0, 0), (width, height)), self.framesize)

    def freefallmain(self):

        pygame.init()
        pygame.font.init()

        pygame.display.set_caption('Свободное падение')
        pygame.display.set_icon(pygame.image.load("pics/icon.png"))
        clock = pygame.time.Clock()

        my_font = pygame.font.SysFont('Arial', self.fontsize)
        pausetext = my_font.render('PAUSED', False, self.WHITE)
        pausecenter = pausetext.get_rect(center=(self.middle, self.fontsize + 30))

        running = True
        while running:
            self.reloadscreen()
            self.drawphysobj()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.physobj.append([list(pos), 0])
                    # записываем в список физических объектов положение объекта и переменную t

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    if event.key == pygame.K_r:
                        self.physobj = []
                    if event.key == pygame.K_s:
                        self.paused = True
                        self.screen.blit(pausetext, pausecenter)
                        pygame.display.flip()
                        self.configscreen()
                    if event.key == pygame.K_BACKSPACE and len(self.physobj) > 0:
                        self.physobj.pop()
            if self.paused:
                self.screen.blit(pausetext, pausecenter)
            pygame.display.flip()
            clock.tick(self.tickrate)
        pygame.quit()
