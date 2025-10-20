from manim import *
from utils import SlidesControl
# SECCIONES
from secciones.portada import Portada
from secciones.introduccion import Introduccion
from secciones.antecedentes import Antecedentes
from secciones.metodologia import Metodologia

# CONTROL GENERAL
class TesisDefensa(SlidesControl):
    def construct(self):
        Portada.construct(self)
        Introduccion.construct(self)
        Antecedentes.construct(self)
        Metodologia.construct(self)