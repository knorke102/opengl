import pygame as pg


class Texture:
    """
    Класс представляющий работу с текстурами.
    """
    def __init__(self, app):
        """
        Метод инициализации объекта текстуры.
        :param GraphicsEngine app: Объект приложения.
        """
        self.app = app
        self.ctx = app.ctx
        self.dir_textures = 'textures'
        self.textures = {
            0: self.get_texture(path=f'{self.dir_textures}/img.png'),
            1: self.get_texture(path=f'{self.dir_textures}/img_1.png'),
            2: self.get_texture(path=f'{self.dir_textures}/img_2.png')
        }

    def get_texture(self, path):
        """
        Метод загрузки текстур из файлов.
        :param str path: Путь к файлу изображения.
        :return moderngl.Program: Скомпилированная текстура.
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(),
                                   components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture

    def destroy(self):
        """
        Метод уничтожения объекта путем освобождения связанных ресурсов.
        """
        [tex.release() for tex in self.textures.values()]
