from manim import *
from utils import HOME, NORMAL_SIZE, TITLE_SIZE

class Antecedentes:
    @staticmethod
    def construct(self):
        Antecedentes.antecedentes(self)
        Antecedentes.analisis_critico_antecedentes(self)
        Antecedentes.aportacion_cientifica(self)
        Antecedentes.hipotesis(self)
        Antecedentes.objetivo_general(self)
        Antecedentes.objetivos_específicos(self)
        
    
    @staticmethod
    def antecedentes(self):
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
                                                        ).set_width(config.frame_width*0.8
                                                                    ).next_to(current_title_mobject, DOWN, buff=0.5)

            self.play(FadeIn(mobj) for mobj in [current_title_mobject, current_image_mobject_loaded])
            self.update_canvas()
            self.next_slide(notes="Este análisis crítico identifica las áreas de oportunidad para la presente investigación.")
            self.clear_allSlide_fade()
    
    @staticmethod
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

        self.clear_allSlide_wipe(next_slide_content=[slide_title_text, bullet_list_aport])
        self.update_canvas()
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