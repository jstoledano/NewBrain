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
        proceso_electoral_id="2024",
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


def test_entidad_permite_df_y_dl_como_catalogo():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=20,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=20,
        nombre_cabecera="Veracruz",
    )
    cdl = DistritoElectoralLocal(
        id=21,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=21,
        nombre_cabecera="Xalapa",
    )
    mun = Municipio(
        id=2,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        municipio_id=2,
        nombre_municipio="Coatepec",
        nombre_cabecera="Coatepec",
    )
    sec = SeccionElectoral(
        id=2,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=cdf.id,
        distrito_electoral_local_id=cdl.id,
        municipio_id=mun.municipio_id,
        seccion=5678,
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
    assert len(exp.distritos_federales) == 1
    assert len(exp.distritos_locales) == 1
    assert len(exp.municipios) == 1
    assert len(exp.secciones) == 1


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


def test_municipio_no_admite_coexistencia_df_dl():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=3,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=2,
        nombre_cabecera="Veracruz",
    )

    cdl = DistritoElectoralLocal(
        id=5,
        proceso_electoral_id="2024",
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

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="municipio",
            distritos_federales=[cdf],
            distritos_locales=[cdl],
            municipios=[mun],
        )


def test_nivel_distrito_federal_valido_y_seccion_adscrita():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=2,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=2,
        nombre_cabecera="Veracruz",
    )

    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=cdf.id,
        distrito_electoral_local_id=0,
        municipio_id=1,
        seccion=1234,
    )

    exp = ExpedienteMGE.crear(
        proceso=proc,
        entidad=ent,
        nivel="distrito_electoral_federal",
        distritos_federales=[cdf],
        secciones=[sec],
    )

    assert exp.nivel == "distrito_electoral_federal"
    assert len(exp.distritos_federales) == 1
    assert len(exp.distritos_locales) == 0


def test_nivel_distrito_federal_no_admite_del():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=3,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=3,
        nombre_cabecera="Veracruz",
    )
    cdl = DistritoElectoralLocal(
        id=8,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=8,
        nombre_cabecera="Xalapa",
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito_electoral_federal",
            distritos_federales=[cdf],
            distritos_locales=[cdl],
        )


def test_nivel_distrito_federal_no_admite_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=10,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=10,
        nombre_cabecera="Veracruz",
    )

    mun = Municipio(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        municipio_id=1,
        nombre_municipio="Xalapa",
        nombre_cabecera="Xalapa",
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito_electoral_federal",
            distritos_federales=[cdf],
            municipios=[mun],
        )


def test_nivel_distrito_federal_seccion_fuera():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=4,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=4,
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
            nivel="distrito_electoral_federal",
            distritos_federales=[cdf],
            secciones=[sec],
        )


def test_nivel_distrito_local_valido():
    proc = sample_proceso()
    ent = sample_entidad()

    cdl = DistritoElectoralLocal(
        id=5,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=5,
        nombre_cabecera="Xalapa",
    )

    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=0,
        distrito_electoral_local_id=cdl.id,
        municipio_id=1,
        seccion=1234,
    )

    exp = ExpedienteMGE.crear(
        proceso=proc,
        entidad=ent,
        nivel="distrito_electoral_local",
        distritos_locales=[cdl],
        secciones=[sec],
    )

    assert exp.nivel == "distrito_electoral_local"
    assert len(exp.distritos_locales) == 1
    assert len(exp.distritos_federales) == 0


def test_nivel_distrito_local_no_admite_df():
    proc = sample_proceso()
    ent = sample_entidad()

    cdl = DistritoElectoralLocal(
        id=7,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=7,
        nombre_cabecera="Xalapa",
    )
    cdf = DistritoElectoralFederal(
        id=9,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=9,
        nombre_cabecera="Veracruz",
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito_electoral_local",
            distritos_locales=[cdl],
            distritos_federales=[cdf],
        )


def test_nivel_distrito_local_no_admite_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    cdl = DistritoElectoralLocal(
        id=11,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=11,
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

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito_electoral_local",
            distritos_locales=[cdl],
            municipios=[mun],
        )


def test_nivel_distrito_local_seccion_fuera():
    proc = sample_proceso()
    ent = sample_entidad()

    cdl = DistritoElectoralLocal(
        id=6,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=6,
        nombre_cabecera="Xalapa",
    )

    sec = SeccionElectoral(
        id=1,
        proceso_electoral_id=proc.id,
        entidad_id=ent.entidad,
        distrito_electoral_federal_id=0,
        distrito_electoral_local_id=999,  # no coincide
        municipio_id=1,
        seccion=1234,
    )

    with pytest.raises(InconsistenciaExpedienteMGE):
        ExpedienteMGE.crear(
            proceso=proc,
            entidad=ent,
            nivel="distrito_electoral_local",
            distritos_locales=[cdl],
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


def test_nivel_seccion_valido_con_df_dl_municipio():
    proc = sample_proceso()
    ent = sample_entidad()

    cdf = DistritoElectoralFederal(
        id=11,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito=11,
        nombre_cabecera="Xalapa",
    )
    cdl = DistritoElectoralLocal(
        id=12,
        proceso_electoral_id="2024",
        entidad_id=ent.entidad,
        distrito_local=12,
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
    seccion = SeccionElectoral(
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
        nivel="seccion",
        distritos_federales=[cdf],
        distritos_locales=[cdl],
        municipios=[mun],
        secciones=[seccion],
    )

    assert exp.nivel == "seccion"
    assert len(exp.secciones) == 1
    assert len(exp.distritos_federales) == 1
    assert len(exp.distritos_locales) == 1
