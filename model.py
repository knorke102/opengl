import glm


class BaseModel:
    """
    Класс представляющий основную функциональность для создания и визуализации моделей.
    """
    def __init__(self, app, vao_name, tex_id):
        """
        Метод инициализации объекта модели.
        :param GraphicsEngine app: Объект приложения.
        :param str vao_name: Имя объекта массива вершин (VAO), связанного с моделью.
        :param int tex_id: Идентификатор текстуры, связанной с моделью.
        """
        self.app = app
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    @staticmethod
    def get_model_matrix():
        """
        Метод получения идентификационной матрицы в качестве матрицы модели.
        :return glm.mat4: Идентификационная матрица.
        """
        return glm.mat4()

    def update(self):
        """
        Метод обновления должен быть реализован в подклассах.
        """
        pass

    def render(self):
        """
        Метод визуализации модели.
        Обновление ее атрибутов и отрисовки связанный с ней объект массива вершин.
        """
        self.update()
        self.vao.render()


class Cube(BaseModel):
    """
    Класс предоставляет основную функциональность для создания и визуализации куба.
    """
    def __init__(self, app, vao_name='cube', tex_id=0):
        """
        Инициализация объекта куб.
        :param GraphicsEngine app: Объект приложения.
        :param str vao_name: Имя объекта массива вершин (VAO), связанного с моделью.
        :param int tex_id: Идентификатор текстуры, связанной с моделью.
        """
        super().__init__(app, vao_name, tex_id)
        self.texture = None
        self.on_init()

    def update(self):
        """
        Метод обновляет данные в шейдере перед его использованием для рендеринга куба.
        """
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self, texture=0):
        """
        Метод для установки начальных значений для форм и матриц шейдеров.
        :param int texture: Номер текстурного юнита для текстуры модели.
        """
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.texture.use()

        # init program
        self.program['u_texture_0'] = texture

        # mvp
        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
