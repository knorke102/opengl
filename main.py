import sys
import pygame as pg
import moderngl as mgl
from mesh import Mesh
from scene import Scene
from light import Light
from camera import Camera


class GraphicsEngine:
    """
    Класс представляющий графический движок для создания и управления графическими сценами.

    Графический движок используется для:
    Инициализации графического контекста OpenGL.
    Создания объектов света, камеры, сцены и других элементов.
    Также для обновления и отображения графики.
    """
    def __init__(self, win_size=(1600, 900)):
        """
        Метод инициализации объекта графического движка.
        :param tuple win_size: Начальный размер окна в формате (ширина, высота).
        """
        self.WIN_SIZE = win_size

        # Настройки контекста OpenGL
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Создание контекста OpenGL
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Настройки времени
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Инициализация базовых объектов
        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)

    def check_events(self):
        """
        Метод проверяет наличие событий pygame в цикле и обрабатывает их.
        Если пользователь закрывает окно или нажимает клавишу Escape, приложение завершает работу.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def get_time(self, time=0.001):
        """
        Метод обновляет текущее время и вычисляет разницу во времени с предыдущим кадром.
        :param float time: Время в миллисекундах.
        """
        self.time = pg.time.get_ticks() * time

    def render(self, red=0.08, green=0.16, blue=0.18, alpha=1.0):
        """
        Метод выполняет рендеринг сцены.
        :param float red: Компонента красного цвета фона.
        :param float green: Компонента зеленого цвета фона.
        :param float blue: Компонента синего цвета фона.
        :param float alpha: Прозрачность фона.
        """
        self.ctx.clear(color=(red, green, blue, alpha))
        self.scene.render()
        pg.display.flip()

    def run(self, fps=60):
        """
        Метод запускает основной цикл визуализации сцены.
        :param int fps: Количество сменяемых кадров за одну секунду.
        """
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(fps)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
