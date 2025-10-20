from manim import *
from utils import HOME, NORMAL_SIZE, TITLE_SIZE, TINY_SIZE

class Metodologia:
    @staticmethod
    def construct(self):
        Metodologia.metodologia(self)

    @staticmethod
    def metodologia(self):
        # animacion inicial para seccion
        self.update_canvas()
        self.section_title_animation(str_title='Metodología de síntesis')
        # contenido de seccion

        slide_content = {
            'titles': ['Metodología N-GQD (BC)', 'Metodología N-GQD (CA)', 'Metodología N-GQD (glu)'],
            'images': [('n-gqd_BC_photo.jpg', 'sintesis_n-gqd_BC.png'),
                       ('n-gqd_CA_photo.jpg', 'sintesis_n-gqd_CA.png'),
                       ('n-gqd_glu_photo.jpg', 'sintesis_n-gqd_glu.png')]
                       }
        
        num_slide = len(slide_content['titles'])
        rute_img = f'{HOME}\\'

        for i in range(num_slide):
            slide_title_met = Title(slide_content['titles'][i], font_size=TITLE_SIZE)

            photo = ImageMobject(rute_img + slide_content['images'][i][0]
                                 ).scale(0.3).to_edge(LEFT, buff=0.2).shift(DOWN)
            scheme_img = ImageMobject(rute_img + slide_content['images'][i][1]
                                      ).set_width(config.frame_width*0.75).to_edge(RIGHT, buff=0.2).shift(DOWN*0.5)
            
            self.play(FadeIn(mobj) for mobj in [slide_title_met, photo, scheme_img])
            self.update_canvas()
            self.next_slide()
            self.clear_allSlide_fade()