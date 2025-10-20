from PIL import Image, ImageOps
from dataclasses import dataclass
import cv2
import numpy as np
from manim import *
from manim_slides import Slide
from spectrum_data_loader import load_df_data
from scipy.signal import savgol_filter

HOME = r"figures"
TITLE_SIZE = 50
NORMAL_SIZE = 30
TINY_SIZE = 15

class SlidesControl(Slide):
    # ------------- funciones control de contenido de diapositivas -------------
    # Cambiar número de diapositiva
    def update_canvas(self):
        self.counter += 1
        old_slide_number = self.canvas["slide_number"]
        new_slide_number = Text(f"{self.counter}").move_to(old_slide_number)
        self.play(Transform(old_slide_number, new_slide_number))

    def clear_slide_content(self):
        trash_can = [mobj for mobj in self.mobjects
                     if mobj not in [self.canvas["title"], self.canvas["slide_number"]]]
        self.play(FadeOut(*trash_can))

    def clear_allSlide_wipe(self, next_slide_content: list):
        trash_can = [mobj for mobj in self.mobjects
                     if mobj not in [self.canvas['slide_number']]] # solo deja slide_num en escena
        self.wipe(Group(*trash_can), next_slide_content, run_time=1.2)

    def clear_allSlide_fade(self):
        trash_can = [FadeOut(mob) for mob in self.mobjects
                     if mob not in [self.canvas["slide_number"]]] # solo deja slide_num en escena
        self.play(*trash_can)
    
    def section_title_animation(self, str_title: str):
        # Aparece el nombre de la sección pegado a la izquiera muy grande y después desaparece
        section_title = Tex(str_title, tex_environment='flushleft', font_size=TITLE_SIZE+15).to_edge(LEFT)

        self.play(FadeIn(section_title))
        self.next_slide()
        self.play(FadeOut(section_title))

@dataclass
class VideoStatus:
    time: float = 0
    videoObject: cv2.VideoCapture = None
    def __deepcopy__(self, memo):
        return self

class VideoMobject(ImageMobject):
    '''
    Following a discussion on Discord about animated GIF images.
    Modified for videos
    Parameters
    ----------
    filename
        the filename of the video file
    imageops
        (optional) possibility to include a PIL.ImageOps operation, e.g.
        PIL.ImageOps.mirror
    speed
        (optional) speed-up/slow-down the playback
    loop
        (optional) replay the video from the start in an endless loop
    https://discord.com/channels/581738731934056449/1126245755607339250/1126245755607339250
    2023-07-06 Uwe Zimmermann & Abulafia
    2024-03-09 Uwe Zimmermann
    '''
    def __init__(self, filename=None, imageops=None, speed=1.0, loop=False, **kwargs):
        self.filename = filename
        self.imageops = imageops
        self.speed    = speed
        self.loop     = loop
        self._id = id(self)
        self.status = VideoStatus()
        self.status.videoObject = cv2.VideoCapture(filename)

        self.status.videoObject.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, frame = self.status.videoObject.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            img = Image.fromarray(frame)

            if imageops != None:
                img = imageops(img)
        else:
            img = Image.fromarray(np.uint8([[63, 0, 0, 0],
                                        [0, 127, 0, 0],
                                        [0, 0, 191, 0],
                                        [0, 0, 0, 255]
                                        ]))
        super().__init__(img, **kwargs)
        if ret:
            self.add_updater(self.videoUpdater)

    def videoUpdater(self, mobj, dt):
        if dt == 0:
            return
        status = self.status
        status.time += 1000*dt*mobj.speed
        self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
        ret, frame = self.status.videoObject.read()
        if (ret == False) and self.loop:
            status.time = 0
            self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
            ret, frame = self.status.videoObject.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # needed here?        
            img = Image.fromarray(frame)

            if mobj.imageops != None:
                img = mobj.imageops(img)
            mobj.pixel_array = change_to_rgba_array(
                np.asarray(img), mobj.pixel_array_dtype
            )

def crear_diagrama_sensor_base():
    """
    Crea y devuelve los componentes Mobject base para el diagrama del sensor.
    Retorna un diccionario con los componentes para fácil acceso.
    """
    # Fuente de luz (LED)
    led_body = Circle(radius=0.45, color=WHITE, fill_opacity=0.3)
    led_emitter = Dot(color=RED_E, radius=0.12).move_to(led_body.get_right())
    led_group = VGroup(led_body, led_emitter).move_to(LEFT * 5.5)
    led_label = Tex('Fuente de Luz', font_size=NORMAL_SIZE - 4).next_to(led_group, UP, buff=0.3)

    # Muestra
    sample_cuvette = Rectangle(width=1.5, height=2.5, color=BLUE_C, fill_opacity=0.2).move_to(LEFT * 1.5)
    sample_label = Tex('Muestra', font_size=NORMAL_SIZE - 4).next_to(sample_cuvette, UP, buff=0.3)
    
    # Selector de Onda (Filtro) - Inicialmente invisible
    filtro = Rectangle(width=0.25, height=0.75, color=TEAL, fill_opacity=0.4
                       ).move_to(VGroup(led_body, sample_cuvette).get_center()).set_opacity(0)
    filtro_label = Tex('Selector de Onda', font_size=NORMAL_SIZE - 4).next_to(filtro, UP, buff=0.3).set_opacity(0)

    # Detector
    photodetector_area = Rectangle(width=0.8, height=1.8, color=TEAL_E, fill_opacity=0.7)
    photodetector_base = Rectangle(width=1.0, height=0.25, color=GRAY).next_to(photodetector_area, DOWN, buff=0)
    photodetector_group = VGroup(photodetector_area, photodetector_base).move_to(RIGHT * 1.5)
    photodetector_label = Tex('Detector', font_size=NORMAL_SIZE - 4).next_to(photodetector_group, UP, buff=0.3)

    # Procesador de Señal - Inicialmente invisible
    procesador = Square(side_length=1.6, color=ORANGE, fill_opacity=0.3).to_edge(RIGHT, buff=0.8)
    procesador_label = Tex(r"Procesador\\de Señal", font_size=NORMAL_SIZE - 4).move_to(procesador).set_opacity(0)

    # Devolver componentes en un diccionario para un acceso claro
    componentes = {
        "fuente": led_group, "fuente_label": led_label,
        "muestra": sample_cuvette, "muestra_label": sample_label,
        "selector": filtro, "selector_label": filtro_label,
        "detector": photodetector_group, "detector_label": photodetector_label,
        "procesador": procesador, "procesador_label": procesador_label,
    }
    
    return componentes

class ManimGraph:
    """
    Una clase de ayuda para simplificar la creación de gráficas de espectros en Manim.
    Esta versión desacopla el graficado de la creación de la leyenda para mayor flexibilidad.
    """
    def __init__(self, escena):
        self.escena = escena
        self.axes = None
        self.x_range = None
        self.y_range = None

    def setup_axes(self, x_label, y_label, x_range, y_range, x_length=8, y_length=5, **kwargs):
        """
        Crea y configura los ejes de la gráfica.
        """
        self.x_range = x_range
        self.y_range = y_range
        
        decimal_config = {"group_with_commas": False}

        self.axes = Axes(
            x_range=self.x_range, y_range=self.y_range,
            x_length=x_length, y_length=y_length,
            axis_config={"include_tip": False, "color": GREY},
            x_axis_config={"decimal_number_config": decimal_config},
            y_axis_config={"decimal_number_config": decimal_config},
            **kwargs
        ).add_coordinates()
        
        x_ax_label = self.axes.get_x_axis_label(Tex(x_label), edge=DOWN, direction=DOWN, buff=0.35)
        y_ax_label = self.axes.get_y_axis_label(Tex(y_label).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.35)
        
        self.axes_with_labels = VGroup(self.axes, x_ax_label, y_ax_label)
        return self.axes_with_labels

    def plot_spectrum(self, filepath, color, smooth=False):
        """
        Carga, filtra y grafica los datos. Devuelve solo el objeto de la gráfica.
        """
        if self.axes is None:
            raise Exception("Debes llamar a setup_axes() antes de plot_spectrum()")

        df = load_df_data(filepath)
        x_min, x_max = self.x_range[:2]
        filtered_df = df[(df.iloc[:, 0] >= x_min) & (df.iloc[:, 0] <= x_max)]
        
        x_data = filtered_df.iloc[:, 0].to_numpy()
        y_data = filtered_df.iloc[:, 1].to_numpy()
        
        y_min, y_max = self.y_range[:2]
        y_data = np.clip(y_data, y_min, y_max)
        
        if smooth:
            window_length = min(15, len(y_data))
            if window_length % 2 == 0: window_length -= 1
            if window_length > 1:
                y_data = savgol_filter(y_data, window_length=window_length, polyorder=2)

        graph = self.axes.plot_line_graph(
            x_values=x_data, y_values=y_data,
            line_color=color, add_vertex_dots=False
        )
        
        return graph

    def create_legend(self, legend_items, position=UR, buff=0.2):
        """
        Crea un bloque de leyenda a partir de una lista de textos y colores.
        Args:
            legend_items (list): Lista de diccionarios, ej. [{"text": "Mi Curva", "color": BLUE}]
            position (np.ndarray): Esquina del gráfico para anclar la leyenda (UR, UL, DR, DL).
            buff (float): Margen interior desde la esquina.
        """
        if self.axes is None:
            raise Exception("Debes configurar los ejes con setup_axes() primero.")

        labels = VGroup()
        for item in legend_items:
            label = Tex(item["text"], color=item["color"], font_size=28)
            labels.add(label)
        
        # Alinear las etiquetas verticalmente a la izquierda
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # Posicionar el bloque de leyenda dentro del gráfico
        opposite_direction = -position
        labels.next_to(self.axes.get_corner(position), opposite_direction, buff=buff)
        
        return labels