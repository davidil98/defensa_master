from manim import *
from utils import * # Importar ManimGraph

class Resultados:
    @staticmethod
    def construct(self):
        """
        Construye la secuencia completa de la sección de resultados.
        """

        Resultados.caracterizacion_vibracional(self)
        Resultados.caracterizacion_morfologica_tem(self)
        Resultados.caracterizacion_comparativa_pl(self)
        Resultados.caracterizacion_detallada_ca(self)
        Resultados.evaluacion_sensor(self)

    @staticmethod
    def caracterizacion_vibracional(self):
        """
        Anima la comparación de espectros FT-IR, destacando los grupos funcionales.
        """
        self.update_canvas()
        slide_title = Title('Análisis de Grupos Funcionales (FT-IR)', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        self.play(Write(slide_title))

        # 1. Configurar la gráfica con el eje X invertido
        graph_helper = ManimGraph(self)
        axes_group = graph_helper.setup_axes(
            x_label=r"Número de onda (cm$^{-1}$)",
            y_label=r"Transmitancia (\%)",
            x_range=[400, 4000, 500], # [start, end, step] -> Eje invertido
            y_range=[0, 110, 20],
            x_length=10,
            y_length=5,
        )
        axes_group.center().scale(0.8).shift(DOWN)
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
        ], position=DR, buff=0.4)
        self.play(Write(legend))

        # 4. Animar las regiones de interés
        regiones_info = {
            "-NH": {"pos": 1650, "ancho": 100, "color": YELLOW},
            "-CONH2": {"pos": 1510, "ancho": 100, "color": BLUE},
            "-COH": {"pos": 1010, "ancho": 150, "color": RED},
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
            
            label = Tex(nombre, font_size=20).next_to(rect, DOWN, buff=0.1)
            
            self.play(FadeIn(rect), Write(label))
            rectangulos.add(rect, label)
            self.wait(0.5)

        self.next_slide(notes="Todos los materiales muestran la incorporación exitosa de grupos funcionales, validando la síntesis.")
        self.clear_allSlide_fade()
    
    @staticmethod
    def caracterizacion_morfologica_tem(self):
        """
        Presenta los resultados de TEM utilizando ZoomedScene para
        enfocarse en los detalles de cada tipo de N-GQD usando un ZoomManager.
        """
        # --- Configuración inicial de la escena ---
        self.update_canvas()
        slide_title = Title('Análisis Morfológico (TEM)', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        
        # Cargar la imagen de TEM completa
        tem_images = ImageMobject(f"{HOME}/N-GQDs_TEM.png").scale(1).center()
        
        # Etiquetas para cada panel
        label_bc = Tex("a, b) N-GQD (BC)").scale(0.7).to_edge(LEFT, buff=0.7)
        label_ca = Tex("c, d) N-GQD (CA)").scale(0.7).next_to(label_bc, DOWN, buff=0.6)
        label_glu = Tex("e, f) N-GQD (Glu)").scale(0.7).next_to(label_ca, DOWN, buff=0.6)

        self.play(Write(slide_title))
        self.play(FadeIn(tem_images))
        self.play(Write(VGroup(label_bc, label_ca, label_glu)))
        self.next_slide()
        
        # --- Zoom 1: N-GQD (BC) ---
        # Crear un "frame" o marco de zoom
        zoom_frame_bc = Rectangle(width=1.25, height=1.25, color=YELLOW).move_to(tem_images.get_corner(DL) + UR*1.5)
        
        self.play(Create(zoom_frame_bc))
        # Activar el zoom. Manim se encarga de la animación.
        self.activate_zooming(animate=True)
        self.play(self.zoomed_camera.frame.animate.move_to(zoom_frame_bc).set_width(zoom_frame_bc.width * 1.05))
        
        # Añadir anotaciones en la vista de zoom
        texto_zoom_bc = Tex(r"Partículas de 20-30 nm\\Distribución Heterogénea", font_size=NORMAL_SIZE).to_corner(UR, buff=0.5)
        self.play(Write(texto_zoom_bc))
        self.wait(1)
        self.next_slide(notes="El N-GQD (BC) muestra partículas grandes y poco uniformes.")

        # --- Zoom 2: N-GQD (CA) - El Candidato Ideal ---
        zoom_frame_ca = Rectangle(width=1, height=1, color=GREEN).move_to(tem_images.get_center() + LEFT)
        
        self.play(Transform(zoom_frame_bc, zoom_frame_ca))
        # Mover la cámara de zoom al nuevo frame
        self.play(self.zoomed_camera.frame.animate.move_to(zoom_frame_ca))
        
        texto_zoom_ca = Tex(r"\textbf{Partículas de 3-5 nm}", r"\\ \textbf{Morfología Homogénea}", font_size=32, color=GREEN).to_corner(DR, buff=0.5)
        self.play(FadeOut(texto_zoom_bc, shift=DOWN), FadeIn(texto_zoom_ca, shift=UP))
        self.wait(1)
        self.next_slide(notes="En contraste, el N-GQD (CA) muestra un excelente control morfológico, con partículas pequeñas y consistentes.")

        # --- Zoom 3: N-GQD (Glu) ---
        zoom_frame_glu = Rectangle(width=1.5, height=1.5, color=RED).move_to(tem_images.get_corner(DR) + UL*1.4)
        
        self.play(Transform(zoom_frame_bc, zoom_frame_glu))
        # Mover la cámara de zoom al nuevo frame
        self.play(self.zoomed_camera.frame.animate.move_to(zoom_frame_glu))
        
        texto_zoom_glu = Tex("Aglomeración Significativa", font_size=32, color=RED).to_corner(UL, buff=1)
        self.play(FadeOut(texto_zoom_ca, shift=DOWN), FadeIn(texto_zoom_glu, shift=UP))
        self.wait(1)
        self.next_slide(notes="Finalmente, el N-GQD (Glu) tiende a aglomerarse, lo cual no es ideal.")

        # --- Conclusión y salida del zoom ---
        # Desactivar el zoom para volver a la vista normal
        self.activate_zooming(animate=False)
        self.play(FadeOut(zoom_frame_bc, texto_zoom_glu))

        conclusion_text = Tex("La morfología homogénea del N-GQD (CA) es clave para un rendimiento reproducible.", font_size=NORMAL_SIZE).to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)
        
        self.clear_allSlide_fade()

        # ----- Imágenes de SAED -----
        self.update_canvas()
        nuevo_titulo = Text("Patrones de SAED", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        saed_images = ImageMobject(f'{HOME}\\SAED_diffractions.png').next_to(nuevo_titulo, DOWN).set_width(config.frame_width*0.7)
        self.play(FadeIn(saed_images))
        self.next_slide(notes="Comparamos la intensidad relativa de la fluorescencia bajo condiciones idénticas.")
        self.clear_slide_content()
    
    @staticmethod
    def caracterizacion_comparativa_pl(self):
        self.update_canvas()
        nuevo_titulo = Text("Caracterización Comparativa de PL", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Transform(self.canvas["title"], nuevo_titulo))
        
        pl_comparison = ImageMobject(f'{HOME}\\pl_ngqd_comparison.png').set_width(config.frame_width*0.5).to_edge(LEFT, buff=0.3).shift(DOWN)
        pl_caption = VGroup(
            Text("Tiempo de integración: 15 s", font_size=NORMAL_SIZE-5),
            Text("Num. de mediciones: 5", font_size=NORMAL_SIZE-5),
            Text("[N-GQD]: 20 mg/mL", font_size=NORMAL_SIZE-5),
            Text("V = 1 mL", font_size=NORMAL_SIZE-5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(pl_comparison, RIGHT, buff=0.4)
        
        self.play(FadeIn(pl_comparison), Write(pl_caption))
        self.next_slide(notes="Su Band Gap confirma la absorción en el rango UV, justificando el uso de un LED de 365 nm.")
        self.clear_allSlide_fade()
    
    # -------------- ETAPA 2 --------------
    @staticmethod
    def caracterizacion_detallada_ca(self):
        """
        Subsección 2: Caracterización del N-GQD (CA) seleccionado.
        """
        # --- Diapositiva 4: Tauc Plot ---
        self.update_canvas()
        slide_title = Title('Caracterización de N-GQD (CA): Propiedades Ópticas', font_size=TITLE_SIZE)
        self.play(FadeIn(slide_title))
        
        tauc_img = ImageMobject(f'{HOME}/grafico_tauc_ngqd_ca.png').set_width(config.frame_width*0.42).to_edge(LEFT, buff=0.5)
        uv_vis_img = ImageMobject(f'{HOME}/uv_vis_ngqd_ca.png').set_width(config.frame_width*0.42).to_edge(RIGHT, buff=0.5)
        conclusion_tauc = Tex(r"Band Gap Óptico $\approx$ 3.20 eV", font_size=NORMAL_SIZE).to_edge(DOWN)
        highlight_bandgap = SurroundingRectangle(tauc_img.copy().scale(0.3).move_to(tauc_img.get_center()+DOWN*0.8+LEFT*0.5), color=YELLOW)
        
        self.play(FadeIn(tauc_img),
                  FadeIn(uv_vis_img))
        self.play(Create(highlight_bandgap), Write(conclusion_tauc))
        self.next_slide(notes="El pH 3 es óptimo, ya que proporciona una señal fuerte y cumple el requisito de acidez para la reacción de detección.")
        self.clear_allSlide_fade()

        # --- Diapositiva 5: Efecto en estabilidad optica ---
        self.update_canvas()
        self.play(slide_title.animate.become(Title('Caracterización de N-GQD (CA): Estabilidad Óptica', font_size=TITLE_SIZE)))
        
        estabilidad_op_img = ImageMobject(f'{HOME}/pl_ngqd_ca_effects_combined.png').set_width(config.frame_width*0.85).center()
        self.play(FadeIn(estabilidad_op_img))
        self.next_slide()
        self.clear_allSlide_fade()
    
    @staticmethod
    def evaluacion_sensor(self):
        """
        Subsección 3: Pruebas de rendimiento del N-GQD (CA) como sensor.
        """
        # --- Diapositiva 6: Tiempo de Reacción ---
        self.update_canvas()
        slide_title = Title('Rendimiento del Sensor: Tiempo de Respuesta', font_size=TITLE_SIZE)
        self.play(Write(slide_title))

        time_spectrum = ImageMobject(f'{HOME}/plTime_irNitrites_spectra.png').scale_to_fit_width(config.frame_width*0.75).to_edge(LEFT, buff=0.5)
        video = VideoMobject(f'{HOME}/n-gqd_presencia_nitritos.mp4', loop=True).scale(0.25).to_edge(RIGHT, buff=1)
        conclusion_time = Tex("Respuesta de Quenching Rápida (menor 30s)", color=YELLOW, font_size=NORMAL_SIZE).to_edge(DOWN)

        self.play(FadeIn(time_spectrum), FadeIn(video))
        self.play(Write(conclusion_time))
        self.wait(5) # Dejar el video correr un poco
        self.next_slide(notes="El resultado más importante: el límite de detección.")
        self.clear_allSlide_fade()
        
        # --- Diapositiva 6: Tiempo de Reacción ---
        self.update_canvas()
        slide_title = Title('Rendimiento del Sensor: Curva de Calibración', font_size=TITLE_SIZE)
        self.play(Write(slide_title))

        in_situ_curve = ImageMobject(f'{HOME}/calibration_curve_series.png').scale_to_fit_width(config.frame_width*0.85).to_edge(LEFT, buff=1)
        nom_text = Tex(r"Significativamente inferior al límite de la NOM-127 ($64.3 \mu M$)", font_size=NORMAL_SIZE).next_to(in_situ_curve, DOWN, buff=0.5)

        self.play(FadeIn(in_situ_curve), Write(nom_text))
        self.next_slide(notes="Se logró una síntesis controlada que produjo un nanomaterial con las características deseadas.")
        self.clear_allSlide_fade()