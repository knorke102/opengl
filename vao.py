from vbo import VBO
from shader import ShaderProgram


class VAO:
    """
    Класс представляющий работу с объектами массива вершин (VAO).
    """
    def __init__(self, ctx):
        """
        Метод инициализации объекта массива вершин (VAO).
        :param moderngl.Context ctx: Контекст moderngl.
        """
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {
            'cube': self.get_vao(
                program=self.program.programs['default'],
                vbo=self.vbo.vbos['cube']
            )
        }

    def get_vao(self, program, vbo):
        """
        Метод создания объекта массива вершин на основе заданных шейдеров и буфера вершин.
        :param moderngl.Program program: Скомпилированный шейдер.
        :param vbo: Буфер вершин.
        :return moderngl.VertexArray: Созданный объект массива вершин.
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        """
        Метод уничтожения объекта путем освобождения связанных ресурсов.
        """
        self.vbo.destroy()
        self.program.destroy()
