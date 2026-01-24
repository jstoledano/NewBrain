import pytest
from datetime import date

from newbrain.mge.domain.entities.ProcesoElectoral import ProcesoElectoral
from newbrain.mge.domain.entities.EntidadFederativa import EntidadFederativa
from newbrain.mge.domain.entities.DistritoElectoralFederal import DistritoElectoralFederal
from newbrain.mge.domain.entities.DistritoElectoralLocal import DistritoElectoralLocal
from newbrain.mge.domain.entities.Municipio import Municipio
from newbrain.mge.domain.entities.SeccionElectoral import SeccionElectoral
from newbrain.mge.domain.entities.Manzana import Manzana
from newbrain.mge.domain.aggregates import ExpedienteMGE, InconsistenciaExpedienteMGE


def sample_proceso():
    return ProcesoElectoral(
        id="2024",
        nombre_corto="PE2024",
        nombre_oficial="Proceso Electoral 2024",
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=date(2024, 12, 31),
    )


def sample_entidad():
    return EntidadFederativa(
        entidad=30,
        nombre_entidad="VERACRUZ DE IGNACIO DE LA LLAVE",
        nombre_corto="Veracruz",
        nombre_clave="VR",
        nombre_abrev="VER",
    )


def test_crear_expediente_entidad_valido():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=1,
        proceso_electoral_id=2024,  # int, debe coincidir con str "2024"
        entidad_id=ent.entidad,
        distrito=1,
        nombre_cabecera="Xalapa",
    )
    cdl = DistritoElectoralLocal(
        id=10,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_local=10,
        nombre_cabecera="Xalapa",
    )
    mun = Municipio(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        municipio_id=1,
        nombre_municipio="Xalapa",
        nombre_cabecera="Xalapa",
    )
    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=cdf.id,
        distrito_electoral_local_id=cdl.id,
        municipio_id=mun.municipio_id,
        seccion=1234,
    )

    exp = ExpedienteMGE.crear(
        proceso=proc,
        entidad=ent,
        nivel="entidad",
        distritos_federales=[cdf],
        distritos_locales=[cdl],
        municipios=[mun],
        secciones=[sec],
    )

    assert exp.nivel == "entidad"
    assert exp.entidad.entidad == ent.entidad
    assert exp.proceso.id == proc.id
    assert len(exp.distritos_federales) == 1
    assert len(exp.distritos_locales) == 1


def test_inconsistencia_proceso_en_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    mun_invalido = Municipio(
        id=2,
        proceso_electoral_id="2025",  # no coincide con 2024
        entidad_id=ent.entidad,
        municipio_id=2,
        nombre_municipio="Coatepec",
        nombre_cabecera="Coatepec",
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="entidad",
            municipios=[mun_invalido],
        )


def test_nivel_distrito_no_admite_mezcla_federal_local():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=3,
        proceso_electoral_id=2024,
        entidad_id=ent.entidad,
        distrito=2,
        nombre_cabecera="Veracruz",
    )

    cdl = DistritoElectoralLocal(
        id=5,
        proceso_electoral_id=2024,
        entidad_id=ent.entidad,
        distrito_local=10,
        nombre_cabecera="Xalapa",
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito",
            distritos_federales=[cdf],
            distritos_locales=[cdl],
        )


def test_nivel_distrito_seccion_debe_pertenecer():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=2,
        proceso_electoral_id=2024,
        entidad_id=ent.entidad,
        distrito=2,
        nombre_cabecera="Veracruz",
    )

    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=999,  # no coincide
        distrito_electoral_local_id=0,
        municipio_id=1,
        seccion=1234,
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito",
            distritos_federales=[cdf],
            secciones=[sec],
        )


def test_nivel_municipio_requiere_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="municipio",
        )


def test_nivel_municipio_seccion_fuera_de_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    mun = Municipio(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        municipio_id=1,
        nombre_municipio="Xalapa",
        nombre_cabecera="Xalapa",
    )

    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=1,
        distrito_electoral_local_id=1,
        municipio_id=99,  # municipio distinto
        seccion=1234,
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="municipio",
            municipios=[mun],
            secciones=[sec],
        )


def test_nivel_seccion_requiere_una_seccion():
    proc = sample_proceso()
    ent = sample_entidad()

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="seccion",
            secciones=[],
        )

    seccion = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=1,
        distrito_electoral_local_id=1,
        municipio_id=1,
        seccion=1234,
    )
    manzana = Manzana(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        municipio_id=1,
        localidad_id=1,
        seccion_id=9999,  # no coincide con seccion.seccion
        manzana=1,
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="seccion",
            secciones=[seccion],
            manzanas=[manzana],
        )
