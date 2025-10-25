from manim import *
from utils import *

class BiblyAgradecimientos:
    @staticmethod
    def construct(self):
        BiblyAgradecimientos.bibliografia(self)
        BiblyAgradecimientos.agradecimientos(self)

    @staticmethod
    def bibliografia(self):
        """
        Construye la sección de Bibliografía, presentando las referencias
        como texto animado en varias diapositivas.
        """

        # --- Diapositiva 1 ---
        self.update_canvas()
        slide_title = Title('Bibliografía', font_size=TITLE_SIZE)
        self.play(Write(slide_title))

        refs1 = VGroup(
            Tex(r"1. Vikesland PJ. Nanosensors for water quality monitoring. \textit{Nature Nanotechnology} 2018; 13:651–60.", tex_environment="flushleft"),
            Tex(r"2. Nuevo León G de. Emite Gobierno de NL Declaratoria de Emergencia por sequía. Consultado el 10 de octubre de 2023. Available from: https://www.nl.gob.mx/boletines-comunicados-y-avisos/emite-gobierno-de-nl-declaratoria-de-emergencia-por-sequia", tex_environment="flushleft"),
            Tex(r"3. Nuevo León G de. Incrementa Agua y Drenaje número de pozos someros y profundos. Consultado el 10 de octubre de 2023. 2023. Available from: https://www.n1.gob.mx/boletines-comunicados-y-avisos/incrementa-agua-y-drenaje-numero-de-pozos-someros-y-profundos", tex_environment="flushleft"),
            Tex(r"4. Qiu G, Han Y, Zhu X, Gong J, Luo T, Zhao C, et al. Sensitive Detection of Sulfide Ion Based on Fluorescent Ionic Liquid—Graphene Quantum Dots Nanocomposite. Frontiers in Chemistry. 2021;9(April):1-8.", tex_environment="flushleft"),
        ).scale(0.5).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center().shift(DOWN*0.5)

        self.play(Write(refs1))
        self.next_slide()
        
        # --- Diapositiva 2 ---
        self.update_canvas()
        refs2 = VGroup(
            Tex(r"5. Munawar A, Ong Y, Schirhagl R, Tahir MA, Khan WS y Bajwa SZ. Nanosensors for diagnosis with optical, electric and mechanical transducers. RSC Advances 2019; 9:6793-803. D01: 10. 1039/c8ra10144b", tex_environment="flushleft"),
            Tex(r"6. Troudi N, Hamzaoui-Azaza F, Tzoraki O, Melki F y Zammouri M. Assessment of ground-water quality for drinking purpose with special emphasis on salinity and nítrate contami-nation in the shallow aquifer of Guenniche (Northern Tunisia). Environmental Monitoring and Assessment 2020 Sep; 192. D01: 10.1007/s10661-020-08584-9", tex_environment="flushleft"),
            Tex(r"7. Aparicio JAC, Ponce H y Rudamas C. Interlayer transition in graphene carbon quantum dots. \textit{MRS Advances} 2020. 2020 Dec; 5:3345-52. Doi.10.1557/adv.2020.410", tex_environment="flushleft"),
            Tex(r"8. Saleh TA. Nanomaterials: Classification, properties, and environmental toxicities. Envi-ronmental Technology \& Innovation 2020 Nov; 20:101067. DOI10.1016/j.eti.2020.101067", tex_environment="flushleft"),
        ).scale(0.5).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center().shift(DOWN*0.5)

        self.play(Transform(refs1, refs2))
        self.next_slide()

        # --- Diapositiva 3 ---
        self.update_canvas()
        refs3 = VGroup(
            Tex(r"9. Ghaffarkhah A, Hosseini E, Kamkar M, Sehat AA, Dordanihaghighi S, Allahbakhsh A, Kuur C van der y Arjmand M. Synthesis, Applications, and Prospects of Graphene Quantum Dots: A Comprehensive Review. Small 2021 Sep; 18. DOI: 10.1002/small.202102683", tex_environment="flushleft"),
            Tex(r"10. Yoon H, Park M, Kim J, Novak TG, Lee S y Jeon S. Toward highly efficient luminescence in graphene quantum dots for optoelectronic applications. Chemical Physics Reviews 2021 Jul; 2. DOI: 10.1063/5.0049183", tex_environment="flushleft"),
            Tex(r"11. Nesakumar N, Srinivasan S y Alwarappan S. Graphene quantum dots: synthesis, pro-perties, and applications to the development of optical and electrochemical sensors for chemical sensing. Microchimica Acta 2022 Jun; 189. DOI: 10.1007/s00604-022-05353-Y", tex_environment="flushleft"),
            Tex(r"12. Kurniawan D, Chen YY, Sharma N, Rahardja MR y Chiang WH. Graphene Quantum Dot-Enabled Nanocomposites as Luminescence- and Surface-Enhanced Raman Scattering Biosensors. Chemosensors 2022 Nov; 10:498. DOI 10.3390/chemosensors10120498", tex_environment="flushleft"),
        ).scale(0.5).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center().shift(DOWN*0.5)
        
        self.play(Transform(refs1, refs3))
        self.next_slide()
        self.clear_allSlide_fade()
    
    @staticmethod
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