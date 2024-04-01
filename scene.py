from model import Cube


class Scene:
    """
    Класс представляющий работу со сценой.
    """
    def __init__(self, app):
        """
        Метод инициализации объекта сцены.
        :param GraphicsEngine app: Объект приложения.
        """
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        """
        Метод добавление объекта в сцену.
        :param obj obj: Объект, который нужно добавить в сцену.
        """
        self.objects.append(obj)

    def load(self):
        """
        Метод загрузки начальных объектов в сцену.
        """
        app = self.app
        add = self.add_object

        # Add a cube to the scene
        add(Cube(app))

    def render(self):
        """
        Метод визуализации сцены, отрисовывая все объекты в сцене.
        """
        for obj in self.objects:
            obj.render()
