import glm


class Light:
    """
    Класс представляющий источник света.
    Источник света может иметь различные параметры.
    Такие, как положение, цвет и интенсивность свечения.
    """
    def __init__(self, position=(50, 50, -10), color=(1, 1, 1), direction=(0, 0, 0),
                 ambient=0.1, diffuse=0.8, specular=1.0):
        """
        Метод инициализации объекта света.
        :param float position: Начальное положение источника света в координатах (x, y, z).
        :param float color: RGB-цвет источника света.
        :param float direction: Направление источника света.
        :param float ambient: Окружающий источник света.
        :param float diffuse: Рассеянный источник света.
        :param float specular: Отражающий источник света.
        """
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(direction)

        # Интенсивность света
        self.Ia = ambient * self.color
        self.Id = diffuse * self.color
        self.Is = specular * self.color

        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self, view=(0, 1, 0)):
        """
        :param float view: Направление, куда смотрит источник света (вектор в формате (x, y, z)).
        :return glm.mat4: Матрица вида для источника света.
        """
        return glm.lookAt(self.position, self.direction, glm.vec3(view))
