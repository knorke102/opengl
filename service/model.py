import glm


class BaseModel:
    """
    Класс представляющий основную функциональность для создания и визуализации моделей.
    """
    def __init__(self, app, vao_name, tex_id,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """
        Метод инициализации объекта модели.
        :param GraphicsEngine app: Объект приложения.
        :param str vao_name: Имя объекта массива вершин (VAO), связанного с моделью.
        :param int tex_id: Идентификатор текстуры, связанной с моделью.
        :param pos: Позиция модели (x, y, z).
        :param rot: Углы поворота модели по осям (x, y, z) в радианах.
        :param scale: Масштаб модели по осям (x, y, z).
        """
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3(*map(glm.radians, rot))
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        self.texture = None
        self.shadow_vao = None
        self.shadow_program = None
        self.depth_texture = None

    def get_model_matrix(self, z=(0, 0, 1), y=(0, 1, 0), x=(1, 0, 0)):
        """
        Метод получения идентификационной матрицы в качестве матрицы модели.
        :param z: Направление оси Z модели.
        :param y: Направление оси Y модели.
        :param x: Направление оси X модели.
        :return glm.mat4: Идентификационная матрица.
        """
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(z))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(y))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(x))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def update(self): ...

    def render(self):
        """
        Метод визуализации модели.
        Обновление ее атрибутов и отрисовки связанный с ней объект массива вершин.
        """
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    """
    Класс представляющий наследуемую функциональность для создания и визуализации моделей.
    """
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

        self.on_init()

    def update(self):
        """
        Метод обновляет данные в шейдере перед его использованием для рендеринга.
        """
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        """
        Обновление данных для рендеринга теней.
        """
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        """
        Рендеринг модели для теней.
        """
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        """
        Метод для установки начальных значений для форм и матриц шейдеров.
        """
        self.program['m_view_light'].write(self.app.light.m_view_light)
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))

        # depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)

        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)

        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)

        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    """
    Класс предоставляет основную функциональность для создания и визуализации куба.
    """
    def __init__(self, app, vao_name='cube', tex_id=0,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(BaseModel):
    """
    Класс предоставляет основную функциональность для создания и визуализации пола.
    """
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(self.camera.m_view)
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)


class OtherModel(ExtendedBaseModel):
    """
    Класс предоставляет основную функциональность для создания и визуализации 3д-модели.
    """
    def __init__(self, app, vao_name='other_model', tex_id='other_model',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(10, 10, 10)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
