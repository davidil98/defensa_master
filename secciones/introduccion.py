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
        Introduccion.intro_nanomateriales(self)
        Introduccion.nanomateriales(self)
        Introduccion.gqd(self)
        Introduccion.gqd_quenching(self)
        Introduccion.cierre_intro(self)
    
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
            componentes['selector'], componentes['selector_label'],
            componentes["muestra"], componentes["muestra_label"],
            componentes["detector"], componentes["detector_label"],
            componentes['procesador'], componentes['procesador_label']
        ).center().shift(UP)
        
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
        self.next_slide(notes="Primero, elegimos la fuente de luz.")

        # --- Paso 1: Fuente de Luz ---
        highlight_fuente = SurroundingRectangle(VGroup(componentes["fuente"], componentes["fuente_label"]), color=YELLOW)

        img_led = ImageMobject(f'{HOME}\\fuentes_luz_sensores.png').scale(0.5)
        label_led = Tex(r"(a) lámparas de descarga de gas, (b) LEDs acopladas a fibras ópticas y (c) diodos láser.", font_size=NORMAL_SIZE-10).next_to(img_led, DOWN)
        opcion_fuente = Group(img_led, label_led).move_to(texto_inferior.get_center())

        self.play(Create(highlight_fuente))
        self.wipe(texto_inferior, opcion_fuente)
        self.next_slide(notes="Luego, añadimos un selector de onda.")

        # --- Paso 2: Selector de Onda ---
        highlight_selector = SurroundingRectangle(VGroup(componentes["selector"], componentes["selector_label"]), color=YELLOW)
        
        img_mono = ImageMobject(f'{HOME}\\selectores_sensores.png').scale(0.6)
        label_mono = Tex("(a) filtro de longitud de onda y (b) monocromadores", font_size=NORMAL_SIZE-10).next_to(img_mono, DOWN)
        opcion_selector = Group(img_mono, label_mono).move_to(texto_inferior.get_center())
        
        self.play(
            FadeOut(highlight_fuente),
            componentes["selector"].animate.set_opacity(1),
            componentes["selector_label"].animate.set_opacity(1),
        )

        self.play(Create(highlight_selector))
        self.wipe(opcion_fuente, opcion_selector)
        self.next_slide(notes="El corazón del sensor es el elemento en la muestra.")

        # --- Paso 3: Elemento Sensibilizador ---
        elemento_sensibilizador = Tex("Elemento Sensibilizador", font_size=NORMAL_SIZE, color=ORANGE).next_to(componentes["muestra"], DOWN, buff=1)
        arrow_to_sample = Arrow(elemento_sensibilizador.get_top() + UP*0.1, componentes["muestra"].get_center(), buff=0.1, color=ORANGE)
        
        # Animación de rayos de luz
        rayo_in = Line(componentes["fuente"].get_right(), componentes["selector"].get_left(), color=PURPLE, stroke_width=5)
        rayo_mid1 = Line(componentes["selector"].get_right(), componentes["muestra"].get_left(), color=PURPLE, stroke_width=5)
        rayo_out = Line(componentes["muestra"].get_right(), componentes["detector"].get_left(), color=GREEN, stroke_width=5)
        
        self.play(FadeOut(highlight_selector, opcion_selector))
        self.play(Write(elemento_sensibilizador), GrowArrow(arrow_to_sample))
        self.play(
            componentes["fuente"].submobjects[1].animate.set_color(PURPLE_B), # Cambiar color del emisor del LED
            ShowPassingFlash(rayo_in.copy().set_color(WHITE)),
            ShowPassingFlash(rayo_mid1.copy().set_color(WHITE)),
            ShowPassingFlash(rayo_out.copy().set_color(WHITE))
        )
        self.add(rayo_in, rayo_mid1, rayo_out)
        self.next_slide(notes="El detector convierte la luz en una señal eléctrica.")
        
        # --- Paso 4: Detector de Luz ---
        highlight_detector = SurroundingRectangle(VGroup(componentes["detector"], componentes["detector_label"]), color=YELLOW)

        img_pmt = ImageMobject(f'{HOME}\\fotodetectores_sensores.png').scale(0.5)
        label_pmt = Tex("fotodetectores tipo (a) fotodiodos, (b) fotodiodos de avalancha y (c) fotomultiplicadores.", font_size=NORMAL_SIZE-10).next_to(img_pmt, DOWN)
        opcion_detector = Group(img_pmt, label_pmt).move_to(texto_inferior.get_center())

        self.play(FadeOut(elemento_sensibilizador, arrow_to_sample))
        self.play(Create(highlight_detector))
        self.play(FadeIn(opcion_detector))
        self.next_slide(notes="Finalmente, un procesador interpreta la señal.")
        
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
        self.play(Create(linea_a_procesador), Write(texto_final))
        self.next_slide()

        self.clear_allSlide_fade()
    
    @staticmethod
    def intro_nanomateriales(self):
        """
        Introduce la diferencia entre materiales bulk y nanomateriales,
        destacando la fluorescencia como propiedad clave para los sensores.
        Utiliza una semilla de np.random para animaciones consistentes.
        """
        np.random.seed(0)

        # --- Título de la diapositiva ---
        self.update_canvas()
        slide_title_NM = Title('Nanomateriales vs. Materiales Bulk', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title_NM
        self.play(Write(self.canvas['title']))

        # --- Parte 1: Material Bulk ---
        bulk_material_label = Tex("Material Bulk", font_size=NORMAL_SIZE).to_edge(UP, buff=1.8).shift(LEFT * 3.5)
        bulk_material = Rectangle(width=3.5, height=2.5, color=BLUE_E, fill_opacity=0.7).next_to(bulk_material_label, DOWN, buff=0.4)

        # Átomos desorganizados (ahora con posiciones reproducibles)
        bulk_atoms = VGroup()
        for _ in range(35):
            x_offset = np.random.uniform(-bulk_material.width / 2 + 0.2, bulk_material.width / 2 - 0.2)
            y_offset = np.random.uniform(-bulk_material.height / 2 + 0.2, bulk_material.height / 2 - 0.2)
            bulk_atoms.add(Dot(radius=0.06, color=random_bright_color()).move_to(bulk_material.get_center() + RIGHT * x_offset + UP * y_offset))

        bulk_group = VGroup(bulk_material_label, bulk_material, bulk_atoms)
        self.play(FadeIn(bulk_group, shift=RIGHT))
        self.next_slide(notes="Los materiales bulk tienen propiedades ópticas predecibles.")

        # Interacción de la luz con el material bulk
        light_source_bulk = Dot(bulk_material.get_left() + LEFT * 2.5 + UP * 0.5, color=YELLOW)
        incident_light_bulk = Arrow(light_source_bulk.get_center(), bulk_material.get_left() + UP * 0.5, buff=0.1, color=YELLOW, stroke_width=6)
        reflected_light_bulk = Arrow(bulk_material.get_left() + UP * 0.5, bulk_material.get_left() + LEFT * 1.5 + UP * 1.2, buff=0.1, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        absorbed_text_bulk = Tex("Absorción y Reflexión simple", font_size=NORMAL_SIZE).next_to(bulk_material, DOWN, buff=0.5)

        self.play(Create(light_source_bulk))
        self.play(GrowArrow(incident_light_bulk))
        self.play(GrowArrow(reflected_light_bulk), Write(absorbed_text_bulk), run_time=1)
        self.next_slide(notes="Pero al reducir la dimensionalidad a nanoescala, emergen propiedades cuánticas.")
        self.play(FadeOut(light_source_bulk, incident_light_bulk, reflected_light_bulk, absorbed_text_bulk))

        # --- Parte 2: Transición a Nanomateriales ---
        nano_material_label = Tex("Nanomateriales (Puntos Cuánticos)", font_size=NORMAL_SIZE).to_edge(UP, buff=1.8).shift(RIGHT * 3.5)
        nano_area = Circle(radius=1.5, color=DARK_BLUE, fill_opacity=0.3).next_to(nano_material_label, DOWN, buff=0.4)
        
        # Simular puntos cuánticos (posiciones fijas para consistencia)
        qds = VGroup(*[
            Dot(radius=0.18, color=BLUE_D).move_to(nano_area.get_center() + pos)
            for pos in [
                RIGHT * 0.8 + UP * 0.3, LEFT * 0.5 + UP * 0.8,
                RIGHT * 0.1 + DOWN * 0.9, LEFT * 0.9,
                RIGHT * 0.9 + DOWN * 0.2, LEFT*0.2 + DOWN*0.4
            ]
        ])

        nano_group = VGroup(nano_material_label, nano_area, qds)
        self.play(Transform(bulk_group, nano_group), run_time=1.5)
        self.next_slide(notes="Estos materiales, como los puntos cuánticos de grafeno, pueden exhibir fluorescencia.")

        # --- Parte 3: Fenómeno de Fluorescencia ---
        light_source_nano = Dot(nano_area.get_left() + LEFT * 2.5, color=PURPLE_A)
        incident_light_nano = Arrow(light_source_nano.get_center(), nano_area.get_center() + LEFT * nano_area.radius * 0.8, buff=0.1, color=PURPLE_C, stroke_width=6)

        self.play(Create(light_source_nano))
        self.play(GrowArrow(incident_light_nano))

        # Animación de fluorescencia (emisión de luz)
        emitted_lights_nano = VGroup()
        colors_emission = [GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E, LIGHT_BROWN]
        
        animations = []
        for i, qd in enumerate(qds):
            # Animar el "encendido" de cada punto cuántico
            animations.append(qd.animate.set_color(colors_emission[i]))
        self.play(LaggedStart(*animations, lag_ratio=0.1))

        for i, qd in enumerate(qds):
            # Emiten luz en varias direcciones (ahora reproducibles)
            for j in range(3):
                angle = TAU * j / 3 + np.random.uniform(-0.2, 0.2)
                direction = np.array([np.cos(angle), np.sin(angle), 0])
                emitted_ray = Arrow(qd.get_center(), qd.get_center() + direction * 0.8, buff=0.05, color=colors_emission[i], stroke_width=4, max_tip_length_to_length_ratio=0.3)
                emitted_lights_nano.add(emitted_ray)
        
        fluorescence_text = Tex(r"Fluorescencia:\\Absorción UV $\rightarrow$ Emisión Visible", font_size=NORMAL_SIZE).next_to(nano_area, DOWN, buff=0.5)
        self.play(LaggedStart(*[GrowArrow(ray) for ray in emitted_lights_nano], lag_ratio=0.05), Write(fluorescence_text))

        self.next_slide(notes="Esta propiedad es la que los convierte en excelentes elementos sensibilizadores.")
        
        # Conclusión final
        conclusion_text = Paragraph(
            "Su capacidad de convertir luz UV en visible",
            "es la clave para el diseño de un sensor.",
            font_size=NORMAL_SIZE, alignment="center"
        ).to_edge(DOWN)
        
        # Eliminar todo excepto el título y el grupo nano
        elementos_a_quitar = VGroup(light_source_nano, incident_light_nano, emitted_lights_nano, fluorescence_text)
        self.play(FadeOut(elementos_a_quitar))
        self.play(Write(conclusion_text))

        self.next_slide()
        self.clear_allSlide_fade()
    
    @staticmethod
    def nanomateriales(self):
        """
        Versión resumida y enfocada que muestra la progresión de los nanomateriales 
        a base de carbono, desde el grafito hasta el GQD.
        """
        self.update_canvas()
        slide_title = Title('Nanomateriales a Base de Carbono', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        
        description = Tex("Deriva de la familia del grafeno:", font_size=NORMAL_SIZE).next_to(slide_title, DOWN, buff=0.4)
        self.play(Write(slide_title), Write(description))
        self.next_slide(notes="Comenzamos con el grafito, un material 3D.\n"+
                        "Al exfoliarlo, obtenemos grafeno, una lámina 2D.\n"+
                        "Que puede enrollarse en nanotubos de 1D.\n"+
                        "Y al fragmentarlo, llegamos a los puntos cuánticos de grafeno.")

        # --- Cargar y posicionar todos los elementos ---
        grafito = ImageMobject(f'{HOME}\\graphite.png').set_height(2)
        grafeno = ImageMobject(f'{HOME}\\graphene.png').set_height(2)
        nanotubo = SVGMobject(f'{HOME}\\nanotube.svg').set_height(2)
        gqd = SVGMobject(f'{HOME}\\gqd_structure.svg').set_height(2)
        
        estructuras = Group(grafito, grafeno, nanotubo, gqd).arrange(RIGHT, buff=1.5).center().shift(UP*0.5)

        # Etiquetas
        label_grafito = Tex("Grafito (3D Bulk)", font_size=NORMAL_SIZE-8).next_to(grafito, DOWN)
        label_grafeno = Tex("Grafeno (2D)", font_size=NORMAL_SIZE-8).next_to(grafeno, DOWN)
        label_nanotubo = Tex("Nanotubo (1D)", font_size=NORMAL_SIZE-8).next_to(nanotubo, DOWN)
        label_gqd = Tex("Punto Cuántico (0D)", font_size=NORMAL_SIZE-8).next_to(gqd, DOWN)
        labels = VGroup(label_grafito, label_grafeno, label_nanotubo, label_gqd)

        # Flechas de progresión
        arrow1 = Arrow(grafito.get_right(), grafeno.get_left(), buff=0.3)
        arrow2 = Arrow(grafeno.get_right(), nanotubo.get_left(), buff=0.3)
        arrow3 = Arrow(nanotubo.get_right(), gqd.get_left(), buff=0.3)
        arrows = VGroup(arrow1, arrow2, arrow3)

        # --- Animación Secuencial ---
        self.play(FadeOut(description))

        # 1. Aparece el Grafito
        self.play(FadeIn(grafito), Write(label_grafito))
        self.play(GrowArrow(arrow1))

        # 2. Aparece el Grafeno
        self.play(FadeIn(grafeno), Write(label_grafeno))
        self.play(GrowArrow(arrow2))

        # 3. Aparece el Nanotubo
        self.play(FadeIn(nanotubo), Write(label_nanotubo))
        self.play(GrowArrow(arrow3))

        # 4. Aparece el GQD (el importante)
        self.play(FadeIn(gqd), Write(label_gqd))
        self.next_slide()
        self.clear_allSlide_fade()
    
    @staticmethod
    def gqd(self):
        """
        Versión reescrita que presenta los GQD y su funcionalización como un
        proceso de 'ingeniería' para sintonizar sus propiedades ópticas.
        """
        # --- Diapositiva 1: Propiedades del GQD ---
        self.update_canvas()
        slide_title_gqd = Title('Puntos Cuánticos de Grafeno (GQD)', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title_gqd

        gqd_pristino = SVGMobject(f'{HOME}\\gqd_structure.svg').scale(2).to_edge(LEFT, buff=1)
        
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
        
        self.play(Write(slide_title_gqd))
        self.play(FadeIn(gqd_pristino), Write(propiedades_heredadas))
        self.next_slide(notes="La propiedad clave es que su fluorescencia puede ser modificada.")
        
        gqd_fluorescente = SVGMobject(f'{HOME}\\gqd_fluorescence.svg').scale(2).move_to(gqd_pristino)
        
        self.play(ReplacementTransform(gqd_pristino, gqd_fluorescente), Write(propiedades_unicas))
        self.next_slide()
        
        # --- Diapositiva 2: Sintonizando la Fluorescencia ---
        self.clear_slide_content()

        # Configuración de ejes para el espectro PL
        axes = Axes(
            x_range=[400, 700, 50], y_range=[0, 1.8, 0.5],
            x_length=7, y_length=4,
            axis_config={"include_numbers": True, "font_size": 21}
        ).to_edge(RIGHT, buff=1)
        x_label = axes.get_x_axis_label(Tex("Longitud de Onda (nm)"), edge=DOWN, direction=DOWN, buff=0.35)
        y_label = axes.get_y_axis_label(Tex("Intensidad PL (u.a.)").rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.35)
        pl_plot_group = VGroup(axes, x_label, y_label)
        self.play(Create(pl_plot_group))

        # Función para generar curvas gaussianas
        def get_pl_curve(amplitude, center_wl=525, sigma=35, color=GREEN_C):
            return axes.plot(
                lambda x: amplitude * np.exp(-((x - center_wl)**2) / (2 * sigma**2)),
                color=color, stroke_width=4
            )

        # Datos para la animación de funcionalización (narrativa de "ingeniería")
        gqd_data = [
            {"file": f'{HOME}\\gqd_fluorescence.svg', "name": "GQD Base", "amplitude": 0.4, "color": BLUE_D, "notes": "La estructura base del GQD ya posee una fluorescencia fundamental."},
            {"file": f'{HOME}\\go_dots.svg', "name": "GO-dots (Oxigenado)", "amplitude": 0.7, "color": BLUE_B, "notes": "Añadir grupos de oxígeno (GO-dots) modifica y a menudo aumenta la fluorescencia."},
            {"file": f'{HOME}\\n_gqd.svg', "name": "N-GQD (Nitrogenado)", "amplitude": 1.5, "color": GREEN_B, "notes": "El dopaje con nitrógeno es una estrategia clave para maximizar el rendimiento cuántico."}
        ]

        # Elementos que se transformarán
        current_gqd_svg = SVGMobject(gqd_data[0]["file"]).scale(1.7).to_edge(LEFT, buff=0.8)
        current_gqd_label = Tex(gqd_data[0]["name"], font_size=NORMAL_SIZE).next_to(current_gqd_svg, DOWN)
        current_pl_curve = get_pl_curve(gqd_data[0]["amplitude"], color=gqd_data[0]["color"])

        self.play(
            DrawBorderThenFill(current_gqd_svg),
            Write(current_gqd_label),
            Create(current_pl_curve),
            notes=gqd_data[0]["notes"]
        )
        self.next_slide()

        # Transformaciones secuenciales
        for data in gqd_data[1:]:
            new_gqd_svg = SVGMobject(data["file"]).scale(1.7).move_to(current_gqd_svg)
            new_gqd_label = Tex(data["name"], font_size=NORMAL_SIZE).next_to(new_gqd_svg, DOWN)
            new_pl_curve = get_pl_curve(data["amplitude"], color=data["color"])

            self.play(
                Transform(current_gqd_svg, new_gqd_svg),
                Transform(current_gqd_label, new_gqd_label),
                Transform(current_pl_curve, new_pl_curve)
            )
            self.next_slide(notes=data["notes"] +"\nAdemás, el nitrógeno nos da los 'ganchos' químicos que necesitamos para que la reacción con nitritos funcione.")

        # Conclusión final de la sección
        highlight_text = Tex(r"Estrategia Clave:\\Alto Rendimiento Cuántico", font_size=NORMAL_SIZE, color=GREEN_B).next_to(current_pl_curve, UP, buff=0.2)
        final_note = Tex(r"...y provee los grupos amino (-NH$_2$) necesarios para la detección.", font_size=NORMAL_SIZE).to_edge(DOWN, buff=0.2)
        
        self.play(Write(highlight_text))
        self.play(Write(final_note))
        
        self.next_slide(notes="Partimos del N-GQD, que muestra una alta fluorescencia inicial.")
        self.clear_allSlide_fade()
    
    @staticmethod
    def gqd_quenching(self):
        """
        Versión pulida que explica el mecanismo de extinción de fluorescencia
        vinculándolo explícitamente a una reacción tipo Griess en la superficie del N-GQD.
        """
        # Fijar la semilla para reproducibilidad
        np.random.seed(1)
        
        # --- Diapositiva 1: El Estado Inicial ---
        self.update_canvas()
        slide_title_quenching = Title('Mecanismo de Detección: Extinción de Fluorescencia', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title_quenching

        # Configuración de N-GQD y espectro PL (similar a antes)
        n_gqd_svg = SVGMobject(f'{HOME}\\n_gqd.svg').scale(1.4).to_edge(LEFT, buff=0.8)
        n_gqd_label = Tex("N-GQD", font_size=NORMAL_SIZE).next_to(n_gqd_svg, DOWN)
        
        # Configuración de ejes para el espectro PL
        axes = Axes(
            x_range=[400, 700, 50], y_range=[0, 1.8, 0.5],
            x_length=7, y_length=4,
            axis_config={"include_numbers": True, "font_size": 21}
        ).to_edge(RIGHT, buff=1).shift(UP*0.5)
        x_label = axes.get_x_axis_label(Tex("Longitud de Onda (nm)", font_size=NORMAL_SIZE), edge=DOWN, direction=DOWN, buff=0.35)
        y_label = axes.get_y_axis_label(Tex("Intensidad PL (u.a.)", font_size=NORMAL_SIZE).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.35)
        pl_plot_group = VGroup(axes, x_label, y_label)

        def get_pl_curve(amplitude, color=GREEN_B):
            return axes.plot(lambda x: amplitude * np.exp(-((x - 525)**2) / (2 * 35**2)), color=color, stroke_width=4)

        initial_amplitude = 1.5
        current_pl_curve = get_pl_curve(initial_amplitude)

        self.play(Write(slide_title_quenching))
        self.play(
            DrawBorderThenFill(n_gqd_svg),
            Write(n_gqd_label),
            Create(pl_plot_group),
            Create(current_pl_curve)
        )
        self.next_slide(notes="La reacción, al igual que la de Griess, requiere un medio ácido.")

        # --- Diapositiva 2: El Mecanismo Químico ---
        ph_acido_tex = Tex(r"Medio Ácido ($H^+$)", font_size=NORMAL_SIZE+2, color=RED_A).next_to(n_gqd_svg, UP, buff=0.8)
        nitrito_mol = Tex(r"$NO_2^-$", font_size=NORMAL_SIZE, color=ORANGE).next_to(n_gqd_svg, DOWN).shift(LEFT*2)
        
        # Representación del grupo amino en la superficie
        grupo_amino = Tex(r"-NH$_2$", color=YELLOW).next_to(ph_acido_tex, DOWN, buff=0.2).shift(RIGHT)
        
        self.play(Write(ph_acido_tex), )
        self.play(FadeIn(grupo_amino, scale=0.5))
        self.play(FadeIn(nitrito_mol, shift=LEFT))
        self.next_slide(notes="El nitrógeno dopante provee grupos amino en la superficie.")

        # Transformación química
        grupo_diazo = Tex(r"-N=N-", color=RED).move_to(grupo_amino)
        explanation_text = Tex(r"Reacción tipo Griess en la superficie:", font_size=NORMAL_SIZE-4).to_edge(DOWN, buff=1)
        explanation_text2 = Tex(r"El grupo amino se convierte en un \textbf{grupo diazo}, un 'quencher' de fluorescencia.", font_size=NORMAL_SIZE-4).next_to(explanation_text, DOWN)
        
        new_pl_curve = get_pl_curve(initial_amplitude * 0.8, color=RED_D) # caída baja

        self.play(nitrito_mol.animate.move_to(grupo_amino.get_center() + LEFT*0.2))
        self.play(
            ReplacementTransform(grupo_amino, grupo_diazo),
            FadeOut(nitrito_mol),
            Transform(current_pl_curve, new_pl_curve),
            Write(explanation_text),
            )
        self.play(Write(explanation_text2))
        self.next_slide()

        # --- Diapositiva 3: Efecto de la Concentración ---
        self.play(FadeOut(grupo_diazo, explanation_text, explanation_text2))
        
        concentracion_label = Tex("Concentración de $NO_2^-$:", font_size=NORMAL_SIZE).center().to_edge(DOWN, buff=0.6).shift(LEFT)
        concentracion_valor = Tex("Baja", font_size=NORMAL_SIZE+2, color=YELLOW).next_to(concentracion_label, RIGHT, buff=1)
        self.play(Write(concentracion_label), Write(concentracion_valor))

        quenching_steps = [
            {"amplitude": 0.5, "conc_text": "Media", "color": RED_B},
            {"amplitude": 0.2, "conc_text": "Alta", "color": RED_D}
        ]
             
        nitritos_group = VGroup()
        for step in quenching_steps:
            new_nitritos = VGroup(*[
                Tex("$NO_2^-$", font_size=NORMAL_SIZE-4, color=step["color"]).move_to(
                    n_gqd_svg.get_center() + np.array([r * np.cos(a), r * np.sin(a), 0])
                )
                for r, a in zip(np.random.uniform(1.2, 1.8, 3), np.random.uniform(0, TAU, 3))
            ])
            nitritos_group.add(*new_nitritos)

            new_pl_curve = get_pl_curve(step["amplitude"], color=step["color"])
            new_conc_valor = Tex(step["conc_text"], font_size=NORMAL_SIZE-2, color=step["color"]).move_to(concentracion_valor)

            self.next_slide(notes=f"Al aumentar la concentración a {step['conc_text']}, la fluorescencia sigue disminuyendo.")
            self.play(
                FadeIn(new_nitritos, lag_ratio=0.1),
                Transform(current_pl_curve, new_pl_curve),
                Transform(concentracion_valor, new_conc_valor)
            )

        self.next_slide(notes="Unimos todos los componentes asequibles que hemos seleccionado.")
        self.clear_allSlide_fade()

    @staticmethod
    def cierre_intro(self):
        """
        Cierra la introducción presentando el concepto final del sensor,
        integrando el N-GQD como el elemento sensibilizador clave.
        """
        # --- Diapositiva 1: El Sensor Conceptual ---
        self.update_canvas()
        slide_title = Title('Propuesta Conceptual del Sensor', font_size=TITLE_SIZE)
        self.canvas['title'] = slide_title
        
        # Usar la función de utils para crear el diagrama base
        componentes = crear_diagrama_sensor_base()
        
        # Personalizar etiquetas para nuestro diseño final
        componentes["fuente_label"].become(Tex("LED UV (~365 nm)", font_size=NORMAL_SIZE - 2).next_to(componentes["fuente"], UP, buff=0.3))
        componentes["selector_label"].become(Tex("Filtro (~510 nm)", font_size=NORMAL_SIZE - 2).next_to(componentes["selector"], DOWN, buff=0.3))
        componentes["detector_label"].become(Tex("Fotodiodo de Si", font_size=NORMAL_SIZE - 2).next_to(componentes["detector"], UP, buff=0.3))
        componentes["muestra_label"].become(Tex("Muestra Acuosa", font_size=NORMAL_SIZE - 2).next_to(componentes["muestra"], UP, buff=0.3))

        # Hacer visibles todos los componentes del diagrama
        for comp in ["selector", "procesador"]:
            componentes[comp].set_opacity(1)
            componentes[comp+"_label"].set_opacity(1)

        diagrama_completo = VGroup(*componentes.values()).center().shift(UP)
        
        self.play(Write(slide_title))
        self.play(LaggedStart(
            *[FadeIn(comp) for comp in componentes.values()],
            lag_ratio=0.1
        ))
        self.next_slide(notes="El componente clave es nuestro nanomaterial.")

        # --- Animación del Elemento Sensibilizador ---
        n_gqd_svg = SVGMobject(f'{HOME}\\n_gqd.svg').scale(1.5).to_edge(DOWN, buff=0.5)
        label_n_gqd = Tex(r"\textbf{N-GQD}", font_size=NORMAL_SIZE, color=YELLOW).next_to(n_gqd_svg, UP)
        
        self.play(FadeIn(n_gqd_svg, shift=UP), Write(label_n_gqd))
        self.wait(1)
        
        # El N-GQD se convierte en el elemento sensibilizador
        elemento_sensibilizador = Tex("Elemento Sensibilizador", font_size=NORMAL_SIZE-3, color=ORANGE).move_to(componentes["muestra"]).shift(DOWN)
        
        self.play(
            ReplacementTransform(n_gqd_svg, elemento_sensibilizador),
            FadeOut(label_n_gqd)
        )
        self.wait(1)
        
        # Simular puntos cuánticos (posiciones fijas para consistencia)
        nano_area = Circle(radius=0.6, color=LIGHT_BROWN, fill_opacity=0.3).move_to(componentes["muestra"].get_center())
        qds = VGroup(*[
            Dot(radius=0.12, color=GREY_BROWN).move_to(nano_area.get_center() + pos)
            for pos in [
                RIGHT * 0.4 + UP * 0.3, LEFT * 0.3 + UP * 0.1,
                RIGHT * 0.1 + DOWN * 0.1, LEFT * 0.2,
                RIGHT * 0.3 + DOWN * 0.2, LEFT*0.2 + DOWN*0.4
            ]
        ])
        nano_label = Text('N-GQD', font_size=NORMAL_SIZE-8).next_to(nano_area, DOWN, buff=0.3)
        nano_group = VGroup(nano_area, qds, nano_label)

        self.play(ReplacementTransform(elemento_sensibilizador, nano_group))

        self.next_slide(notes="El LED UV emite luz..." \
                        "...el N-GQD la absorbe y emite luz visible..." \
                            "...que es medida por el fotodiodo..." \
                                "...y convertida en un resultado.")

        # Animación final del funcionamiento
        rayo_in = Line(componentes["fuente"].get_right(), componentes["selector"].get_left(), color=PURPLE)
        rayo_mid = Line(componentes["selector"].get_right(), componentes["muestra"].get_left(), color=PURPLE)
        rayo_out = Line(componentes["muestra"].get_right(), componentes["detector"].get_left(), color=GREEN)
        linea_procesador = DashedLine(componentes["detector"].get_right(), componentes["procesador"].get_left(), color=ORANGE)
        # continua el paso de luz
        self.play(ShowPassingFlash(rayo_in.copy().set_stroke(width=8)))
        self.play(ShowPassingFlash(rayo_mid.copy().set_stroke(width=8)))
        # Animación de fluorescencia (emisión de luz)
        colors_emission = [GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E, LIGHT_BROWN]
        
        animations = []
        for i, qd in enumerate(qds):
            # Animar el "encendido" de cada punto cuántico
            animations.append(qd.animate.set_color(colors_emission[i]))
        self.play(LaggedStart(*animations, lag_ratio=0.1))
        # continua el paso de luz
        self.play(ShowPassingFlash(rayo_out.copy().set_stroke(width=8)))
        self.play(ShowPassingFlash(linea_procesador.copy().set_stroke(width=8)))
        
        self.add(rayo_in, rayo_mid, rayo_out, linea_procesador)
        self.wait(1)
        self.next_slide(notes="Esto nos lleva a las preguntas centrales de la investigación.")

        # --- Diapositiva 2: Preguntas de Investigación ---
        preguntas_finales = VGroup(
            Tex(r"Para realizar este concepto, debemos responder:", font_size=NORMAL_SIZE),
            BulletedList(
                "¿Qué método de síntesis produce los N-GQD con mejores propiedades ópticas?",
                "¿Cómo se caracterizan para confirmar su estructura y rendimiento?",
                "¿Cuál es su desempeño real en la detección de nitritos?",
                font_size=NORMAL_SIZE, buff=0.4
            )
        ).arrange(DOWN, buff=0.8).center()

        self.clear_slide_content()
        self.play(Write(preguntas_finales))

        self.next_slide(notes="Las siguientes secciones responderán a estas preguntas.")
        self.clear_allSlide_fade()