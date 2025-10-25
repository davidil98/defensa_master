from manim import *
from utils import ManimGraph

# Para ejecutar esta prueba, usa el siguiente comando en tu terminal:
# manim -pql test_utils.py TestGraphTool

class TestGraphSmoothing(Scene):
    def construct(self):
        """
        Una escena para probar la clase ManimGraph, mostrando cómo
        graficar datos y crear una leyenda por separado.
        """
        # 1. Título para la escena de prueba
        title = Text("Probando la Herramienta ManimGraph").to_edge(UP)
        self.play(Write(title))

        # 2. Instanciar y configurar la gráfica
        graph_helper = ManimGraph(self)
        axes_group = graph_helper.setup_axes(
            x_label=r"Número de onda (cm$^{-1}$)",
            y_label="Transmitancia (%)",
            x_range=[400, 4000, 500], # [start, end, step] -> Eje invertido
            y_range=[0, 110, 20],
            x_length=10,
            y_length=5,
        )
        axes_group.to_edge(DOWN, buff=0.8)
        self.play(Create(axes_group))
        self.wait(1)

        # 3. Graficar los datos crudos (smooth=False)
        status_text = Text("Graficando datos crudos...").next_to(axes_group, UP, buff=-1.5)
        self.play(Write(status_text))
        
        # plot_spectrum ahora solo devuelve la curva
        graph_raw = graph_helper.plot_spectrum("datos/FT-IR/N-GQD_BC_BLC.txt", color=BLUE, smooth=False)
        self.play(Create(graph_raw))
        self.wait(1)

        # 4. Graficar los datos suavizados para comparación
        new_status_text = Text("Graficando datos suavizados...").move_to(status_text)
        self.play(Transform(status_text, new_status_text))

        graph_smooth = graph_helper.plot_spectrum("datos/FT-IR/N-GQD_BC_BLC.txt", color=GREEN, smooth=True)
        self.play(Create(graph_smooth))
        self.wait(1)
        
        # 5. Crear y mostrar la leyenda por separado
        self.play(FadeOut(status_text))
        legend_items = [
            {"text": "N-GQD (BC) - Crudo", "color": BLUE},
            {"text": "N-GQD (BC) - Suavizado", "color": GREEN},
        ]
        legend = graph_helper.create_legend(legend_items, position=DR)
        self.play(Write(legend))
        self.wait(2)

        # 6. Indicar que la prueba ha finalizado
        completion_text = Text("Prueba Completada!", color=GREEN).to_edge(UP, buff=1.5)
        self.play(FadeOut(title), Write(completion_text))
        self.wait(2)
