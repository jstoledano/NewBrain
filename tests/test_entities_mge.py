import pytest
from dataclasses import FrozenInstanceError
from datetime import date

from newbrain.mge.domain.entities.EntidadFederativa import EntidadFederativa
from newbrain.mge.domain.entities.Municipio import Municipio
from newbrain.mge.domain.entities.SeccionElectoral import SeccionElectoral
from newbrain.mge.domain.entities.DistritoElectoralFederal import DistritoElectoralFederal
from newbrain.mge.domain.entities.DistritoElectoralLocal import DistritoElectoralLocal
from newbrain.mge.domain.entities.ProcesoElectoral import ProcesoElectoral
from newbrain.mge.domain.entities.LimiteLocalidad import LimiteLocalidad
from newbrain.mge.domain.entities.LocalidadPuntual import LocalidadPuntual
from newbrain.mge.domain.entities.Manzana import Manzana


def test_entidad_federativa_str_y_frozen():
    ef = EntidadFederativa(
        entidad=30,
        nombre_entidad="VERACRUZ DE IGNACIO DE LA LLAVE",
        nombre_corto="Veracruz",
        nombre_clave="VR",
        nombre_abrev="VER",
    )
    assert str(ef) == "30 VERACRUZ"
    with pytest.raises(FrozenInstanceError):
        ef.nombre_corto = "Otro"


def test_municipio_str_y_frozen():
    m = Municipio(
        id=1,
        proceso_electoral_id="2024",
        entidad_id=30,
        municipio_id=7,
        nombre_municipio="Coatepec",
        nombre_cabecera="Coatepec",
    )
    assert str(m) == "007 COATEPEC"
    with pytest.raises(FrozenInstanceError):
        m.nombre_municipio = "Xalapa"


def test_seccion_electoral_str_y_frozen():
    s = SeccionElectoral(
        id=1,
        proceso_electoral_id="2024",
        entidad_id=30,
        distrito_electoral_federal_id=1,
        distrito_electoral_local_id=10,
        municipio_id=1,
        seccion=1234,
    )
    assert str(s) == "30 1234"
    with pytest.raises(FrozenInstanceError):
        s.seccion = 9999


def test_distrito_electoral_federal_str_y_frozen():
    d = DistritoElectoralFederal(
        id=1,
        proceso_electoral_id=2024,
        entidad_id=30,
        distrito=1,
        nombre_cabecera="Xalapa",
    )
    assert str(d) == "30 01"
    with pytest.raises(FrozenInstanceError):
        d.distrito = 2


def test_distrito_electoral_local_str_y_frozen():
    dl = DistritoElectoralLocal(
        id=10,
        proceso_electoral_id=2024,
        entidad_id=30,
        distrito_local=12,
        nombre_cabecera="Xalapa",
    )
    assert str(dl) == "30 12"
    with pytest.raises(FrozenInstanceError):
        dl.distrito_local = 13


def test_proceso_electoral_str_mismo_anio_y_contiene_fecha():
    pe = ProcesoElectoral(
        id="2024",
        nombre_corto="PE2024",
        nombre_oficial="Proceso Electoral 2024",
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=date(2024, 12, 31),
    )
    # str muestra nombre_corto en mayúsculas y (2024) al ser mismo año
    assert str(pe) == "PE2024 (2024)"
    assert pe.contiene_fecha(date(2024, 6, 1))
    assert pe.contiene_fecha(pe.fecha_inicio)
    assert pe.contiene_fecha(pe.fecha_fin)
    assert not pe.contiene_fecha(date(2025, 1, 1))


def test_proceso_electoral_str_distintos_anios():
    pe = ProcesoElectoral(
        id="2425",
        nombre_corto="PE",
        nombre_oficial="Proceso Electoral 2024-2025",
        fecha_inicio=date(2024, 11, 1),
        fecha_fin=date(2025, 2, 28),
    )
    # str muestra (24-25) al ser distinto año
    assert str(pe) == "PE (24-25)"


def test_limite_localidad_str_y_frozen():
    ll = LimiteLocalidad(
        id=1,
        proceso_electoral_id="2024",
        entidad_id=30,
        municipio_id=1,
        localidad_id=25,
        nombre_localidad="Las Trancas",
    )
    assert str(ll) == "0025 LAS TRANCAS"
    with pytest.raises(FrozenInstanceError):
        ll.localidad_id = 26


def test_localidad_puntual_str_y_frozen():
    lp = LocalidadPuntual(
        id=1,
        proceso_electoral_id="2024",
        entidad_int=30,
        municipio_int=1,
        localidad_id=9999,
        nombre_localidad="Punto",
    )
    assert str(lp) == "9999 PUNTO"
    with pytest.raises(FrozenInstanceError):
        lp.nombre_localidad = "Otro"


def test_manzana_str_y_frozen():
    mz = Manzana(
        id=1,
        proceso_electoral_id="2024",
        entidad_id=30,
        municipio_id=1,
        localidad_id=9999,
        seccion_id=1234,
        manzana=88,
    )
    assert str(mz) == "1234 9999 0088"
    with pytest.raises(FrozenInstanceError):
        mz.manzana = 1
