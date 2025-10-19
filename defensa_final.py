from manim import *
from utils import SlidesControl
# SECCIONES
from secciones.portada import Portada
from secciones.introduccion import Introduccion

# CONTROL GENERAL
class TesisDefensa(SlidesControl):
    def construct(self):
        Portada.construct(self)
        Introduccion.construct(self)
        