import pytest
from abril.core import mi_funcion


def test_mi_funcion():
    assert mi_funcion() == "¡Hola desde Abril!"
