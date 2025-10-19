from manim import *
from chanim import *
from utils import HOME, NORMAL_SIZE, TITLE_SIZE, TINY_SIZE, crear_diagrama_sensor_base

class Introduccion:
    @staticmethod
    def construct(self):
        Introduccion.introAgua(self)
        Introduccion.waterquality(self)
        Introduccion.nitritos(self)
        Introduccion.deteccionNitritos(self)
        Introduccion.desventajasDeteccion(self)
        Introduccion.sensoresOp(self)
    
    @staticmethod
    def introAgua(self):
        # canvas
        slide_title = Tex('Introducción', font_size=TITLE_SIZE).to_corner(UL)
        self.counter = 1
        slide_number = Text("1").to_corner(DL, buff=0.5)
        self.add_to_canvas(title=slide_title,slide_number=slide_number)

        # contenido texto
        tex = Paragraph('Históricamente, el agua siempre ha sido vital para garan-\ntizar la prosperidad de los asentamientos humanos.',
            alignment='right', line_spacing=0.8, font_size=NORMAL_SIZE
        ).to_corner(UR, buff=0.2).shift(DOWN)

        box = SurroundingRectangle(Group(slide_title, tex), color=WHITE, buff=0.2)

        img1 = ImageMobject(f'{HOME}\\watersample1.jpg').scale(1.8).shift(LEFT*3.5).shift(DOWN)
        img2 = ImageMobject(f'{HOME}\\watersample2.jpg').scale(1.8).shift(RIGHT*3.5).shift(DOWN)

        quoting = Tex('El aseguramiento de la calidad del agua se convierte en un desafío constante.',
                      font_size=NORMAL_SIZE).to_edge(DOWN, buff=0.5)

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
    
    @staticmethod
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
        description_diagram2 = Tex('Su bajo coste de operación, almacenamiento y construcción lo hace una opción viable y recurrente.',
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
    
    @staticmethod
    def nitritos(self):
        # Contenido
        slide_title_nitrites = Title('Nitritos como Contaminante de Aguas Subterráneas', font_size=TITLE_SIZE)
        tex_content_nitrite = Tex('Se considera un contaminante de interés en las aguas subterráneas.\n',
                      'Es un indicador de la contaminación agrícola, su solubilidad y permeabilidad\n',
                      'le permite filtrarse a través del suelo.', font_size=NORMAL_SIZE, tex_environment="flushleft"
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
    
    @staticmethod
    def deteccionNitritos(self):
        # contenido
        slide_title_deteccion = Tex('Detección de Nitritos en Agua', font_size=TITLE_SIZE).to_corner(UL, buff=0.5)
        tex_content_deteccion = Tex('Los métodos de detección convencionales utilizan reacciones colorimétricas\n',
                      'fundamentadas en la \\textbf{reacción de Griess}.', font_size=NORMAL_SIZE, tex_environment="flushleft"
                      ).to_edge(LEFT, buff=1).shift(UP*2)
        bibliography_nom = Tex('S. de Salud, “Norma Oficial Mexicana NOM-127-SSA1-2021, Agua Para Uso\n,'
                               ' y Consumo Humano, Límites Permisibles de la Calidad del Agua,” 2021.', font_size=TINY_SIZE, tex_environment='flushleft'
        ).next_to(self.canvas['slide_number'], RIGHT, buff=0.5)

        # Cambio de escena
        # --- Animación de la Reacción de Griess ---
        slide_title_rxn = Tex('Detección de Nitritos: Reacción de Griess', font_size=TITLE_SIZE).to_corner(UL, buff=0.5)
        chem_amina = r'H_2NO_2S-*6(-=-(-NH_2)=-=)'
        chem_nitrite = r'NO^{-}_2'
        chem_azide = r'H_2NO_2S-*6(-=-(-\chembelow{N}{H}-N=[:45]O)=-=)'
        chem_protonation = r'\arrow{->[\chemfig{+H^+}][\chemfig{H_2O}]}'
        rxn_first = Reaction(
            [chem_amina, chem_nitrite],
            [chem_azide, chem_protonation],
            arrow_text_up=r'\chemfig{+H^+}',
            arrow_text_down=r'\chemfig{H_2O}').scale(0.4).next_to(tex_content_deteccion, DOWN, buff=1)
        rxn_description = Tex(r'Sulfanilamida (Amina aromática) $\rightarrow$ grupo azo',
                                  font_size=NORMAL_SIZE).next_to(rxn_first, DOWN, buff=1)
        # rxn dos
        chem_diazo = 'H_2NO_2S-*6(-=-(-N^{+}~[:45]N)=-=)'
        chem_acoplante = '[:65]*6(=*6(-=-=-)-=(-*6(HN---H_2N))-=-)'
        chem_colorante = '*6(=*6(-(*6(-HN---NH_2))=-=(-N=[:-45]N(-*6(-=-(-SO_2NH_2)=-=)))-)-=-=-)'
        rxn_second = Reaction([chem_diazo, chem_acoplante],
                              [chem_colorante],
                              arrow_type='forward').scale(0.35).next_to(tex_content_deteccion, DOWN, buff=0.3)
        rxn_description2 = Tex(r'Sal de diazonio $+$ NED (Agente acoplante) $\rightarrow$ \text{Colorante Diazo}',
                                   font_size=NORMAL_SIZE).next_to(rxn_second, DOWN, buff=0.5)
        #Poner en escena
        self.update_canvas()
        self.canvas['title'] = slide_title_deteccion
        self.play(FadeIn(slide_title_deteccion),
                  FadeIn(tex_content_deteccion),
                  FadeIn(bibliography_nom))
        self.next_slide()
        self.play(Transform(slide_title_deteccion, slide_title_rxn))
        self.play(Write(rxn_first),
                  FadeIn(rxn_description))
        self.next_slide()
        self.play(Transform(rxn_description, rxn_description2),
                  Transform(rxn_first, rxn_second))
        # Cambio de escena
        self.next_slide()
        self.clear_allSlide_fade()

    @staticmethod
    def desventajasDeteccion(self):
        slide_title_oportunidad = Tex('Áreas de Oportunidad del Método Griess', font_size=TITLE_SIZE).to_corner(UL, buff=0.5)
        desventajas_detec_list = BulletedList(
            'Consumo de tiempo considerable.',
            'Requiere equipo de laboratorio robusto (espectrofotómetro).',
            'Manejo y desecho de reactivos peligrosos.',
            r'El análisis \textit{in situ} (en campo) es limitado.',
            font_size=NORMAL_SIZE,
            buff=0.4
        ).center().shift(DOWN*0.2)
        
        necesidad_tex = Tex("Se necesita una alternativa rápida, portátil y segura.", font_size=NORMAL_SIZE, color=YELLOW).next_to(desventajas_detec_list, DOWN, buff=1)

        self.play(
            FadeIn(slide_title_oportunidad)
        )
        
        self.update_canvas()
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT) for item in desventajas_detec_list], lag_ratio=0.3))
        self.play(Write(necesidad_tex))

        self.next_slide(notes='Estas limitaciones justifican la necesidad de desarrollar nuevas tecnologías, como los sensores optoelectrónicos...')
        self.clear_allSlide_fade()
    
    @staticmethod
    def sensoresOp(self):
        """
        Versión dinámica que construye el sensor paso a paso,
        mostrando las opciones de componentes según el guion del usuario.
        """
        # --- Diapositiva 1: Configuración Inicial ---
        self.update_canvas()
        slide_title = Title('Sensores Optoelectrónicos como Diseño Modular', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        self.play(Write(slide_title))

        # Crear el diagrama base usando la función de utils
        componentes = crear_diagrama_sensor_base()
        diagrama_base = VGroup(
            componentes["fuente"], componentes["fuente_label"],
            componentes["muestra"], componentes["muestra_label"],
            componentes["detector"], componentes["detector_label"]
        ).center().shift(UP * 1.5)
        
        # Área de contenido inferior
        texto_inferior = Tex("Permiten diseñar un instrumento a la medida con componentes asequibles.", font_size=NORMAL_SIZE).to_edge(DOWN, buff=1.5)
        
        self.play(
            LaggedStart(
                GrowFromCenter(componentes["fuente"], scale=0.5), Write(componentes["fuente_label"]),
                GrowFromCenter(componentes["muestra"], scale=0.5), Write(componentes["muestra_label"]),
                GrowFromCenter(componentes["detector"], scale=0.5), Write(componentes["detector_label"]),
                lag_ratio=0.5
            )
        )
        self.play(Write(texto_inferior))
        self.next_slide()

        # --- Paso 1: Fuente de Luz ---
        highlight_fuente = SurroundingRectangle(VGroup(componentes["fuente"], componentes["fuente_label"]), color=YELLOW)

        img_led = ImageMobject(f'{HOME}\\fuentes_luz_sensores.png').scale(0.5)
        label_led = Tex(r"(a) lámparas de descarga de gas, (b) LEDs acopladas a fibras ópticas y (c) diodos láser.", font_size=NORMAL_SIZE-10).next_to(img_led, DOWN)
        opcion_fuente = VGroup(img_led, label_led).move_to(texto_inferior.get_center())

        self.play(Create(highlight_fuente))
        self.wipe(texto_inferior, opcion_fuente)
        self.next_slide(notes="Primero, elegimos la fuente de luz.")

        # --- Paso 2: Selector de Onda ---
        highlight_selector = SurroundingRectangle(VGroup(componentes["selector"], componentes["selector_label"]), color=YELLOW)
        
        img_mono = ImageMobject(f'{HOME}\\selectores_sensores.png').scale(0.6)
        label_mono = Tex("(a) filtro de longitud de onda y (b) monocromadores", font_size=NORMAL_SIZE-10).next_to(img_mono, DOWN)
        opcion_selector = VGroup(img_mono, label_mono).move_to(texto_inferior.get_center())
        
        self.play(
            FadeOut(highlight_fuente),
            componentes["selector"].animate.set_opacity(1),
            componentes["selector_label"].animate.set_opacity(1),
        )

        self.play(Create(highlight_selector))
        self.wipe(texto_inferior, opcion_selector)
        self.next_slide(notes="Luego, añadimos un selector de onda.")

        # --- Paso 3: Elemento Sensibilizador ---
        elemento_sensibilizador = Tex("Elemento Sensibilizador", color=ORANGE).scale(0.7).move_to(componentes["muestra"])
        arrow_to_sample = Arrow(elemento_sensibilizador.get_bottom() + DOWN*0.2, componentes["muestra"].get_top(), buff=0.1, color=ORANGE)
        
        # Animación de rayos de luz
        rayo_in = Line(componentes["fuente"].get_right(), componentes["selector"].get_left(), color=PURPLE, stroke_width=5)
        rayo_mid1 = Line(componentes["selector"].get_right(), componentes["muestra"].get_left(), color=PURPLE, stroke_width=5)
        rayo_out = Line(componentes["muestra"].get_right(), componentes["detector"].get_left(), color=GREEN, stroke_width=5)
        
        self.play(FadeOut(highlight_selector, texto_inferior), notes="El corazón del sensor es el elemento en la muestra.")
        self.play(Write(elemento_sensibilizador), GrowArrow(arrow_to_sample))
        self.play(
            componentes["fuente"].submobjects[1].animate.set_color(PURPLE_B), # Cambiar color del emisor del LED
            ShowPassingFlash(rayo_in.copy().set_color(WHITE)),
            ShowPassingFlash(rayo_mid1.copy().set_color(WHITE)),
            ShowPassingFlash(rayo_out.copy().set_color(WHITE))
        )
        self.add(rayo_in, rayo_mid1, rayo_out)
        self.next_slide()
        
        # --- Paso 4: Detector de Luz ---
        highlight_detector = SurroundingRectangle(VGroup(componentes["detector"], componentes["detector_label"]), color=YELLOW)

        img_pmt = ImageMobject(f'{HOME}\\fotodetectores_sensores.png').scale(0.5)
        label_pmt = Tex("fotodetectores tipo (a) fotodiodos, (b) fotodiodos de avalancha y (c) fotomultiplicadores.", font_size=NORMAL_SIZE-10).next_to(img_pmt, DOWN)
        opcion_detector = VGroup(img_pmt, label_pmt).move_to(texto_inferior.get_center())

        self.play(FadeOut(elemento_sensibilizador, arrow_to_sample))
        self.play(Create(highlight_detector))
        self.play(FadeIn(opcion_detector))
        self.next_slide(notes="El detector convierte la luz en una señal eléctrica.")
        
        # --- Paso 5: Procesador de Señal ---
        highlight_procesador = SurroundingRectangle(VGroup(componentes["procesador"], componentes["procesador_label"]), color=YELLOW)
        linea_a_procesador = DashedLine(componentes["detector"].get_right(), componentes["procesador"].get_left(), color=ORANGE)
        texto_final = Tex("Convierte la señal eléctrica en un dato legible (ej. concentración).", font_size=NORMAL_SIZE).to_edge(DOWN, buff=1.5)

        self.play(
            FadeOut(highlight_detector),
            FadeOut(opcion_detector),
            componentes["procesador"].animate.set_opacity(1),
            componentes["procesador_label"].animate.set_opacity(1),
        )
        self.play(Create(highlight_procesador))
        self.play(Create(linea_a_procesador), Write(texto_final), notes="Finalmente, un procesador interpreta la señal.")
        self.next_slide()

        self.clear_allSlide_fade()