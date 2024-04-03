from service.vao import VAO
from service.texture import Texture


class Mesh:
    """
    Класс представляющий сетку для отображения объектов.
    Объект представляет собой совокупность:
    Вершин и индексов, определяющих форму, структуру и текстуру объекта.
    """
    def __init__(self, app):
        """
        Метод инициализации объекта сетки.
        :param GraphicsEngine app: Объект приложения.
        """
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)

    def destroy(self):
        """
        Метод уничтожения объекта путем освобождения связанных ресурсов.
        """
        self.vao.destroy()
        self.texture.destroy()
