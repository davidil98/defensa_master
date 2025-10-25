from manim import *
from utils import SlidesControl
# SECCIONES
from secciones.portada import Portada
from secciones.introduccion import Introduccion
from secciones.antecedentes import Antecedentes
from secciones.metodologia import Metodologia
from secciones.resultados import Resultados
from secciones.conclusiones import Conclusiones
from secciones.bibl_y_agradeimientos import BiblyAgradecimientos

# CONTROL GENERAL
class TesisDefensa(SlidesControl):
    # Desactivamos la generación de videos en reversa para evitar errores de memoria
    # con diapositivas muy largas o que contienen videos (VideoMobject).
    skip_reversing = True

    def construct(self):
        Portada.construct(self)
        Introduccion.construct(self)
        Antecedentes.construct(self)
        Metodologia.construct(self)
        Resultados.construct(self)
        Conclusiones.construct(self)
        BiblyAgradecimientos.construct(self)