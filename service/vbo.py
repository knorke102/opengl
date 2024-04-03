import numpy as np


class VBO:
    """
    Класс представляющий работу с буфером вершин (VBO).
    """
    def __init__(self, ctx):
        """
        Метод инициализации объекта буфера вершин (VBO).
        :param moderngl.Context ctx: Контекст moderngl.
        """
        self.vbos = {
            'cube': CubeVBO(ctx),
            'skybox': SkyBoxVBO(ctx)
        }

    def destroy(self):
        """
        Метод уничтожения объекта.
        """
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    """
    Базовый класс для работы с буфером вершин (VBO).
    """
    def __init__(self, ctx):
        """
        Метод инициализации базового объекта буфера вершин (VBO).
        :param moderngl.Context ctx: Контекст moderngl.
        """
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format = None
        self.attribs = None

    def get_vertex_data(self):  ...

    def get_vbo(self):
        """
        Метод создания и возвращения буфера вершин.
        :return moderngl.Buffer: Созданный буфер вершин.
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        """
        Метод уничтожения объекта.
        """
        self.vbo.release()


class CubeVBO(BaseVBO):
    """
    Класс для создания буфера вершин для куба.
    """
    def __init__(self, ctx):
        """
        Метод инициализации объекта буфера вершин для куба.
        :param moderngl.Context ctx: Контекст moderngl.
        """
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Метод создания данных вершин на основе координат вершин и индексов.
        :param list vertices: Список координат вершин.
        :param list indices: Список индексов вершин.
        :return numpy.ndarray: Данные вершин.
        """
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        """
        Метод генерации данных вершин для куба.
        :return: numpy.ndarray: Данные вершин для куба.
        """
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]

        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]

        vertex_data = self.get_data(vertices, indices)

        normals = np.array(normals, dtype='f4').reshape(36, 3)
        vertex_data = np.hstack([normals, vertex_data])

        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class SkyBoxVBO(BaseVBO):
    """
    Класс для создания буфера вершин для пола.
    """
    def __init__(self, ctx):
        """
        Метод инициализации объекта буфера вершин для пола.
        :param moderngl.Context ctx: Контекст moderngl.
        """
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    def get_vertex_data(self, z=0.9999):
        """
        Получение данных вершин для пола.
        :param float z: Координата z, чтобы пол находился позади всех других объектов.
        :return numpy.ndarray: Данные вершин для пола.
        """
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype='f4')
        return vertex_data
