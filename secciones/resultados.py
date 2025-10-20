from manim import *
from utils import * # Importar ManimGraph

class Resultados:
    @staticmethod
    def construct(self):
        """
        Construye la secuencia completa de la sección de resultados.
        """
        self.section_title_animation(str_title='Resultados')
        Resultados.caracterizacion_comparativa(self)

    @staticmethod
    def caracterizacion_comparativa(self):
        """
        Anima la comparación de espectros PL para seleccionar el N-GQD "campeón".
        """
        self.update_canvas()
        slide_title = Title('Selección del Nanomaterial: Rendimiento Fotoluminiscente', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        self.play(Write(slide_title))

        # 1. Instanciar y configurar la gráfica
        graph_helper = ManimGraph(self)
        axes_group = graph_helper.setup_axes(
            x_label="Longitud de onda (nm)",
            y_label="Intensidad PL (u.a.)",
            x_range=[300, 700, 100],
            y_range=[0, 3500, 500]
        )
        axes_group.to_edge(DOWN, buff=0.8)
        self.play(Create(axes_group))

        # 2. Graficar cada espectro secuencialmente
        self.next_slide(notes="Evaluamos tres precursores para la síntesis de N-GQD.")
        
        # N-GQD (BC)
        plot_bc = graph_helper.plot_spectrum("datos/n_gqd_bc.csv", color=ORANGE, label_text="N-GQD (BC)", smooth=True)
        self.play(Create(plot_bc[0]), Write(plot_bc[1]), notes="El Carbón Negro (BC) muestra una fluorescencia moderada.")
        self.next_slide()

        # N-GQD (Glu)
        plot_glu = graph_helper.plot_spectrum("datos/n_gqd_glu.csv", color=BLUE, label_text="N-GQD (Glu)", smooth=True)
        self.play(Create(plot_glu[0]), Write(plot_glu[1]), notes="La Glucosa (Glu) presenta un rendimiento cuántico bajo.")
        self.next_slide()

        # N-GQD (CA) - El Campeón
        plot_ca = graph_helper.plot_spectrum("datos/n_gqd_ca.csv", color=GREEN, label_text="N-GQD (CA)", smooth=True)
        self.play(ShowPassingFlash(plot_ca[0].copy().set_color(YELLOW), time_width=0.5), run_time=1.5)
        self.play(Create(plot_ca[0]), Write(plot_ca[1]), notes="El Ácido Cítrico (CA) resulta en una fluorescencia notablemente superior.")
        self.next_slide()

        # 3. Conclusión de la selección
        conclusion_box = SurroundingRectangle(plot_ca, color=YELLOW, buff=0.2)
        conclusion_text = VGroup(
            Tex("Selección del Candidato:", font_size=NORMAL_SIZE),
            Tex(r"\textbf{N-GQD (CA)}", font_size=NORMAL_SIZE, color=YELLOW),
            Tex("Por su alta intensidad de fluorescencia.", font_size=NORMAL_SIZE-4)
        ).arrange(DOWN).to_corner(UL, buff=1.0)

        self.play(Create(conclusion_box))
        self.play(Write(conclusion_text), notes="Por lo tanto, seleccionamos el N-GQD (CA) para el desarrollo del sensor.")
        
        self.next_slide()
        self.clear_allSlide_fade()