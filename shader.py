

class ShaderProgram:
    """
    Класс представляющий работу со шейдерами.
    """
    def __init__(self, ctx):
        """
        Метод инициализации объекта шейдеров.
        :param moderngl.Context ctx: Контекст moderngl.
        """
        self.ctx = ctx
        self.dir_shaders = 'shaders'
        self.programs = {
            'default': self.get_program('default')
        }

    def get_program(self, path):
        """
        Метод загрузки шейдеров из файлов.
        :param str path: Название шейдера.
        :return moderngl.Program: Скомпилированный шейдер.
        """
        with open(f'{self.dir_shaders}/{path}.vert') as file:
            vertex_shader = file.read()

        with open(f'{self.dir_shaders}/{path}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        """
        Метод уничтожения объекта.
        """
        [program.release() for program in self.programs.values()]
