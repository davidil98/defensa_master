from manim import *
from manim_slides import Slide
import locale
from datetime import datetime as dt
import cv2 # needs opencv-python https://pypi.org/project/opencv-python/
from PIL import Image, ImageOps
from dataclasses import dataclass

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


HOME = r"figures"
TITLE_SIZE = 35
NORMAL_SIZE = 28
TINY_SIZE = 15
class Presentation(Slide):
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

    # -------------- CONTENIDO DE PRESENTACION -------------------
    def construct(self):
        # SECCIONES
        self.portada() # NECESITA OPTIMIZACION PARA HTML, no poner tantas animaciones
        self.intro()
        self.antecedentes()
        self.analisis_critico_antecedentes()
        self.aportacion_cientifica()
        self.hipotesis()
        self.objetivo_general()
        self.objetivos_específicos()
        self.metodologia()
        self.resultados()
        self.discusion_conclusiones()
        self.bibliografia()
        self.agradecimientos()

    def portada(self):
        # Texto
        university_name = Tex(r'{\sc Universidad Autónoma de Nuevo León\\Facultad de Ciencias Químicas}',
                              font_size=33)
        posgrade_name = Tex(r'{\sc Maestría en Ciencias con Orientación en Química de los Materiales}',
                            font_size=28)
        titulo_tema = Tex(r'{\bf\sc Desarrollo de un Sensor Optoelectrónico Basado en Puntos Cuánticos de Grafeno para la Detección de Nitritos en Agua de Pozos Someros.}', # Corregido: "de"
                          font_size = 38)
        author_name = Tex(r'{\sc Autor: L.Q.I.\,David Ibarra Luna}',
                           font_size = 28)
        supervisor_name = Tex(r'{\sc Directora: Dra.\,Ma. Idalida del Consuelo Gómez de la Fuente}',
                              font_size = 23)
        cosupervisors_names = Tex(r'{\sc Co-directores:\\Dra.\,Oxana Visilievna Kharissova \hspace{0.5cm} Dr.\,Luis Arturo Obregón Zúñiga}',
                                  font_size=23)

        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8') # Localización
        fecha_actual = dt.now()
        location = 'Cd. Universitaria, San Nicolás de los Garza, N.L.'
        location_and_date = Tex(location +'\n'+ fecha_actual.strftime(' %A, %d de %B del %Y'),
                                font_size = 20)

        # Imagenes
        logo_uanl = ImageMobject(f'{HOME}\\UANL_logo.png').scale(0.15)
        logo_fcq = ImageMobject(f'{HOME}\\FCQ_logo.png')

        # Posicionar
        logo_uanl.to_corner(UR, buff=0.2)
        logo_fcq.to_corner(UL, buff=0.2)
        university_name.to_edge(UP, buff=0.6)
        posgrade_name.next_to(university_name, DOWN, buff=0.5)
        author_name.next_to(titulo_tema, DOWN, buff=0.6)
        supervisor_name.next_to(author_name, DOWN, buff=0.2)
        cosupervisors_names.next_to(supervisor_name, DOWN, buff=0.2)
        location_and_date.to_edge(DOWN, buff=0.2)

        # grupos
        logos = Group(logo_fcq, logo_uanl)
        info = VGroup(university_name, posgrade_name, author_name, supervisor_name, cosupervisors_names, location_and_date)

        # Poner en escena
        self.play(
            LaggedStart(
                FadeIn(logos[0], run_time=1.5),
                FadeIn(logos[1], run_time=1.5),
                lag_ratio=0.3
            )
        )

        self.play(Write(titulo_tema))
        self.play(Succession((FadeIn(texto) for texto in info), lag_ratio=0.8))

        # Borrar escena
        self.next_slide()
        self.play([FadeOut(mob) for mob in self.mobjects])

    def intro(self):
        #SUB-SECCIONES DE INTRO
        self.introAgua()
        self.waterquality()
        self.nitritos()
        self.deteccionNitritos()
        self.sensoresOp()
        self.intro_nanomateriales()
        self.nanomateriales()
        self.gqd()
        self.gqd_quenching()
        self.cierre_intro()

    def introAgua(self):
        title_size = 55
        normal_size = 25

        # canvas
        slide_title = Tex('Introducción', font_size=title_size).to_corner(UL)
        self.counter = 1
        slide_number = Text("1").to_corner(DL)
        self.add_to_canvas(title=slide_title,slide_number=slide_number)

        # contenido texto
        tex = Paragraph(
            'Históricamente, el agua siempre ha sido vital para garantizar\nla prosperidad en los asentamientos humanos.',
            alignment='right', line_spacing=0.8, font_size=normal_size
        ).to_corner(UR, buff=0.50)

        box = SurroundingRectangle(Group(slide_title, tex), color=WHITE, buff=0.2)

        img1 = ImageMobject(f'{HOME}\\watersample1.jpg').scale(1.8).shift(LEFT*3.5).shift(DOWN)
        img2 = ImageMobject(f'{HOME}\\watersample2.jpg').scale(1.8).shift(RIGHT*3.5).shift(DOWN)

        quoting = Tex('El aseguramiento de la calidad del agua se convierte en un desafío constante.',
                      font_size=normal_size).to_edge(DOWN, buff=0.5)

        # Poner en escena
        self.play(FadeIn(slide_number), Write(slide_title))
        self.play(Succession(
            FadeIn(tex),
            Create(box),
            FadeIn(img1),
            FadeIn(img2),
            FadeIn(quoting),
            )
            )

        # Borrar escena (excepto canvas)
        self.next_slide()
        trash_can = [mobj for mobj in self.mobjects
                     if mobj not in [self.canvas["title"], self.canvas["slide_number"]]]
        self.wipe(Group(*trash_can), [])

    def waterquality(self):
        # Contenido
        slide_title_calidad = Title(r'Calidad del agua',
                            font_size=TITLE_SIZE).to_corner(UL)
        tex = Tex('Las fluctuaciones en la calidad del agua dependen de sus fuentes:',
                  font_size=NORMAL_SIZE).next_to(slide_title_calidad, DOWN, buff=1)
        listing = BulletedList('Ríos y arroyos', 'Lagos y manantiales', 'Agua subterránea (pozos someros)',
                               font_size=NORMAL_SIZE
                               ).next_to(tex ,DOWN, buff=0.8)

        # poner en escena. Inicia con la slide en negro excepto canvas
        self.update_canvas() # actualiza num_slide (canvas)
        self.play(Transform(self.canvas['title'], slide_title_calidad)) # actualizar titulo (canvas)
        self.play(FadeIn(tex), FadeIn(listing))
        self.next_slide() # Remarcar siguiente titulo
        self.play(listing.animate.fade_all_but('Agua subterránea (pozos someros)'))
        self.play(listing.animate.set_color_by_tex('Agua subterránea (pozos someros)', RED))
        self.next_slide(notes='El agua subterránea suele ser de las más accesibles para los asentamientos, por ejemplo, los pozos someros') # Quitar todo de escena
        self.play(FadeOut(*[mobj for mobj in self.mobjects
                            if mobj not in [listing, self.canvas["slide_number"]]]))

        # ------------------------ pozos someros ----
        # siguiente titulo
        shallow_title = Title('Agua subterránea (pozos someros)',
                              font_size=TITLE_SIZE)
        # contenido
        img_shallow_diagram = ImageMobject(f'{HOME}\\shallow_well_diagram.png').scale(2)
        description_diagram = Tex('Un pozo somero es una excavación relativamente poco profunda en el suelo para extraer agua del nivel freático.',
                                  font_size=NORMAL_SIZE).next_to(img_shallow_diagram, DOWN, buff=0.5)
        description_diagram2 = Tex('Su bajo coste de operación, almacenamiento y construcción lo hacen una opción viable y recurrente.',
                                   font_size=NORMAL_SIZE).next_to(img_shallow_diagram, DOWN, buff=0.5)

        self.update_canvas()
        self.canvas['title'] = shallow_title
        self.play(ReplacementTransform(listing[2], shallow_title))
        self.add(shallow_title)
        self.play(FadeOut(*[mobj for mobj in self.mobjects
                    if mobj not in [self.canvas['title'], self.canvas["slide_number"]]]))
        self.play(FadeIn(img_shallow_diagram, description_diagram))
        self.next_slide() # cambiar descripcion del diagrama
        self.play(Transform(description_diagram, description_diagram2))
        self.next_slide() # Quita contenido de la diapositiva e introducir siguiente
        self.clear_slide_content()

        #------------- Crisis hídrica y usos pozos someros ---------------
        # Contenido
        slide_title_crisis = Tex('Crisis hídrica, Nuevo León 2022',
                                 font_size=TITLE_SIZE).to_corner(UL, buff=0.5)
        crisis_tex = Tex('La falta de lluvias ocasionó niveles críticos en el almacenamiento de las Presas Cerro Prieto y La Boca.',
                         font_size=NORMAL_SIZE).to_edge(DOWN, buff=0.5)
        img_presa1 = ImageMobject(f'{HOME}\\cerro_prieto_dry.jpg').scale(0.5).shift(LEFT*3.5)
        img_presa2 = ImageMobject(f'{HOME}\\presa_laBoca_seco.jpg').scale(0.5).shift(RIGHT*3.5)
        # Después de limpiar contenido
        plan_crisis_tex = Tex('Las primeras acciones de gobierno fueron restaurar e incorporar pozos someros al suministro de agua.',
                              font_size=NORMAL_SIZE).to_edge(DOWN, buff=0.5)
        img_gob_pozos = ImageMobject(f'{HOME}\\gob_pozos_someros.jpg').scale(0.6)

        # Poner en escena
        self.update_canvas() # cambia num de diapositiva
        self.play(Transform(self.canvas['title'], slide_title_crisis)) # Transforma títutlo
        self.play(Succession(
            FadeIn(crisis_tex),
            FadeIn(img_presa1),
            FadeIn(img_presa2)
        ))
        # Cambiar contenido
        self.next_slide()
        self.clear_slide_content()
        self.play(Succession(
            FadeIn(plan_crisis_tex),
            FadeIn(img_gob_pozos)
        ))

    def nitritos(self):
        # Contenido
        slide_title_nitrites = Title('Nitritos en agua', font_size=TITLE_SIZE)
        tex_content_nitrite = Tex('Se considera el contaminante más extendido en las aguas subterráneas.\n',
                      'Debido a que el nitrato es soluble y móvil, es propenso a filtrarse\n',
                      'a través del suelo al infiltrarse agua.', font_size=NORMAL_SIZE, tex_environment="flushleft"
                      ).next_to(slide_title_nitrites, DOWN, buff=1)
        bibliography = Tex('Spalding, R. F.; Exner, M. E. Occurrence of nitrate in groundwater\n',
                           'a review. J. Environ. Qual. 1993, 22, 392-402.', font_size=TINY_SIZE,
                           tex_environment='flushleft'
                           ).next_to(self.canvas['slide_number'], RIGHT, buff=0.5)

        next_content_list = [slide_title_nitrites, tex_content_nitrite, bibliography]
        # cambio de escena
        nitrites_diagram = ImageMobject(f'{HOME}\\nitrites_diagram.jpg').scale(1.5)
        bibliography_diagram = Tex('Verma A, Sharma A, Kumar R, Sharma P. Nitrate contamination in groundwater and\n',
                                   'associated health risk assessment for Indo-Gangetic Plain, India. Groundw Sustain Dev [Internet].\n',
                                    '2023;23(100978):100978. Available from: http://dx.doi.org/10.1016/j.gsd.2023.100978',
                                    font_size=TINY_SIZE, tex_environment='flushleft').next_to(self.canvas['slide_number'], RIGHT, buff=0.5)
        # cambio de escena
        effects_nitrites = Tex('La exposición prolongada puede provocar:',
                               font_size=35, tex_environment='flushleft').next_to(slide_title_nitrites,DOWN, buff=1)
        effects_nitrites_bullet = BulletedList('Metahemoglobinemia en infantes',
                                               'Dificultades de gestación',
                                               'Problemas de tiroides',
                                               'Problemas asociados al cáncer', font_size=NORMAL_SIZE
                                               ).next_to(effects_nitrites, DOWN, buff=0.5)
        bibliography_effects_nitrites = Tex(
            'Galaviz-Villa I, et al. Presence of nitrates and nitrites in water for human consumption\n',
            'and their impact on public health in sugarcane-producing areas. Tropical and Subtropical\n',
            'Agroecosystems [Internet]. 2011 [citado el 24 de mayo de 2025] ;13(3):381–8. Disponible en:\n',
            'https://www.revista.ccba.uady.mx/ojs/index.php/TSA/article/view/1273', font_size=TINY_SIZE, tex_environment='flushleft'
        ).next_to(self.canvas['slide_number'], RIGHT, buff=0.5)

        # Poner en escena
        self.next_slide() # limpia escena anterior e introduce nueva
        self.clear_allSlide_wipe(next_slide_content=next_content_list)
        self.update_canvas()
        self.canvas['title'] = slide_title_nitrites
        self.next_slide(notes='Los nitritos en el agua provienen principalmente de actividades agrícolas y del manejo inadecuado de residuos.') # cambia contenido de diapositiva
        self.wipe([tex_content_nitrite, bibliography], [nitrites_diagram, bibliography_diagram])
        self.next_slide() # cambia contenido de diapositiva
        self.wipe([nitrites_diagram, bibliography_diagram], [effects_nitrites, effects_nitrites_bullet, bibliography_effects_nitrites])
        self.next_slide() # limpia diapositiva excepto slide_num e introduce nueva
        self.clear_allSlide_fade()

    def deteccionNitritos(self):
        # contenido
        slide_title_deteccion = Tex('Detección de Nitritos en Agua', font_size=TITLE_SIZE).to_corner(UL, buff=0.5)

        deteccion_tex = Tex('Se suele realizar por métodos robustos y complementarios, como:',
                            font_size=NORMAL_SIZE,tex_environment='flushleft').to_edge(LEFT, buff=1).shift(UP)
        deteccion_metodos = BulletedList('Espectrofotometría UV-Vis', 'Tiras reactivas', 'kits reactivos',
                                         font_size=NORMAL_SIZE).shift(DOWN)
        bibliografia_detec = Tex('Salud S de. Norma Oficial Mexicana NOM-127-SSA1-2021, Agua Para Uso y Consumo Humano,\n',
                                 'Límites Permisibles de la Calidad del Agua. 2021', font_size=TINY_SIZE, tex_environment='flushright'
                                 ).next_to(self.canvas['slide_number'], LEFT, buff=0.5)
        # cambio de contenido
        desventajas_detec_tex = Tex('Algunas desventajas:',
                                    tex_environment='flushleft',font_size=NORMAL_SIZE).to_edge(LEFT, buff=1).shift(UP)
        desventajas_detec_list = BulletedList('Consumo de tiempo mejorable',
                                              'Equipos robustos',
                                              'Manejo y disposición de reactivos peligrosos',
                                              r'Análisis {\it in situ} mejorables', # Corregido: Análisis
                                              font_size=NORMAL_SIZE)

        # Poner en escena
        self.update_canvas()
        self.play(FadeIn(mobj) for mobj in [slide_title_deteccion, deteccion_tex, deteccion_metodos, bibliografia_detec])
        self.canvas['title'] = slide_title_deteccion
        self.next_slide() # cambiar contenido de diapositiva
        self.play(FadeOut(bibliografia_detec))
        self.play(Transform(deteccion_tex, desventajas_detec_tex),
                  Transform(deteccion_metodos, desventajas_detec_list))
        self.next_slide(notes='Los sensores optoelectrónicos permiten...') # limpia escena
        self.clear_allSlide_fade()

    def sensoresOp(self):
        # Contenido
        slide_title_sensors = Title('Sensores Optoelectrónicos', font_size=TITLE_SIZE) # Usa TITLE_SIZE global
        ventajas_sensores_tex = Tex('Arreglo experimental sencillo, respuesta rápida, análisis in situ, etc.',
                                    font_size=NORMAL_SIZE).to_edge(DOWN, buff=1)

        # --- Componentes del Diagrama ---
        # LED Inicial (Rojo)
        led_body = Circle(radius=0.25, color=DARKER_GRAY, fill_opacity=0.6).move_to(LEFT*4.5)
        led_emitter = Dot(color=RED_E, radius=0.1).move_to(led_body.get_critical_point(RIGHT))
        led_group = VGroup(led_body, led_emitter)
        # La etiqueta del LED se creará y transformará dinámicamente
        led_label_initial = Tex('LED', font_size=NORMAL_SIZE-8).next_to(led_group, DOWN, buff=0.3)
        current_led_label = led_label_initial # Para manejar la transformación

        sample_cuvette = Rectangle(width=1.2, height=2.2, color=BLUE_C, fill_opacity=0.25).shift(ORIGIN)
        sample_label = Tex('Muestra', font_size=NORMAL_SIZE-8).next_to(sample_cuvette,DOWN,buff=0.3)

        photodetector_sensitive_area = Rectangle(width=0.7, height=1.5, color=TEAL_E, fill_opacity=0.7
                                                ).move_to(RIGHT*4.5)
        photodetector_base = Rectangle(width=0.9, height=0.2, color=GRAY).next_to(photodetector_sensitive_area, DOWN, buff=0)
        photodetector_group = VGroup(photodetector_sensitive_area, photodetector_base)
        photodetector_label = Tex('Fotodetector', font_size =NORMAL_SIZE-8).next_to(photodetector_group, DOWN, buff=0.3)

        # Grupos
        diagram_components = VGroup(led_group, sample_cuvette, photodetector_group)
        # Asegurar que las etiquetas estén bien posicionadas después de .arrange para los componentes principales
        # (led_label se maneja con current_led_label, sample_label y photodetector_label se reposicionan si es necesario)
        sample_label.next_to(sample_cuvette, DOWN, buff=0.3)
        photodetector_label.next_to(photodetector_group, DOWN, buff=0.3)

        labels_group = VGroup(current_led_label, sample_label, photodetector_label)
        full_diagram_display = VGroup(diagram_components, labels_group).next_to(slide_title_sensors, DOWN, buff=0.8).scale(0.9)
        # --- Función interna para generar caminos de luz ---
        def light_path_generator(
            ray1_color, ray1_flash_color,
            ray2_color, ray2_flash_color,
            ray3_color, ray3_flash_color
            ):
            num_rays_local = 3
            light_rays_collection_local = VGroup()
            ray_start_point_led_local = led_emitter.get_center() # Usar el led_emitter del scope exterior

            sample_entry_y_coords_local = np.linspace(-sample_cuvette.height / 2 * 0.6, sample_cuvette.height / 2 * 0.6, num_rays_local)
            detector_entry_y_coords_local = np.linspace(-photodetector_sensitive_area.height / 2 * 0.6, photodetector_sensitive_area.height / 2 * 0.6, num_rays_local)

            animations_first_segment_local = []
            animations_second_segment_local = []
            animations_third_segment_local = []

            for i in range(num_rays_local):
                sample_entry_point = sample_cuvette.get_critical_point(LEFT) + UP * sample_entry_y_coords_local[i]
                sample_exit_point = sample_cuvette.get_critical_point(RIGHT) + UP * sample_entry_y_coords_local[i]
                detector_entry_point = photodetector_sensitive_area.get_critical_point(LEFT) + UP * detector_entry_y_coords_local[i]

                ray_segment_to_sample = Line(ray_start_point_led_local, sample_entry_point, color=ray1_color, stroke_width=3)
                ray_segment_in_sample = Line(sample_entry_point, sample_exit_point, color=ray2_color, stroke_width=3)
                ray_segment_to_detector = Line(sample_exit_point, detector_entry_point, color=ray3_color, stroke_width=3)

                light_rays_collection_local.add(ray_segment_to_sample, ray_segment_in_sample, ray_segment_to_detector)

                animations_first_segment_local.append(ShowPassingFlash(ray_segment_to_sample.copy().set_stroke(ray1_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.7))
                animations_second_segment_local.append(ShowPassingFlash(ray_segment_in_sample.copy().set_stroke(ray2_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.6))
                animations_third_segment_local.append(ShowPassingFlash(ray_segment_to_detector.copy().set_stroke(ray3_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.7))

            return animations_first_segment_local, animations_second_segment_local, animations_third_segment_local, light_rays_collection_local

        # --- Generar caminos de luz ---
        # 1. Sensor Genérico (LED Rojo, Luz Amarilla)
        first_ray, second_ray, third_ray, light_ray_collection_generic = light_path_generator(
            ray1_color=YELLOW_D, ray1_flash_color=YELLOW_B,
            ray2_color=YELLOW_C, ray2_flash_color=YELLOW_A,
            ray3_color=YELLOW_D, ray3_flash_color=YELLOW_B
        )

        # 2. Sensor Fluorescente (N-GQDs -> LED UV, Luz UV -> Verde)
        # Los rayos se generan después de cambiar el color del LED

        # ---- Texto y flecha para elemento sensibilizador ----
        # Ajustado el nombre para evitar conflicto si se reutiliza
        sensitizing_element_text = Tex('Elemento sensibilizador', font_size=NORMAL_SIZE-2).next_to(sample_cuvette, DOWN, buff=1.2)
        arrow_to_sample = Arrow(start=sensitizing_element_text.get_top(), end=sample_label.get_bottom() + DOWN*0.1, color=RED_A, buff=0.1)

        # --- Animaciones ---
        # Configuración inicial del canvas y título de la diapositiva
        self.update_canvas() # Asumiendo que esto es para el número de slide
        self.canvas['title'] = slide_title_sensors # Asigna el título al canvas
        self.play(Write(self.canvas['title'])) # Anima la aparición del título del canvas

        self.play(FadeIn(ventajas_sensores_tex))

        self.next_slide(notes='El arreglo más sencillo se compone de un LED, una muestra y un fotodetector.')
        self.play(
            LaggedStart(
                GrowFromCenter(led_group), Write(current_led_label),
                GrowFromCenter(sample_cuvette), Write(sample_label),
                GrowFromCenter(photodetector_group), Write(photodetector_label),
                lag_ratio=0.5
            )
        )
        # Animación del sensor genérico (luz amarilla)
        self.play(LaggedStart(*first_ray, lag_ratio=0.15))
        self.play(LaggedStart(*second_ray, lag_ratio=0.15))
        self.play(LaggedStart(*third_ray, lag_ratio=0.15))
        self.play(Create(light_ray_collection_generic), run_time=0.5)

        self.next_slide(notes='El elemento sensibilizador en la muestra origina un fenómeno óptico singular.')
        self.play(FadeOut(ventajas_sensores_tex), FadeOut(light_ray_collection_generic)) # Limpiar antes de mostrar el efecto del sensibilizador

        # Introducir el texto del elemento sensibilizador y la flecha
        self.play(Write(sensitizing_element_text))
        self.play(GrowArrow(arrow_to_sample))

        # Cambiar LED a UV y su etiqueta
        new_led_label_uv = Tex('LED UV', font_size=NORMAL_SIZE-8).next_to(led_group, DOWN, buff=0.3)
        self.play(
            led_emitter.animate.set_color(PURPLE_B), # LED cambia a color UV
            Transform(current_led_label, new_led_label_uv) # Etiqueta cambia a "LED UV"
        )
        # Es importante actualizar la referencia si vas a interactuar con current_led_label después.
        # current_led_label ahora es new_led_label_uv en términos del objeto en pantalla.

        # Generar los rayos para el sensor fluorescente AHORA que el LED ha cambiado de color y está en posición
        first_ray_sen, second_ray_sen, third_ray_sen, light_ray_collection_sen = light_path_generator(
            ray1_color=PURPLE_C, ray1_flash_color=PURPLE_A,    # Luz UV del LED a la muestra
            ray2_color=PURPLE_B, ray2_flash_color=PURPLE_A,    # Luz UV DENTRO de la muestra (absorción/interacción)
            ray3_color=GREEN_C, ray3_flash_color=GREEN_B      # Luz VERDE emitida (fluorescencia)
        )

        self.next_slide(notes='La luz UV incidente se convierte en luz verde emitida, que es detectada.')
        # Animar el camino de luz fluorescente
        self.play(LaggedStart(*first_ray_sen, lag_ratio=0.15))
        self.play(LaggedStart(*second_ray_sen, lag_ratio=0.15))
        self.play(LaggedStart(*third_ray_sen, lag_ratio=0.15))
        self.play(Create(light_ray_collection_sen), run_time=0.5)

        self.next_slide(notes="Este cambio de longitud de onda es la base de la detección.")
        # Limpieza final de esta sección
        self.clear_allSlide_fade() # O tu método preferido de limpieza

    def intro_nanomateriales(self):
        # Título de la diapositiva
        slide_title_NM = Title('Nanomateriales vs. Materiales Bulk', font_size=TITLE_SIZE)
        self.update_canvas() # Actualiza número de slide
        self.canvas['title'] = slide_title_NM # Asigna al canvas
        self.play(Write(self.canvas['title']))

        # --- Sección 1: Material Bulk ---
        bulk_material_label = Tex("Material Bulk", font_size=NORMAL_SIZE-2).to_edge(UP, buff=1.5).shift(LEFT*3)
        bulk_material = Rectangle(width=3, height=2, color=BLUE_E, fill_opacity=0.7).next_to(bulk_material_label, DOWN, buff=0.5)

        # Simular átomos desorganizados en el material bulk
        bulk_atoms = VGroup()
        for _ in range(30):
            x_offset = np.random.uniform(-bulk_material.width/2 + 0.2, bulk_material.width/2 - 0.2)
            y_offset = np.random.uniform(-bulk_material.height/2 + 0.2, bulk_material.height/2 - 0.2)
            bulk_atoms.add(Dot(radius=0.05, color=random_color()).move_to(bulk_material.get_center() + RIGHT*x_offset + UP*y_offset))

        bulk_group = VGroup(bulk_material_label, bulk_material, bulk_atoms)

        self.play(FadeIn(bulk_group, shift=RIGHT))
        self.next_slide(notes="Los materiales bulk tienen propiedades ópticas y eléctricas predecibles basadas en su composición macroscópica.")

        # Incidencia de luz en material bulk
        light_source_bulk = Dot(bulk_material.get_left() + LEFT*2 + UP*0.5, color=YELLOW)
        incident_light_bulk = Arrow(light_source_bulk.get_center(), bulk_material.get_left() + UP*0.5, buff=0.1, color=YELLOW, stroke_width=5)
        reflected_light_bulk = Arrow(bulk_material.get_left() + UP*0.5, bulk_material.get_left() + LEFT*1.5 + UP*1, buff=0.1, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        absorbed_text_bulk = Tex("Absorción/Reflexión simple", font_size=NORMAL_SIZE+5).next_to(bulk_material, DOWN, buff=0.5)

        self.play(Create(light_source_bulk))
        self.play(GrowArrow(incident_light_bulk))
        self.play(GrowArrow(reflected_light_bulk), Write(absorbed_text_bulk), run_time=1)
        self.next_slide(notes="Al reducir la dimensionalidad a nanoescala, emergen propiedades cuánticas.")
        self.play(FadeOut(light_source_bulk, incident_light_bulk, reflected_light_bulk, absorbed_text_bulk))

        # --- Sección 2: Nanomateriales (Puntos Cuánticos) ---
        nano_material_label = Tex("Nanomateriales (ej. Puntos Cuánticos)", font_size=TINY_SIZE+8).to_edge(UP, buff=1.5).shift(RIGHT*3)

        # Simular puntos cuánticos (N-GQDs)
        qds = VGroup()
        positions = [LEFT*0.7+UP*0.3, RIGHT*0.1+DOWN*0.4, RIGHT*0.8+UP*0.5, LEFT*0.2+UP*0.8, RIGHT*0.5+DOWN*0.8] # Posiciones relativas
        colors_emission = [GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E] # Diferentes tonos de verde o colores si fueran diferentes QDs

        nano_area = Circle(radius=1.2, color=DARK_BLUE, fill_opacity=0.3).next_to(nano_material_label, DOWN, buff=0.7)

        for i, pos in enumerate(positions):
            qd = Dot(radius=0.15, color=BLUE_D).move_to(nano_area.get_center() + pos*0.5) # QDs "apagados"
            qds.add(qd)

        nano_group = VGroup(nano_material_label, nano_area, qds)
        self.play(Transform(bulk_group, nano_group), run_time=1.5) # Transforma bulk en nano

        self.next_slide(notes="Los nanomateriales, como los puntos cuánticos, pueden exhibir fluorescencia.")

        # Incidencia de luz UV en nanomateriales (QDs)
        light_source_nano = Dot(nano_area.get_left() + LEFT*2, color=PURPLE_A) # Fuente de luz UV
        incident_light_nano = Arrow(light_source_nano.get_center(), nano_area.get_center() + LEFT*nano_area.radius*0.7, buff=0.1, color=PURPLE_C, stroke_width=5)

        self.play(Create(light_source_nano))
        self.play(GrowArrow(incident_light_nano))

        # Animación de fluorescencia
        emitted_lights_nano = VGroup()
        for i, qd in enumerate(qds):
            # Los QDs "se encienden" (cambian de color)
            self.play(qd.animate.set_color(colors_emission[i % len(colors_emission)]), run_time=0.2)
            # Emiten luz en varias direcciones
            for j in range(3): # 3 rayos por QD
                angle = TAU * j / 3 + np.random.uniform(-0.2, 0.2) # Pequeña aleatoriedad en el ángulo
                direction = np.array([np.cos(angle), np.sin(angle), 0])
                emitted_ray = Arrow(qd.get_center(), qd.get_center() + direction * 0.7, buff=0.05, color=colors_emission[i % len(colors_emission)], stroke_width=3, max_tip_length_to_length_ratio=0.3)
                emitted_lights_nano.add(emitted_ray)

        fluorescence_text_nano = Tex("Fluorescencia:\nAbsorción UV, Emisión Visible", font_size=TINY_SIZE+8).next_to(nano_area, DOWN, buff=0.5)
        self.play(LaggedStart(*[GrowArrow(ray) for ray in emitted_lights_nano], lag_ratio=0.1), Write(fluorescence_text_nano))

        self.next_slide(notes="Esta propiedad es clave para su aplicación en sensores optoelectrónicos.")

        # Texto final de la diapositiva
        conclusion_text = Paragraph(
            "Los nanomateriales ofrecen propiedades ópticas y eléctricas únicas,",
            "debido a efectos cuánticos y gran área superficial,",
            "abriendo nuevas vías para la tecnología de sensores.",
            font_size=NORMAL_SIZE-4, alignment="center"
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(conclusion_text))

        self.next_slide(notes='El siguiente diagrama muestra la generación progresiva de nanomateriales a partir de uno a granel')
        # Limpieza
        self.clear_allSlide_fade()

    def nanomateriales(self):
        # ---- nanomateriales -----
        slide_title_nano = Title('Nanomateriales', font_size=TITLE_SIZE)
        description_nano = Tex('Una clasificación general de la generación de nanomateriales es:', # Corregido: es
                            font_size=NORMAL_SIZE).next_to(slide_title_nano, DOWN, buff=0.8)

        # Cargar y estandarizar objetos SVG
        bulk = SVGMobject(f'{HOME}\\bulk.svg').set(height=1.5).set_color(BLUE)
        well = SVGMobject(f'{HOME}\\well.svg').set(height=1.5).set_color(GREEN)
        wire = SVGMobject(f'{HOME}\\cilinder.svg').set(height=1.5).set_color(RED)
        dot = Dot(radius=0.2, color=YELLOW)  # Dot escalado para equivalencia visual

        # Ajustar posición vertical de todos los objetos al mismo nivel
        for mobj in [bulk, well, wire, dot]:
            mobj.align_to(bulk, DOWN)  # Alinear por la base

        # Agrupación y distribución horizontal
        quantum_objs = VGroup(bulk, well, wire, dot).arrange(RIGHT, buff=2.5, aligned_edge=DOWN)

        # Nombres con alineación precisa debajo de cada objeto
        names = VGroup(
            Text("Bulk", font_size=NORMAL_SIZE).move_to(bulk.get_center()).shift(DOWN*1.5),
            Text("Hilo cuántico", font_size=NORMAL_SIZE).move_to(well.get_center()).shift(DOWN*1.5),
            Text("Pozo cuántico", font_size=NORMAL_SIZE).move_to(wire.get_center()).shift(DOWN*1.5),
            Text("Punto cuántico", font_size=NORMAL_SIZE).move_to(dot.get_center()).shift(DOWN)
        )

        # Animación secuencial
        self.update_canvas()
        self.play(Write(slide_title_nano), Write(description_nano))
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(obj) for obj in quantum_objs],
                lag_ratio=0.3
            )
        )
        self.play(
            LaggedStart(
                *[Write(name) for name in names],
                lag_ratio=0.2
            )
        )
        self.next_slide(notes='Es un ejemplo práctico para lo que sucede con NM a base de carbono')
        self.play(FadeOut(obj) for obj in quantum_objs)

        # --- nanomateriales a base de carbono
        slide_title_nmc = Title('Nanomateriales a base de carbono', font_size= NORMAL_SIZE)

        graphite = ImageMobject(f'{HOME}\\graphite.png').move_to(bulk)
        graphene = ImageMobject(f'{HOME}\\graphene.png').move_to(well)
        nanotube = SVGMobject(f'{HOME}\\nanotube.svg').move_to(wire)
        gqd = SVGMobject(f'{HOME}\\gqd_structure.svg').move_to(dot)

        # Ajuste de tamaño si es necesario
        for structure in [graphite, graphene, nanotube, gqd]:
            structure.set_height(1.5)

        # Agrupación horizontal
        carbon_structures = Group(graphite, graphene, nanotube, gqd).arrange(RIGHT, buff=2.5, aligned_edge=DOWN)

        # Etiquetas
        carbon_names = VGroup(
            Text("Grafito", font_size=NORMAL_SIZE-5).move_to(names[0]),
            Text("Grafeno", font_size=NORMAL_SIZE-5).move_to(names[1]),
            Text("Nanotubo", font_size=NORMAL_SIZE-5).move_to(names[2]),
            Text("Punto cuántico\nde grafeno", font_size=NORMAL_SIZE-5).move_to(names[3]),
        )

        # Animaciones
        self.play(Transform(slide_title_nano, slide_title_nmc), FadeOut(description_nano))
        self.play(LaggedStart(*[FadeIn(obj) for obj in carbon_structures], lag_ratio=0.3))
        self.play(FadeOut(name) for name in names)
        self.play(LaggedStart(*[Write(name) for name in carbon_names], lag_ratio=0.2))

    def gqd(self):
        # contenido
        slide_title_gqd = Title('Puntos Cuánticos de Grafeno (GQD)', font_size=TITLE_SIZE)

        gqd_structure = SVGMobject(f'{HOME}\\gqd_structure.svg').scale(2).to_edge(LEFT, buff=1)
        # Propiedades divididas en dos grupos
        propiedades_heredadas = VGroup(
        Text("1. Donador y aceptor de electrones", font_size=NORMAL_SIZE),
        Text("2. Superficie químicamente modificable", font_size=NORMAL_SIZE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=1).shift(UP)

        propiedades_unicas = VGroup(
        Text("3. Confinamiento cuántico de dominios π", font_size=NORMAL_SIZE, color=RED_B),
        Text("4. Biocompatibilidad e hidrosolubilidad", font_size=NORMAL_SIZE, color=RED_B),
        Text("5. Fluorescencia estable y ajustable", font_size=NORMAL_SIZE, color=RED_B)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(propiedades_heredadas, DOWN, buff=0.2).shift(DOWN*0.5)

        gqd_fluorescence = SVGMobject(f'{HOME}\\gqd_fluorescence.svg').scale(2).move_to(gqd_structure)

        # --- animaciones --
        self.next_slide(notes='Exhiben propiedades similares "heredadas" del grafeno como:') # introduce siguiente slide
        self.update_canvas()
        self.canvas['title'] = slide_title_gqd
        self.clear_allSlide_wipe(next_slide_content=[slide_title_gqd, gqd_structure, propiedades_heredadas])
        self.next_slide(notes='Por su tamaño en el orden nanométrico, surgen nuevas propiedades.') # emerge fluorescencia y muestra resto de propiedades
        self.play(ReplacementTransform(gqd_structure, gqd_fluorescence))
        self.play(LaggedStart(*[Write(prop) for prop in propiedades_unicas], lag_ratio=0.4))
        self.next_slide(
            notes='Estas propiedades emergentes están estrechamente relacionadas con la fluorescencia, que son de interés para el desarrollo de sensores' # Corregido: interés
            ) # Quitar propiedades y muestra espectro de PL
        self.clear_slide_content()

        # --- Ejes para el Espectro PL ---
        # Ajusta los rangos según tus datos o lo que quieras mostrar
        x_min_wl, x_max_wl, x_step_wl = 400, 700, 50  # Longitud de onda en nm
        y_min_intensity, y_max_intensity, y_step_intensity = 0, 1.8, 0.3 # Intensidad PL (u.a.)

        axes = Axes(
            x_range=[x_min_wl, x_max_wl, x_step_wl],
            y_range=[y_min_intensity, y_max_intensity, y_step_intensity],
            x_length=6, # Ancho del gráfico
            y_length=4, # Alto del gráfico
            axis_config={"include_numbers": True, "font_size": 20},
            x_axis_config={"numbers_to_include": np.arange(x_min_wl, x_max_wl + x_step_wl, x_step_wl*2)},
            y_axis_config={"numbers_to_include": np.arange(y_min_intensity, y_max_intensity + y_step_intensity, y_step_intensity*2)}
        ).to_edge(RIGHT, buff=0.5).scale(1)  # Área para el espectro PL

        x_label = axes.get_x_axis_label(Tex("Longitud de Onda (nm)", font_size=22), edge=DOWN, direction=DOWN, buff=0.4)
        y_label = axes.get_y_axis_label(Tex("Intensidad PL (u.a.)", font_size=22).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.5)

        pl_plot_group = VGroup(axes, x_label, y_label)

        # --- Función para generar la curva del espectro PL (Gaussiana) ---
        # center_wl: longitud de onda central del pico; sigma: ancho del pico
        def get_pl_curve(amplitude, center_wl=525, sigma=30, color=GREEN_C):
            # Asegurarse que la amplitud no exceda y_max_intensity para la visualización
            safe_amplitude = min(amplitude, y_max_intensity * 0.95)
            return axes.plot(
                lambda x: safe_amplitude * np.exp(-((x - center_wl)**2) / (2 * sigma**2)),
                x_range=[x_min_wl, x_max_wl], # Graficar en todo el rango del eje x
                color=color,
                stroke_width=3
            )

        # --- Datos de los GQDs (SVG, Nombre, Amplitud PL, Color del Pico) ---
        # Asegúrate de que los archivos SVG existan en tu carpeta HOME
        gqd_data = [
            {"file": f'{HOME}\\gqd_fluorescence.svg', "name": "GQD (Base)", "amplitude": 0.4, "color": BLUE_D, "notes": "Estructura base de GQD con fluorescencia inicial."},
            {"file": f'{HOME}\\go_dots.svg', "name": "GO-dots", "amplitude": 0.7, "color": BLUE_B, "notes": "Puntos de Óxido de Grafeno (GO-dots), fluorescencia moderada."},
            {"file": f'{HOME}\\r_gqd.svg', "name": "r-GQD", "amplitude": 1.0, "color": BLUE_A, "notes": "GQD Reducidos (r-GQD), fluorescencia mejorada."},
            {"file": f'{HOME}\\n_gqd.svg', "name": "N-GQD", "amplitude": 1.5, "color": GREEN_B, "notes": "GQD Dopados con Nitrógeno (N-GQD), fluorescencia significativamente alta, ideal para sensores."}
        ]

        current_gqd_svg = None
        current_gqd_label = None
        current_pl_curve = None

        # ------ animaciones ---------
        self.play(Create(pl_plot_group))

        # --- Animación Secuencial ---
        for i, data in enumerate(gqd_data):
            self.next_slide(notes=data["notes"])

            # Cargar nuevo SVG y etiqueta
            new_gqd_svg = SVGMobject(data["file"]).scale(1.7).to_edge(LEFT, buff=0.5) # Área para el SVG del GQD
            new_gqd_label = Tex(data["name"], font_size=NORMAL_SIZE-2).next_to(new_gqd_svg, DOWN, buff=0.3)
            new_pl_curve = get_pl_curve(data["amplitude"], color=data["color"])

            if current_gqd_svg is None: # Primera iteración
                current_gqd_svg = new_gqd_svg
                current_gqd_label = new_gqd_label
                current_pl_curve = new_pl_curve
                self.play(
                    DrawBorderThenFill(current_gqd_svg),
                    Write(current_gqd_label),
                    Create(current_pl_curve)
                )
                self.next_slide()
            else: # Siguientes iteraciones
                self.play(
                    Transform(current_gqd_svg, new_gqd_svg),
                    Transform(current_gqd_label, new_gqd_label),
                    Transform(current_pl_curve, new_pl_curve)
                )
                self.next_slide()

            # Resaltar N-GQD (último en la lista)
            if i == len(gqd_data) - 1:
                highlight_text = Tex("Mayor Fluorescencia", font_size=NORMAL_SIZE-4, color=data["color"]).next_to(current_pl_curve, UP, buff=0.2)
                self.play(Write(highlight_text))
                # Mantener el highlight_rect y highlight_text o desvanecerlos si prefieres

        self.next_slide(notes="La alta fluorescencia de los N-GQD los hace excelentes candidatos para el desarrollo de sensores.")

    def gqd_quenching(self):
        # Título de la diapositiva
        slide_title_quenching = Title('Extinción de Fluorescencia de N-GQD por Nitritos', font_size=TITLE_SIZE)

        # --- Reutilizar Elementos de la Diapositiva Anterior (N-GQD y su PL) ---
        # N-GQD (el más fluorescente)
        n_gqd_svg = SVGMobject(f'{HOME}\\n_gqd.svg').scale(1.7).to_edge(LEFT, buff=0.5)
        self.n_gqd = n_gqd_svg
        n_gqd_label = Tex("N-GQD", font_size=NORMAL_SIZE-2).next_to(n_gqd_svg, DOWN, buff=0.3)

        # Espectro PL (configuración similar a la diapositiva gqd)
        x_min_wl, x_max_wl, x_step_wl = 400, 700, 50
        y_min_intensity, y_max_intensity, y_step_intensity = 0, 1.8, 0.3
        axes = Axes(
            x_range=[x_min_wl, x_max_wl, x_step_wl],
            y_range=[y_min_intensity, y_max_intensity, y_step_intensity],
            x_length=6, y_length=4,
            axis_config={"include_numbers": True, "font_size": 20},
            x_axis_config={"numbers_to_include": np.arange(x_min_wl, x_max_wl + x_step_wl, x_step_wl*2)},
            y_axis_config={"numbers_to_include": np.arange(y_min_intensity, y_max_intensity + y_step_intensity, y_step_intensity*2)}
        ).to_edge(RIGHT, buff=0.5)
        x_label_pl = axes.get_x_axis_label(Tex("Longitud de Onda (nm)", font_size=22), edge=DOWN, direction=DOWN, buff=0.4)
        y_label_pl = axes.get_y_axis_label(Tex("Intensidad PL (u.a.)", font_size=22).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.5)
        pl_plot_group = VGroup(axes, x_label_pl, y_label_pl)

        # Función para la curva PL (reutilizada)
        def get_pl_curve(amplitude, center_wl=525, sigma=30, color=GREEN_B): # N-GQD color
            safe_amplitude = min(amplitude, y_max_intensity * 0.95)
            return axes.plot(
                lambda x: safe_amplitude * np.exp(-((x - center_wl)**2) / (2 * sigma**2)),
                x_range=[x_min_wl, x_max_wl], color=color, stroke_width=3
            )

        # Estado inicial: N-GQD con alta fluorescencia
        initial_amplitude = 1.5 # La amplitud más alta de N-GQD
        current_pl_curve = get_pl_curve(initial_amplitude)

        self.clear_allSlide_wipe(next_slide_content=[slide_title_quenching,n_gqd_svg, n_gqd_label, pl_plot_group])
        self.update_canvas()
        self.play(Create(current_pl_curve))
        self.next_slide(notes="Los N-GQD muestran una alta fluorescencia inicial.")

        # --- Introducción de Nitritos y Medio Ácido ---
        # Moléculas de Nitrito (NO2-)
        nitrito_tex = Tex("$NO_2^-$", font_size=NORMAL_SIZE, color=ORANGE)
        nitritos_group = VGroup() # Para agrupar las moléculas de nitrito

        # Indicador de pH ácido
        ph_acido_tex = Tex("Medio Ácido ($H^+$)", font_size=NORMAL_SIZE-4, color=RED_A).next_to(n_gqd_svg, UP, buff=0.5)
        self.play(Write(ph_acido_tex), notes="La reacción es favorecida en medio ácido.")
        self.wait(0.5)

        # Texto indicador de concentración de nitritos
        concentracion_label = Tex("Concentración de $NO_2^-$:", font_size=NORMAL_SIZE-4).to_edge(DOWN, buff=1.1).shift(LEFT*2)
        concentracion_valor_str = "Baja"
        concentracion_valor = Tex(concentracion_valor_str, font_size=NORMAL_SIZE-4, color=YELLOW).next_to(concentracion_label, RIGHT, buff=0.4)
        self.play(Write(concentracion_label), Write(concentracion_valor))

        # --- Simulación de Aumento de Concentración y Extinción de PL ---
        # (Amplitudes, número de nitritos a mostrar, texto de concentración)
        quenching_steps = [
            {"amplitude": 1.2, "num_nitritos": 3, "conc_text": "Moderada", "color": YELLOW_D, "notes": "Al añadir nitritos, la fluorescencia comienza a disminuir."},
            {"amplitude": 0.7, "num_nitritos": 6, "conc_text": "Media", "color": ORANGE, "notes": "Mayor concentración de nitritos, mayor extinción de fluorescencia."},
            {"amplitude": 0.3, "num_nitritos": 9, "conc_text": "Alta", "color": RED_D, "notes": "Con alta concentración de nitritos, la fluorescencia se extingue casi por completo."}
        ]

        # Posiciones para las moléculas de nitrito alrededor del N-GQD
        nitrito_positions_area = Circle(radius=n_gqd_svg.height/2 + 0.3).move_to(n_gqd_svg.get_center())

        for i, step in enumerate(quenching_steps):
            self.next_slide(notes=step["notes"])

            # Añadir más moléculas de nitrito
            new_nitritos_to_add = VGroup()
            current_num_nitritos_on_screen = len(nitritos_group)
            num_to_actually_add = step["num_nitritos"] - current_num_nitritos_on_screen

            for _ in range(num_to_actually_add):
                # Posición aleatoria alrededor del N-GQD para los nuevos nitritos
                angle = np.random.uniform(0, TAU)
                pos_on_circle = nitrito_positions_area.point_from_proportion(angle / TAU) # punto en el círculo
                # Pequeña variación para que no se solapen exactamente en el círculo
                random_offset = np.array([np.random.uniform(-0.3,0.3), np.random.uniform(-0.3,0.3), 0])
                final_pos = pos_on_circle + random_offset

                nitrito_mol = nitrito_tex.copy().move_to(final_pos)
                new_nitritos_to_add.add(nitrito_mol)

            # Actualizar texto de concentración
            new_concentracion_valor = Tex(step["conc_text"], font_size=NORMAL_SIZE-4, color=step["color"]).move_to(concentracion_valor)

            # Animar la aparición de nuevos nitritos y la disminución de la PL
            new_pl_curve = get_pl_curve(step["amplitude"]) # El color del pico se mantiene verde, pero su intensidad baja

            animations = [
                Transform(current_pl_curve, new_pl_curve),
                Transform(concentracion_valor, new_concentracion_valor)
            ]
            if len(new_nitritos_to_add) > 0:
                animations.append(FadeIn(new_nitritos_to_add, scale=0.5, lag_ratio=0.2))

            self.play(*animations)
            nitritos_group.add(*new_nitritos_to_add) # Añade los nuevos a la cuenta

        self.next_slide(notes="Este fenómeno de extinción de fluorescencia es la base del sensor de nitritos.")

        conclusion_quenching = Tex(
            "La interacción N-GQD + $NO_2^-$ (en medio ácido) causa la extinción de la fluorescencia.",
            font_size=NORMAL_SIZE-2
        ).next_to(concentracion_label.get_bottom() + DOWN + concentracion_valor.get_bottom() + DOWN, DOWN, buff=0.5) # Ajusta la posición
        conclusion_quenching.align_to(concentracion_label, LEFT)

        self.play(Write(conclusion_quenching))
        self.next_slide(notes='Sin embargo, debido a la gran facilidad de síntesis se han' \
        'desarrollado un sinfín de rutas para su obtención, perdiendo un poco de vista el enfoque a una utilidad práctica.') # Corregido: sinfín
        self.play(FadeOut(mobj) for mobj in self.mobjects if mobj not in [n_gqd_svg, self.canvas['slide_number']])

    def cierre_intro(self):
        slide_title = Title('Arreglo final', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        n_gqg = self.n_gqd
        # --- Componentes del Diagrama ---
        # LED Inicial (Rojo)
        led_body = Circle(radius=0.25, color=DARKER_GRAY, fill_opacity=0.6).move_to(LEFT*4.5)
        led_emitter = Dot(color=RED_E, radius=0.1).move_to(led_body.get_critical_point(RIGHT))
        led_group = VGroup(led_body, led_emitter)
        led_label = Tex('LED UV', font_size=NORMAL_SIZE-5).next_to(led_group, DOWN, buff=0.3)

        sample_cuvette = Rectangle(width=1.2, height=2.2, color=BLUE_C, fill_opacity=0.25).shift(ORIGIN)
        sample_label = Tex('Muestra', font_size=NORMAL_SIZE-5).next_to(sample_cuvette,DOWN,buff=0.3).next_to(sample_cuvette, DOWN, buff=0.3)

        photodetector_sensitive_area = Rectangle(width=0.7, height=1.5, color=TEAL_E, fill_opacity=0.7
                                                ).move_to(RIGHT*4.5)
        photodetector_base = Rectangle(width=0.9, height=0.2, color=GRAY).next_to(photodetector_sensitive_area, DOWN, buff=0)
        photodetector_group = VGroup(photodetector_sensitive_area, photodetector_base)
        photodetector_label = Tex('Fotodetector', font_size=NORMAL_SIZE-5).next_to(photodetector_group, DOWN, buff=0.3)

        # Grupos
        diagram_components = VGroup(led_group, sample_cuvette, photodetector_group)

        labels_group = VGroup(led_label, sample_label, photodetector_label)
        full_diagram_display = VGroup(diagram_components, labels_group).next_to(self.canvas['title'], DOWN, buff=0.8).scale(0.9)
        # --- Función interna para generar caminos de luz ---
        def light_path_generator(
            ray1_color, ray1_flash_color,
            ray2_color, ray2_flash_color,
            ray3_color, ray3_flash_color
            ):
            num_rays_local = 3
            light_rays_collection_local = VGroup()
            ray_start_point_led_local = led_emitter.get_center() # Usar el led_emitter del scope exterior

            sample_entry_y_coords_local = np.linspace(-sample_cuvette.height / 2 * 0.6, sample_cuvette.height / 2 * 0.6, num_rays_local)
            detector_entry_y_coords_local = np.linspace(-photodetector_sensitive_area.height / 2 * 0.6, photodetector_sensitive_area.height / 2 * 0.6, num_rays_local)

            animations_first_segment_local = []
            animations_second_segment_local = []
            animations_third_segment_local = []

            for i in range(num_rays_local):
                sample_entry_point = sample_cuvette.get_critical_point(LEFT) + UP * sample_entry_y_coords_local[i]
                sample_exit_point = sample_cuvette.get_critical_point(RIGHT) + UP * sample_entry_y_coords_local[i]
                detector_entry_point = photodetector_sensitive_area.get_critical_point(LEFT) + UP * detector_entry_y_coords_local[i]

                ray_segment_to_sample = Line(ray_start_point_led_local, sample_entry_point, color=ray1_color, stroke_width=3)
                ray_segment_in_sample = Line(sample_entry_point, sample_exit_point, color=ray2_color, stroke_width=3)
                ray_segment_to_detector = Line(sample_exit_point, detector_entry_point, color=ray3_color, stroke_width=3)

                light_rays_collection_local.add(ray_segment_to_sample, ray_segment_in_sample, ray_segment_to_detector)

                animations_first_segment_local.append(ShowPassingFlash(ray_segment_to_sample.copy().set_stroke(ray1_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.7))
                animations_second_segment_local.append(ShowPassingFlash(ray_segment_in_sample.copy().set_stroke(ray2_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.6))
                animations_third_segment_local.append(ShowPassingFlash(ray_segment_to_detector.copy().set_stroke(ray3_flash_color, 5, opacity=0.8), time_width=0.4, run_time=0.7))

            return animations_first_segment_local, animations_second_segment_local, animations_third_segment_local, light_rays_collection_local

        # --- Generar caminos de luz ---
        first_ray, second_ray, third_ray, light_ray_collection_generic = light_path_generator(
            ray1_color=PURPLE_C, ray1_flash_color=PURPLE_A,    # Luz UV del LED a la muestra
            ray2_color=PURPLE_B, ray2_flash_color=PURPLE_A,    # Luz UV DENTRO de la muestra (absorción/interacción)
            ray3_color=GREEN_C, ray3_flash_color=GREEN_B      # Luz VERDE emitida (fluorescencia)
        )

        # ---- Texto y flecha para elemento sensibilizador ----
        # Ajustado el nombre para evitar conflicto si se reutiliza
        sensitizing_element_text = Tex('Elemento sensibilizador', font_size=NORMAL_SIZE-2).next_to(sample_cuvette, DOWN, buff=1.2)
        arrow_to_sample = Arrow(start=sensitizing_element_text.get_top(), end=sample_label.get_bottom() + DOWN*0.1, color=RED_A, buff=0.1)

        self.update_canvas()
        self.play(FadeIn(full_diagram_display, slide_title))
        self.play(n_gqg.animate.move_to(sample_cuvette).scale(0.26))
        self.play(LaggedStart(*first_ray, lag_ratio=0.15))
        self.play(LaggedStart(*second_ray, lag_ratio=0.15))
        self.play(LaggedStart(*third_ray, lag_ratio=0.15))
        self.play(Create(light_ray_collection_generic), run_time=0.5)

        # Introducir el texto del elemento sensibilizador y la flecha
        self.play(Write(sensitizing_element_text))
        self.play(GrowArrow(arrow_to_sample))
        self.next_slide(notes='Por tanto, es necesario tomar en cuenta los siguientes puntos.') # Corregido: necesario

        # ------ cambio de escena ----------
        slide_title_methods = Title('Métodos de síntesis', font_size=TITLE_SIZE)

        img_tbl = ImageMobject(f'{HOME}\\tables\\metodologias_n_gqd.png'
                               ).set_width(config.frame_width*0.95).next_to(slide_title_methods,DOWN,buff=0.5)
        descrip_final = VGroup(
            Tex(r"1. Explorar métodos de síntesis {\it bottom-up} y {\it top-down} para N-GQD", font_size=NORMAL_SIZE),
            Tex(r"2. Obtener morfología uniforme y funcionalización superficial favorable para la detección de $\text{NO}_{2}^{-}$", font_size=NORMAL_SIZE),
            Tex('3. Desarrollo de un sensor optoelectrónico que evalúe su desempeño (LED/Elemento sensibilizador/Fotodetector).', font_size=NORMAL_SIZE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(slide_title,DOWN,buff=0.5)

        # --- animaciones ---
        self.clear_allSlide_wipe(next_slide_content=[slide_title_methods,img_tbl])
        self.next_slide()
        self.wipe(img_tbl, descrip_final)
        self.next_slide(notes='A continuación, los antecedentes y los métodos de síntesis basados en la literatura.') # Corregido: basados
        self.clear_allSlide_fade()


# --------------------- Antecedentes -----------------------------------
    def antecedentes(self): # Puedes nombrar la función como prefieras
        slide_content = {
            'titles': ['Antecedentes (Síntesis)',
                       'Antecedentes (nitritos en agua)',
                       'Antecedentes (sensores de N-GQD)', # Ligeramente modificado para diferenciar si es necesario
                       'Antecedentes (sensores de N-GQD)',
                       'Antecedentes (sensores de N-GQD)'],
            'img_table': ['sintesis_n_gqd.png', # Reordené para que coincida con "Síntesis"
                          'casos_nitritos.png', # Coincide con "nitritos en agua"
                          'n_gqd_sensors1.png',
                          'n_gqd_sensors2.png',
                          'n_gqd_sensors3.png']
        }

        num_slides = len(slide_content['img_table'])

        for i in range(num_slides):
            title_text_for_slide = slide_content['titles'][i]
            image_filename = slide_content['img_table'][i]

            current_title_mobject = Title(title_text_for_slide, font_size=TITLE_SIZE)
            current_image_mobject_loaded = ImageMobject(f'{HOME}\\tables\\{image_filename}'
                                                        ).set_width(config.frame_width*0.95
                                                                    ).next_to(current_title_mobject, DOWN, buff=0.5)

            self.play(FadeIn(mobj) for mobj in [current_title_mobject, current_image_mobject_loaded])
            self.update_canvas()
            self.next_slide()
            self.clear_allSlide_fade()

    def analisis_critico_antecedentes(self):
        # Título para la diapositiva
        slide_title_analisis = Title("Análisis Crítico de Antecedentes", font_size=TITLE_SIZE).to_edge(LEFT, buff=1)

        # Ajusta font_size, buff, line_spacing y max_width según sea necesario para que quepa bien.
        bullet_list = BulletedList(
            'La detección de nitritos tiene alta relevancia local',
            'La variabilidad (morfología, funcionalización) afecta reproducibilidad e integración.',
            "Los precursores (dopantes, solventes) tienen un impacto directo en rendimiento cuántico y estabilidad coloidal", # Corregido: Añadida coma
            'Base literaria suficiente para desarrollar un sensor de nitritos (N-GQD)',

            font_size=NORMAL_SIZE, # Reducir un poco el tamaño para que quepa más texto
            buff=0.25,
        )

        # Posicionar la lista debajo del título
        bullet_list.to_edge(RIGHT, buff=1)

        # Animar la aparición de la lista
        self.next_slide(notes="Este análisis crítico identifica las áreas de oportunidad para la presente investigación.")
        self.update_canvas()
        self.play(Write(bullet_list), Write(slide_title_analisis))
        self.next_slide()

    def aportacion_cientifica(self):
        # Título de la diapositiva
        slide_title_text = Title("Aportación científica", font_size=TITLE_SIZE)

        bullet_list_aport = BulletedList(
            'Integración y comparación de métodos top-down y bottom-up de N-GQD para la detección de nitritos en agua.',
            "Síntesis de N-GQD con fluorescencia y estabilidad coloidal optimizadas para la detección de nitritos en agua.",
            'Desarrollo y validación conceptual de un prototipo de sensor optoelectrónico para la detección in situ de nitritos', # Corregido: Desarrollo
            font_size=NORMAL_SIZE-2
        ).next_to(slide_title_text,DOWN,buff=0.5)

        self.update_canvas()
        self.clear_allSlide_wipe(next_slide_content=[slide_title_text, bullet_list_aport])
        self.next_slide()

    def hipotesis(self):
        slide_title_hipot = Title('Hipótesis')
        hipotesis_text = Tex('Los N-GQD sintetizados, al ser excitados por una fuente de luz UV apropiada',
                             '(LED de ~365 nm), exhiben una fluorescencia estable y cuantificable,',
                            r'cuya intensidad es posible modular selectivamente por la concentración de $\text{NO}_{2}^{-}$',
                            'en un arreglo optoelectrónico simple compuesto por la fuente de excitación,',
                             'la muestra con N-GQD y un fotodetector', tex_environment='flushleft', font_size=NORMAL_SIZE
                             ).next_to(slide_title_hipot,DOWN,buff=0.5)

        self.update_canvas()
        self.clear_allSlide_wipe(next_slide_content=[slide_title_hipot, hipotesis_text])
        self.next_slide()

    def objetivo_general(self):
        title_slide_obj_esp = Title('Objetivo general')
        objetivo_general_tex = Tex('Desarrollar N-GQDs mediante diseño y síntesis optimizados, cuya extinción',
                             'de fluorescencia muestre una correlación sistemática y sensible (lineal)',
                              'con la concentración de nitritos en agua, para su integración en un sensor',
                               'optoelectrónico.', tex_environment='flushleft', font_size=NORMAL_SIZE
                             ).next_to(title_slide_obj_esp,DOWN,buff=0.5)

        self.update_canvas()
        self.clear_allSlide_wipe(next_slide_content=[title_slide_obj_esp, objetivo_general_tex])
        self.next_slide()

    def objetivos_específicos(self):
        title_slide_obj_esp = Title('Objetivos específicos')
        objetivos_esp_tex = BulletedList('Optimizar las rutas de síntesis (top-down y/o bottom-up) de N-GQD',
                                         'Caracterizar integralmente los N-GQD sintetizados por TEM, FE-SEM, espectrofotometría UV-Vis, espectrofotometría de PL, FT-IR.',
                                         'Evaluar la respuesta de fluorescencia de los N-GQDs optimizados en presencia de nitritos en muestra controlada, ' \
                                         'determinando parámetros clave de desempeño como: sensibilidad, límite de detección (LOD) y estabilidad de la respuesta.',
                                         font_size=NORMAL_SIZE-2).next_to(title_slide_obj_esp,DOWN,buff=0.5)

        self.update_canvas()
        self.clear_allSlide_wipe(next_slide_content=[title_slide_obj_esp, objetivos_esp_tex])
        self.next_slide()
        self.clear_allSlide_fade()
    
    def metodologia(self):
        # animacion inicial para seccion
        self.update_canvas()
        self.section_title_animation(str_title='Metodología de síntesis')
        # contenido de seccion

        slide_content = {
            'titles': ['Metodología N-GQD (BC)', 'Metodología N-GQD (CA)', 'Metodología N-GQD (glu)'],
            'images': [('n-gqd_BC_photo.jpg', 'sintesis_n-gqd_BC.png'),
                       ('n-gqd_CA_photo.jpg', 'sintesis_n-gqd_CA.png'),
                       ('n-gqd_glu_photo.jpg', 'sintesis_n-gqd_glu.png')]
                       }
        
        num_slide = len(slide_content['titles'])
        rute_img = f'{HOME}\\'

        for i in range(num_slide):
            slide_title_met = Title(slide_content['titles'][i], font_size=TITLE_SIZE)

            photo = ImageMobject(rute_img + slide_content['images'][i][0]
                                 ).scale(0.3).to_edge(LEFT, buff=0.2).shift(DOWN)
            scheme_img = ImageMobject(rute_img + slide_content['images'][i][1]
                                      ).set_width(config.frame_width*0.75).to_edge(RIGHT, buff=0.2).shift(DOWN*0.5)
            
            self.play(FadeIn(mobj) for mobj in [slide_title_met, photo, scheme_img])
            self.update_canvas()
            self.next_slide()
            self.clear_allSlide_fade()
    
    def resultados(self):
        self.section_title_animation(str_title='Resultados')
        # ----- Diapositiva 1: Comparativos de espectros IR -----
        self.update_canvas()
        ftir_title = Title("Comparación de Espectros FTIR", font_size=TITLE_SIZE)
        self.canvas['title'] = ftir_title
        self.play(FadeIn(ftir_title))
        
        ftir_comparison = ImageMobject(f'{HOME}\\ftir_comparison.png').scale(1.1)
        self.play(FadeIn(ftir_comparison))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 2: Micrografías TEM -----
        self.update_canvas()
        nuevo_titulo = Text("Micrografías TEM", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        tem_images = ImageMobject(f'{HOME}\\N-GQDs_TEM.png').scale(1).to_edge(LEFT,buff=0.2)
        caption = Paragraph(
            "Micrografías por TEM sobre rejillas",
            "de carbono agujeradas. Las imágenes",
            "de incisos a) y b) pertenecen a N-GQD",
            "(BC),seguido de c) y d) que pertenecen",
            " a N-GQD (CA) y e) y f) para N-GQD (Glu).",
            font_size=NORMAL_SIZE-3,
            alignment="left"
        ).next_to(tem_images, RIGHT, buff=0.2)
        
        self.play(FadeIn(tem_images), Write(caption))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 3: Imágenes de SAED -----
        self.update_canvas()
        nuevo_titulo = Text("Patrones de SAED", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        saed_images = ImageMobject(f'{HOME}\\SAED_n_gqd.png').set_width(config.frame_width*0.8)
        self.play(FadeIn(saed_images))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 4: Arreglo espectrofotómetro PL in situ -----
        self.update_canvas()
        nuevo_titulo = Text("Espectrofotómetro PL In Situ", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        in_situ = ImageMobject(f'{HOME}\\in_situ_spectometer.png').set_width(config.frame_width*0.8)
        self.play(FadeIn(in_situ))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 5: Espectro comparativo PL -----
        self.update_canvas()
        nuevo_titulo = Text("Espectros PL de N-GQDs", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        pl_comparison = ImageMobject(f'{HOME}\\PL_spectra_N-GQD.png').scale(1.2).to_edge(LEFT, buff=0.3)
        pl_caption = VGroup(
            Text("Tiempo de integración: 15 s", font_size=NORMAL_SIZE-5),
            Text("Num. de mediciones: 5", font_size=NORMAL_SIZE-5),
            Text("[N-GQD]: 20 mg/mL", font_size=NORMAL_SIZE-5),
            Text("V = 1 mL", font_size=NORMAL_SIZE-5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(pl_comparison, RIGHT, buff=0.4)
        
        self.play(FadeIn(pl_comparison), Write(pl_caption))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 7: Subtítulo mediciones -----
        self.update_canvas()
        nuevo_titulo = Text("Análisis de Interacciones", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        mediciones_text = Paragraph(
            "Mediciones de PL y FT-IR en diluciones,",
            "pH y en presencia de nitritos.",
            font_size=NORMAL_SIZE,
            alignment="center"
        )
        self.play(Write(mediciones_text))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 8: PL influencia pH -----
        self.update_canvas()
        nuevo_titulo = Text("Efecto del pH en la fotoluminiscencia", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        ph_spectrum = ImageMobject(f'{HOME}\\PLspectra_pH.png').scale(1.5).to_edge(LEFT)
        ph_bars = ImageMobject(f'{HOME}\\Int_max_pH.png').scale(1).to_edge(RIGHT).shift(UP)
        perkin_img = ImageMobject(f'{HOME}\\perkin_elmer_specter.png').scale(0.8).to_corner(DR, buff=0.2)
        
        self.play(FadeIn(ph_spectrum), FadeIn(ph_bars))
        self.play(FadeIn(perkin_img))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 9: Efectos dilución -----
        self.update_canvas()
        nuevo_titulo = Text("Efecto de la Dilución en PL", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        dilution_spectrum = ImageMobject(f'{HOME}\\PL_espectro_diluciones_N-GQD.png').scale(0.75).to_edge(LEFT)
        dilution_bars = ImageMobject(f'{HOME}\\Int_max_diluciones.png').scale(0.95).to_edge(RIGHT)
        
        self.play(FadeIn(dilution_spectrum), FadeIn(dilution_bars))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 10: Interacción con nitritos -----
        self.update_canvas()
        nuevo_titulo = Text("Interacción con Nitritos", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        time_spectrum = ImageMobject(f'{HOME}\\PLspectra_tiempo_int.png').scale(1.3).to_edge(LEFT,buff=0.3)
        video = VideoMobject(f'{HOME}\\n-gqd_presencia_nitritos.mp4', speed=1.0, loop=True).scale(0.45).to_edge(RIGHT,buff=0.3)
        
        self.play(FadeIn(time_spectrum))
        self.play(FadeIn(video))
        self.wait(12)
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 11: FTIR con nitritos -----
        self.update_canvas()
        nuevo_titulo = Text("Análisis FTIR de Interacción", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        ftir_nitritos = ImageMobject(f'{HOME}\\ftir_n-gqd_comparison.png').scale(1.2)
        self.play(FadeIn(ftir_nitritos))
        self.next_slide()
        self.clear_slide_content()

        # ----- Diapositiva 15: Comparación curvas calibración -----
        self.update_canvas()
        nuevo_titulo = Title('Reacción de tipo Griess')
        self.play(Transform(self.canvas["title"], nuevo_titulo))

        rxr_griess_n_gqd = ImageMobject(f'{HOME}\\rxn_tipo_griess_n_gqd_esquema.png').scale(0.3)
        self.play(FadeIn(rxr_griess_n_gqd))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 12: Curva calibración 0-0.1M -----
        self.update_canvas()
        nuevo_titulo = Text("Curva de Calibración (0-0.1 M)", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        curve_spectrum = ImageMobject(f'{HOME}\\curva_intento_espectros.png').scale(1.5).to_edge(LEFT)
        curve_bars = ImageMobject(f'{HOME}\\Int_max_curva_0_1.png').scale(0.9).to_edge(RIGHT)
        
        self.play(FadeIn(curve_spectrum), FadeIn(curve_bars))
        self.next_slide()
        self.clear_slide_content()

        # ----- Diapositiva 13: Curva calibración 0-0.1M -----
        self.update_canvas()
        nuevo_titulo = Text("Curva de Calibración (0-0.1 M)", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        curve_intento = ImageMobject(f'{HOME}\\Curva_intento.png').scale(1.5).to_edge(RIGHT)
        draw_scientific = ImageMobject(f'{HOME}\\adorno_cientifico.png').scale(0.9).next_to(curve_intento, LEFT, buff=0.5)
        
        self.play(FadeIn(curve_intento), FadeIn(draw_scientific))
        self.next_slide()
        self.clear_slide_content()

        # ----- Diapositiva 14: Curva calibración 0-100uM -----
        self.update_canvas()
        nuevo_titulo = Text("Curva de Calibración (0-100 µM)", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        curve_spectrum1 = ImageMobject(f'{HOME}\\Curva1_espectros.png').scale(1.5).to_edge(LEFT)
        curve_bars1 = ImageMobject(f'{HOME}\\Int_max_curva_0_100uM.png').scale(0.9).to_edge(RIGHT)
        
        self.play(FadeIn(curve_spectrum1), FadeIn(curve_bars1))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 13: PL con diferentes longitudes de onda -----
        self.update_canvas()
        nuevo_titulo = Text("Dependencia de λ de Excitación", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        lambda_spectrum = ImageMobject(f'{HOME}\\PLspectra_scanEx.png').scale(1.35).to_edge(LEFT)
        perkin_img2 = ImageMobject(f'{HOME}\\perkin_elmer_specter.png').scale(0.7).to_corner(DR,buff=0.2)
        lambda_caption = Text("[N-GQD]: 1*10^4, V= 3 mL", font_size=NORMAL_SIZE).next_to(lambda_spectrum, RIGHT,buff=0.4)
        
        self.play(FadeIn(lambda_spectrum))
        self.play(FadeIn(perkin_img2), Write(lambda_caption))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 14: Curva calibración 2 -----
        self.update_canvas()
        nuevo_titulo = Text("Curva de Calibración (Perkin Elmer)", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        cal_spectrum2 = ImageMobject(f'{HOME}\\Curva2_espectros.png').scale(1.3).to_edge(LEFT,buff=0.2)
        cal_curve2 = ImageMobject(f'{HOME}\\Curva2.png').scale(1.3).to_edge(RIGHT,buff=0.2)
        cal_caption = Text("[N-GQD]: 1*10^4, V= 3 mL, λ = 395 nm", font_size=NORMAL_SIZE).to_edge(DOWN)
        
        self.play(FadeIn(cal_spectrum2), FadeIn(cal_curve2))
        self.play(Write(cal_caption))
        self.next_slide()
        self.clear_slide_content()
        
        # ----- Diapositiva 15: Comparación curvas calibración -----
        self.update_canvas()
        nuevo_titulo = Text("Curvas de Calibración", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        curve1 = ImageMobject(f'{HOME}\\Curva1.png').scale(1.25).to_edge(LEFT,buff=0.2)
        curve2 = ImageMobject(f'{HOME}\\Curva2.png').scale(1.25).to_edge(RIGHT,buff=0.2)
        curve1_label = Text("In situ", font_size=NORMAL_SIZE).next_to(curve1, DOWN)
        curve2_label = Text("Perkin Elmer", font_size=NORMAL_SIZE).next_to(curve2, DOWN)
        
        self.play(FadeIn(curve1), FadeIn(curve2))
        self.play(Write(curve1_label), Write(curve2_label))
        self.next_slide()
        self.clear_allSlide_fade()

    def discusion_conclusiones(self):
        self.section_title_animation(str_title='Conclusiones')
        # ----- Diapositiva 5: Conclusiones principales -----
        self.update_canvas()
        nuevo_titulo = Text("Conclusiones Principales", font_size=TITLE_SIZE).to_edge(UP)
        self.play(FadeIn(nuevo_titulo))
        
        conclusiones = VGroup(
            Text("1. Síntesis controlada:", font_size=NORMAL_SIZE),
            Text("   • Precursor carbonoso determina propiedades finales", font_size=NORMAL_SIZE),
            Text("   • Ácido cítrico produce N-GQD con tamaño homogéneo (3-5 nm)", font_size=NORMAL_SIZE),
            Text("   • Glucosa induce mayor funcionalización pero causa aglomeración", font_size=NORMAL_SIZE),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.9)
        
        conclusiones2 = VGroup(
            Text("2. Rendimiento óptico superior:", font_size=NORMAL_SIZE),
            Text("   • N-GQD(CA) combina alta intensidad PL con estabilidad espectral", font_size=NORMAL_SIZE),
            Text("3. Detección eficiente de nitritos:", font_size=NORMAL_SIZE),
            Text("   • Respuesta rápida (<30 s) y lineal en rango biológicamente relevante", font_size=NORMAL_SIZE),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.9)

        conclusiones3 = VGroup(
            Text("4. Bases para futuras investigaciones:", font_size=NORMAL_SIZE),
            Text("   • Mecanismos de quenching cuántico", font_size=NORMAL_SIZE),
            Text("   • Funcionalización superficial dirigida", font_size=NORMAL_SIZE),
            Text("   • Escalado de síntesis para aplicaciones prácticas", font_size=NORMAL_SIZE)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.9)
        
        self.play(Write(conclusiones))
        self.next_slide()
        self.wipe(conclusiones, conclusiones2)
        self.next_slide()
        self.wipe(conclusiones2, conclusiones3)
        self.next_slide()
        self.clear_allSlide_fade()
    
    def bibliografia(self):
        slide_title_bib = Title('Bibliografía', font_size=TITLE_SIZE)

        bibliografia = [f'bibliografia{n+1}.png' for n in range(3)]
        img_bib = ImageMobject(f'{HOME}\\{bibliografia[0]}').next_to(slide_title_bib,DOWN,buff=0.5)
        img_bib2 = ImageMobject(f'{HOME}\\{bibliografia[1]}').next_to(slide_title_bib,DOWN,buff=0.5)
        img_bib3 = ImageMobject(f'{HOME}\\{bibliografia[2]}').next_to(slide_title_bib,DOWN,buff=0.5)

        self.update_canvas()
        self.play(FadeIn(slide_title_bib), FadeIn(img_bib))
        self.next_slide()
        self.update_canvas()
        self.wipe(img_bib, img_bib2)
        self.next_slide()
        self.update_canvas()
        self.wipe(img_bib2, img_bib3)
        self.next_slide()
        self.clear_allSlide_fade()
    
    def agradecimientos(self):
        # Cargar y escalar imagen para pantalla completa
        img_agradecimientos = ImageMobject(f'{HOME}\\agradecimientos.png').scale(0.9)

        self.update_canvas()
        self.play(FadeIn(img_agradecimientos))
        self.next_slide()
        self.play(FadeOut(img_agradecimientos))

        # ----- Diapositiva 2: Segundos agradecimientos -----
        self.update_canvas()
        img_agradecimientos2 = ImageMobject(f'{HOME}\\agradecimientos2.png').scale(0.9)
        
        self.play(FadeIn(img_agradecimientos2))
        self.next_slide()
        self.play(FadeOut(img_agradecimientos2))