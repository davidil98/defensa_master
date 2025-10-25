from manim import *
from utils import *

class Metodologia:
    @staticmethod
    def construct(self):
        """
        Construye la secuencia completa de la metodología, incluyendo la
        nueva sección de caracterización.
        """
        self.section_title_animation(str_title='Metodología')
        Metodologia.sintesis(self)
        Metodologia.caracterizacion(self)

    @staticmethod
    def sintesis(self):
        """
        Presenta los diferentes métodos de síntesis de N-GQD.
        (Este es tu método anterior, renombrado para mayor claridad)
        """
        slide_content = {
            'titles': ['Síntesis N-GQD (Carbón Negro)', 'Síntesis N-GQD (Ácido Cítrico)', 'Síntesis N-GQD (Glucosa)'],
            'images': [('n-gqd_BC_photo.jpg', 'sintesis_n-gqd_BC.png'),
                       ('n-gqd_CA_photo.jpg', 'sintesis_n-gqd_CA.png'),
                       ('n-gqd_glu_photo.jpg', 'sintesis_n-gqd_glu.png')]
        }
        
        for i in range(len(slide_content['titles'])):
            self.update_canvas()
            slide_title_met = Title(slide_content['titles'][i], font_size=TITLE_SIZE)
            
            # Asegúrate de que los archivos de imagen estén en la carpeta 'figures'
            photo = ImageMobject(f"{HOME}/{slide_content['images'][i][0]}").scale(0.3).to_edge(LEFT, buff=0.5).shift(DOWN)
            scheme_img = ImageMobject(f"{HOME}/{slide_content['images'][i][1]}").set_width(config.frame_width * 0.7).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
            
            self.play(Write(slide_title_met), FadeIn(photo), FadeIn(scheme_img))
            self.next_slide()
            self.clear_allSlide_fade()

    @staticmethod
    def caracterizacion(self):
        """
        Nueva sección que resume las técnicas de caracterización utilizadas.
        """
        self.update_canvas()
        slide_title = Title('Caracterización', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        self.play(Write(slide_title))

        # Etapa 1: Caracterización Comparativa
        etapa1_title = Tex("Etapa 1: Caracterización Inicial", color=YELLOW).to_edge(LEFT).shift(UP*2)
        
        tecnicas1 = BulletedList(
            "Morfología y Tamaño (TEM)",
            "Estructura Cristalina (SAED)",
            "Grupos Funcionales (FT-IR)",
            "Rendimiento de Fluorescencia (PL)",
            font_size=NORMAL_SIZE
        ).next_to(etapa1_title, DOWN, aligned_edge=LEFT, buff=0.5)

        # Etapa 2: Caracterización del Campeón y Pruebas
        etapa2_title = Tex("Etapa 2: Caracterización Detallada y Pruebas de Sensado", color=YELLOW).to_edge(LEFT).shift(UP*2)

        tecnicas2 = BulletedList(
            r"Interacción N-GQD/$NO_{2}^{-}$ (PL, FT-IR)",
            "Propiedades Ópticas (UV-Vis)",
            "Estudios de Sensado (PL vs [Nitrito])",
            font_size=NORMAL_SIZE
        ).next_to(etapa2_title, DOWN, aligned_edge=LEFT, buff=0.4)

        self.play(Write(etapa1_title))
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT) for item in tecnicas1], lag_ratio=0.2))
        self.next_slide()
        
        self.play(ReplacementTransform(etapa1_title,etapa2_title))
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT) for item in tecnicas2], lag_ratio=0.2))
        self.next_slide(notes="Estas pruebas se realizaron con un sistema a la medida.")

        # Transición al sistema in situ
        sistema_in_situ_img = ImageMobject(f'{HOME}\spectrometer_in_situ_diagram.png').scale_to_fit_width(config.frame_width * 0.75).next_to(slide_title, DOWN, buff=0.5)
        sistema_in_situ_title = Title("Sistema de Medición de Fluorescencia In Situ", font_size=TITLE_SIZE)

        self.play(
            FadeOut(VGroup(etapa1_title, tecnicas1, etapa2_title, tecnicas2)),
            Transform(slide_title, sistema_in_situ_title)
        )
        self.play(FadeIn(sistema_in_situ_img))
        self.next_slide(notes="Este sistema nos permite evaluar el rendimiento en una configuración simple y de bajo costo, similar a un prototipo de campo.")
        self.clear_allSlide_fade()