from manim import *
import locale
from datetime import datetime as dt
from utils import HOME

class Portada:
    @staticmethod
    def construct(self): # 'escena' es el 'self' de la clase principal
        Portada.portada(self)
    
    @staticmethod
    def portada(self):
        # Texto
        university_name = Tex(r'{\sc Universidad Autónoma de Nuevo León\\Facultad de Ciencias Químicas}',
                              font_size=33)
        posgrade_name = Tex(r'{\sc Maestría en Ciencias con Orientación en Química de los Materiales}',
                            font_size=28)
        titulo_tema = Tex(r'{\bf\sc Desarrollo de un Sensor Optoelectrónico Basado en Puntos Cuánticos de Grafeno para la Detección de Nitritos en Agua de Pozos Someros.}', # Corregido: "de"
                          font_size = 38)
        author_name = Tex(r'{\sc Autor: L.Q.I.\,David Ibarra Luna}',
                           font_size = 28)
        supervisor_name = Tex(r'{\sc Directora: Dra.\,Ma. Idalida del Consuelo Gómez de la Fuente}',
                              font_size = 23)
        cosupervisors_names = Tex(r'{\sc Co-directores:\\Dra.\,Oxana Visilievna Kharissova \hspace{0.5cm} Dr.\,Luis Arturo Obregón Zúñiga}',
                                  font_size=23)

        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8') # Localización
        fecha_actual = dt.now()
        location = 'Cd. Universitaria, San Nicolás de los Garza, N.L.'
        location_and_date = Tex(location +'\n'+ fecha_actual.strftime(' %A, %d de %B del %Y'),
                                font_size = 20)

        # Imagenes
        logo_uanl = ImageMobject(f'{HOME}\\UANL_logo.png').scale(0.15)
        logo_fcq = ImageMobject(f'{HOME}\\FCQ_logo.png')

        # Posicionar
        logo_uanl.to_corner(UR, buff=0.2)
        logo_fcq.to_corner(UL, buff=0.2)
        university_name.to_edge(UP, buff=0.6)
        posgrade_name.next_to(university_name, DOWN, buff=0.5)
        author_name.next_to(titulo_tema, DOWN, buff=0.6)
        supervisor_name.next_to(author_name, DOWN, buff=0.2)
        cosupervisors_names.next_to(supervisor_name, DOWN, buff=0.2)
        location_and_date.to_edge(DOWN, buff=0.2)

        # grupos
        logos = Group(logo_fcq, logo_uanl)
        info = VGroup(university_name, posgrade_name, author_name, supervisor_name, cosupervisors_names, location_and_date)

        # Poner en escena
        self.play(
            LaggedStart(
                FadeIn(logos[0], run_time=1.5),
                FadeIn(logos[1], run_time=1.5),
                lag_ratio=0.3
            )
        )

        self.play(Write(titulo_tema))
        self.play(Succession((FadeIn(texto) for texto in info), lag_ratio=0.8))

        # Borrar escena
        self.next_slide()
        self.play([FadeOut(mob) for mob in self.mobjects])