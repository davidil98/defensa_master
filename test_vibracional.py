from manim import *
from utils import SlidesControl, ManimGraph, TITLE_SIZE

# Para ejecutar esta prueba, usa el siguiente comando en tu terminal:
# manim -pql test_vibracional.py TestCaracterizacionVibracional

class TestCaracterizacionVibracional(SlidesControl):
    def construct(self):
        """
        Anima la comparación de espectros FT-IR, destacando los grupos funcionales.
        """
        # Inicializar el canvas para que funcione el control de diapositivas
        self.counter = 0
        slide_number = Text("1").to_corner(DL)
        self.add_to_canvas(slide_number=slide_number)

        slide_title = Title('Análisis de Grupos Funcionales (FT-IR)', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        self.play(Write(slide_title))

        # 1. Configurar la gráfica con el eje X invertido
        graph_helper = ManimGraph(self)
        axes_group = graph_helper.setup_axes(
            x_label=r"Número de onda (cm$^{-1}$)",
            y_label="Transmitancia (%)",
            x_range=[400, 4000, 500], # [start, end, step] -> Eje invertido
            y_range=[0, 110, 20],
            x_length=10,
            y_length=5,
        )
        axes_group.center()
        self.play(Create(axes_group))
        self.next_slide(notes="Comparamos los espectros FT-IR para verificar la funcionalización.")

        # 2. Graficar los espectros secuencialmente
        graph_ca = graph_helper.plot_spectrum("datos/FT-IR/N-GQD_BC_BLC.txt", color=GREEN)
        graph_bc = graph_helper.plot_spectrum("datos/FT-IR/N-GQD_CA_BLC.txt", color=ORANGE)
        graph_glu = graph_helper.plot_spectrum("datos/FT-IR/N-GQD_Glu_BLC.txt", color=GREY)
        
        self.play(Create(graph_ca), notes="Primero, el N-GQD derivado de Ácido Cítrico.")
        self.play(Create(graph_bc), notes="Luego, el de Carbón Negro.")
        self.play(Create(graph_glu), notes="Y finalmente, el de Glucosa.")
        self.next_slide()

        # 3. Crear la leyenda
        legend = graph_helper.create_legend([
            {"text": "N-GQD (CA)", "color": GREEN},
            {"text": "N-GQD (BC)", "color": ORANGE},
            {"text": "N-GQD (Glu)", "color": GREY},
        ], position=UL, buff=0.4)
        self.play(Write(legend))

        # 4. Animar las regiones de interés
        regiones_info = {
            "-NH (Aminas)": {"pos": 1650, "ancho": 100, "color": YELLOW},
            "-CONH2 (Amidas)": {"pos": 1510, "ancho": 100, "color": BLUE},
            "-COH (Alcoholes/Ácidos)": {"pos": 1010, "ancho": 150, "color": RED},
            "Alcanos/Aromáticos": {"pos": 2900, "ancho": 300, "color": PINK},
        }

        rectangulos = VGroup()
        for nombre, info in regiones_info.items():
            rect = Rectangle(
                height=graph_helper.axes.y_length,
                width=info["ancho"] / (abs(graph_helper.x_range[0] - graph_helper.x_range[1])) * graph_helper.axes.x_length,
                stroke_width=0,
                fill_color=info["color"],
                fill_opacity=0.2,
            ).move_to(graph_helper.axes.c2p(info["pos"], graph_helper.y_range[1]/2))
            
            label = Tex(nombre, font_size=20).next_to(rect, UP, buff=0.1)
            
            self.play(FadeIn(rect), Write(label), notes=f"Destacamos la región de {nombre}.")
            rectangulos.add(rect, label)
            self.wait(0.5)

        self.next_slide(notes="Todos los materiales muestran la incorporación exitosa de grupos funcionales, validando la síntesis.")
        self.wait(2)
