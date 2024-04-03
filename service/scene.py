from service.model import Cube, SkyBox, OtherModel


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
        self.skybox = SkyBox(app)

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

        # floor
        n, s = 20, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        # cube
        add(Cube(app, pos=(0, 0, 0), tex_id=1))

        add(OtherModel(app, pos=(0, 0, -10)))

    def render(self):
        """
        Метод визуализации сцены, отрисовывая все объекты в сцене.
        """
        for obj in self.objects:
            obj.render()

    def update(self): ...


class SceneRenderer:
    """
    Класс представляющий рендеринг сцены.
    """
    def __init__(self, app):
        """
        Метод инициализации объекта сцены.
        :param GraphicsEngine app: Объект приложения.
        """
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        """
        Рендеринг теней.
        """
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self):
        """
        Основной рендеринг сцены.
        """
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def render(self):
        """
        Общий процесс рендеринга сцены.
        """
        self.scene.update()
        self.render_shadow()
        self.main_render()

    def destroy(self):
        """
        Метод уничтожения объекта.
        """
        self.depth_fbo.release()
