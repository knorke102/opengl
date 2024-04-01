import glm
import pygame as pg


class Camera:
    """
    Класс представляющий камеру для графического приложения.
    Камера используется для определения точки зрения в графическом пространстве.
    Она может перемещаться и поворачиваться для создания эффекта движения и взгляда от разных углов.
    """
    def __init__(self, app,
                 position=(0, 0, 4),
                 yaw=-90, pitch=0,
                 up=(0, 1, 0), right=(1, 0, 0), forward=(0, 0, -1)
                 ):
        """
        Метод инициализации объекта камеры.
        :param GraphicsEngine app: Объект приложения.
        :param float position: Начальное положение камеры в координатах (x, y, z).
        :param float yaw: Начальный угол рыскания (горизонтальный поворот) в градусах.
        :param float pitch: Начальный угол тангажа (вертикальный поворот) в градусах.
        :param float up: Вектор направления "вверх" камеры.
        :param float right: Вектор направления "вправо" камеры.
        :param float forward: Вектор направления "вперед" камеры.
        """
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(up)
        self.right = glm.vec3(right)
        self.forward = glm.vec3(forward)
        self.yaw = yaw
        self.pitch = pitch
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def update(self):
        """
        Метод изменяет положение и ориентацию камеры.
        Путем перемещения, поворота и обновления векторов направления.
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def update_camera_vectors(self, right=(0, 1, 0)):
        """
        Метод изменяет векторы движения камеры вперед, вправо и вверх.
        На основе углов рыскания и тангажа.
        :param float right: Вектор направления "вправо" камеры в трехмерном пространстве (x, y, z).
        """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(right)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate(self, sensitivity=0.04, max_pitch=-89, min_pitch=89):
        """
        Метод изменяет угол рыскания и тангажа камеры в ответ на движение мыши.
        :param float sensitivity: Чувствительность мыши, определяющая скорость поворота камеры.
        :param float max_pitch: Максимальный угол тангажа (вертикальный поворот) в градусах.
        :param float min_pitch: Минимальный угол тангажа (вертикальный поворот) в градусах.
        """
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * sensitivity
        self.pitch -= rel_y * sensitivity
        self.pitch = max(max_pitch, min(min_pitch, self.pitch))

    def move(self, speed=0.005):
        """
        Метод перемещает камеру в зависимости от нажатых клавиш на клавиатуре.
        :param float speed: Скорость передвижения камеры.
        """
        velocity = speed * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        """
        Метод определяет положение и ориентацию камеры в трехмерном пространстве.
        :return glm.mat4: Матрица просмотра, представляющая положение и ориентацию камеры.
        """
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self, fov=50, near=0.1, far=100):
        """
        Метод преобразования трехмерных координат в двухмерные для отображения на экране.
        :param float fov: Определяет угол обзора камеры.
        :param float near: Определяет ближнюю границу видимости объектов.
        :param float far: Определяет дальнюю границу видимости объектов.
        :return glm.mat4: Проекционная матрица, используемая для преобразования координат.
        """
        return glm.perspective(glm.radians(fov), self.aspect_ratio, near, far)
