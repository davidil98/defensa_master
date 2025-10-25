from manim import *
from utils import *

class Conclusiones:
    @staticmethod
    def construct(self):
        """
        Construye la secuencia final de Conclusiones y Trabajo a Futuro.
        """
        self.section_title_animation(str_title='Conclusiones')
        Conclusiones.hallazgos_principales(self)
        Conclusiones.contribucion_futuro(self)

    @staticmethod
    def hallazgos_principales(self):
        """
        Diapositiva 1: Resume los logros y hallazgos clave con datos numéricos.
        """
        self.update_canvas()
        slide_title = Title('Conclusiones: Hallazgos Principales', font_size=TITLE_SIZE)
        self.play(Write(slide_title))

        hallazgos = VGroup(
            Tex(r"\underline{\textbf{Síntesis y Caracterización}}"),
            BulletedList(
                "La síntesis con Ácido Cítrico produjo N-GQDs optimizados:",
                "Tamaño homogéneo de 3-5 nm (TEM).",
                "Alta intensidad de fluorescencia.",
                tex_environment="flushleft", buff=0.15
            ),
            Tex(r"\underline{\textbf{Rendimiento del Sensor}}"),
            BulletedList(
                r"Mecanismo de quenching validado (tipo Griess)\\ con respuesta rápida (menor 30s).",
                r"El Límite de Detección (LOD) del sistema\\ {\it in situ} fue de \textbf{10.83 µM}.",
                tex_environment="flushleft", buff=0.15
            )
        ).scale(0.6).arrange(DOWN, buff=1, aligned_edge=LEFT).next_to(slide_title, DOWN, buff=0.1)

        self.play(LaggedStart(
            Write(hallazgos[0]),
            Write(hallazgos[1]),
            lag_ratio=0.7, run_time=3
        ))
        self.next_slide(notes="Y se demostró que el sensor es rápido y suficientemente sensible.")
        
        self.play(LaggedStart(
            Write(hallazgos[2]),
            Write(hallazgos[3]),
            lag_ratio=0.7, run_time=3
        ))
        
        self.next_slide(notes="Nuestro trabajo se posiciona como una solución pragmática y efectiva para el monitoreo real.")
        self.clear_allSlide_fade()

    @staticmethod
    def contribucion_futuro(self):
        """
        Diapositiva 2: Presenta la contribución, el contexto y los siguientes pasos.
        """
        self.update_canvas()
        slide_title = Title('Contribución y Visión a Futuro', font_size=TITLE_SIZE)
        self.play(Write(slide_title))

        # Posicionamiento de tu trabajo con la tabla comparativa
        tabla_comparativa = ImageMobject(f"{HOME}/tables/tabla_comparativa_ngqd_nitritos.png").next_to(slide_title,DOWN, buff=0.8).scale(1.2)
        
        texto_contribucion = VGroup(
            Tex("Los resultados muestran un balance clave:", tex_environment="flushleft"),
            BulletedList(
                r"Suficiente sensibilidad para la NOM-127-SSA1-2021 (LOD $<$ 64.3 µM).",
                "Rapidez y simplicidad para su desarrollo y aplicación en campo.",
                tex_environment="flushleft"
            )
        ).scale(0.7).arrange(DOWN, aligned_edge=LEFT).next_to(tabla_comparativa, DOWN, buff=0.8)

        self.play(FadeIn(tabla_comparativa, shift=LEFT))
        self.play(Write(texto_contribucion))
        self.next_slide(notes="El primer paso es construir el prototipo físico portátil.")

        # Transición a Trabajo a Futuro
        trabajo_futuro_title = Tex(r"Trabajo\\a Futuro", font_size=TITLE_SIZE, color=YELLOW).to_corner(UL).shift(DOWN*2.5)
        self.play(
            FadeOut(tabla_comparativa, texto_contribucion),
            Transform(slide_title, trabajo_futuro_title)
        )

        # Esquema del prototipo final
        componentes = crear_diagrama_sensor_base()
        prototipo = VGroup(
            componentes["fuente"], componentes["selector"], componentes["muestra"],
            componentes["detector"], componentes["procesador"]
        ).arrange(RIGHT, buff=0.8).scale(0.6).next_to(trabajo_futuro_title, RIGHT, buff=0.5).shift(UP*0.3)
        
        # Labels para el prototipo
        labels_prototipo = VGroup(
            Tex("LED UV", font_size=18).next_to(componentes["fuente"], DOWN),
            Tex("Filtro", font_size=18).next_to(componentes["selector"], DOWN),
            Tex("Muestra", font_size=18).next_to(componentes["muestra"], DOWN),
            Tex("Fotodiodo", font_size=18).next_to(componentes["detector"], DOWN),
            Tex("Microcontrolador", font_size=18).next_to(componentes["procesador"], DOWN)
        )
        
        for comp in ["selector", "procesador"]:
            componentes[comp].set_opacity(1)

        self.play(FadeIn(prototipo, labels_prototipo))
        self.next_slide(notes="Y a largo plazo, integrar inteligencia artificial para crear un sistema de monitoreo inteligente y predictivo.")

        # Integración de IA
        cerebro_ia = ImageMobject(f"{HOME}/PyData.png", color=BLUE).scale(0.3).next_to(componentes["procesador"], RIGHT, buff=0.8)
        label_ia = Tex("Análisis IA", font_size=18).next_to(cerebro_ia, DOWN)
        flecha_ia = Arrow(componentes["procesador"].get_right(), cerebro_ia.get_left(), buff=0.2)
        
        texto_ia = BulletedList(
            "Validación en muestras reales.",
            "Corrección de interferencias (lambda de excitacion).",
            "Análisis predictivo de calidad del agua.",
            font_size=24
        ).next_to(prototipo, DOWN, buff=1.0, aligned_edge=LEFT).shift(LEFT)

        self.play(GrowArrow(flecha_ia), FadeIn(cerebro_ia), Write(label_ia))
        self.play(Write(texto_ia))
        self.next_slide()
        self.clear_allSlide_fade()