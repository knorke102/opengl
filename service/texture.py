import pygame as pg
import moderngl as mgl


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
        self.textures = {
            0: self.get_texture(path='textures/img.png'),
            1: self.get_texture(path='textures/img_1.png'),
            2: self.get_texture(path='textures/img_2.png'),
            'other_model': self.get_texture(path='textures/ball.png'),
            'skybox': self.get_texture_cube(path='textures/skybox/', ext='png'),
            'depth_texture': self.get_depth_texture()
        }

    def get_depth_texture(self):
        """
        Создание текстуры глубины.
        :return moderngl.Texture: Созданная текстура глубины.
        """
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, path, ext='png'):
        """
        Создание текстуры куба (SkyBox).
        :param path: Путь к файлам текстур куба.
        :param ext: Расширение файлов текстур.
        :return moderngl.TextureCube: Созданная текстура куба.
        """
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]

        textures = []
        for face in faces:
            texture = pg.image.load(path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path, anisotropy=32.0):
        """
        Метод загрузки текстур из файлов.
        :param str path: Путь к файлу изображения.
        :param float anisotropy: Уровень анизотропной фильтрации для текстуры.
        :return moderngl.Program: Скомпилированная текстура.
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = anisotropy
        return texture

    def destroy(self):
        """
        Метод уничтожения объекта путем освобождения связанных ресурсов.
        """
        [tex.release() for tex in self.textures.values()]
