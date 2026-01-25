from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Literal

from ..entities.ProcesoElectoral import ProcesoElectoral
from ..entities.EntidadFederativa import EntidadFederativa
from ..entities.DistritoElectoralFederal import DistritoElectoralFederal
from ..entities.DistritoElectoralLocal import DistritoElectoralLocal
from ..entities.Municipio import Municipio
from ..entities.SeccionElectoral import SeccionElectoral
from ..entities.LimiteLocalidad import LimiteLocalidad
from ..entities.LocalidadPuntual import LocalidadPuntual
from ..entities.Manzana import Manzana


NivelGeoElectoral = Literal[
    "entidad",
    "distrito_electoral_federal",
    "distrito_electoral_local",
    "municipio",
    "seccion",
]


class InconsistenciaExpedienteMGE(Exception):
    """Excepción de dominio para inconsistencias dentro del expediente MGE."""


@dataclass
class ExpedienteMGE:
    """
    Agregado raíz del Marco Geográfico Electoral (MGE).

    Un ExpedienteMGE es un clúster de objetos de dominio asociados
    que se tratan como una unidad conceptual única para efectos de
    interpretación, presentación y uso institucional del MGE.

    Invariantes:
    - Coherencia semántica: todos los objetos pertenecen al mismo proceso electoral y entidad.
    - Nivel geoelectoral único: entidad, distrito (federal/local), municipio o sección.
    - No mezcla de significados: el contenido corresponde solo al nivel declarado.
    """

    proceso: ProcesoElectoral
    entidad: EntidadFederativa
    nivel: NivelGeoElectoral

    # Colecciones (opcionales según el uso del expediente)
    distritos_federales: List[DistritoElectoralFederal] = field(default_factory=list)
    distritos_locales: List[DistritoElectoralLocal] = field(default_factory=list)
    municipios: List[Municipio] = field(default_factory=list)
    secciones: List[SeccionElectoral] = field(default_factory=list)
    limites_localidad: List[LimiteLocalidad] = field(default_factory=list)
    localidades_puntuales: List[LocalidadPuntual] = field(default_factory=list)
    manzanas: List[Manzana] = field(default_factory=list)

    @property
    def id(self) -> str:
        """Identidad compuesta del expediente basada en proceso, entidad y nivel."""
        return f"{self.proceso.id}:{self.entidad.entidad:02d}:{self.nivel}"

    # Fábrica estática para asegurar validaciones de dominio al construir el agregado
    @staticmethod
    def crear(
        *,
        proceso: ProcesoElectoral,
        entidad: EntidadFederativa,
        nivel: NivelGeoElectoral,
        distritos_federales: Optional[List[DistritoElectoralFederal]] = None,
        distritos_locales: Optional[List[DistritoElectoralLocal]] = None,
        municipios: Optional[List[Municipio]] = None,
        secciones: Optional[List[SeccionElectoral]] = None,
        limites_localidad: Optional[List[LimiteLocalidad]] = None,
        localidades_puntuales: Optional[List[LocalidadPuntual]] = None,
        manzanas: Optional[List[Manzana]] = None,
    ) -> "ExpedienteMGE":
        expediente = ExpedienteMGE(
            proceso=proceso,
            entidad=entidad,
            nivel=nivel,
            distritos_federales=list(distritos_federales or []),
            distritos_locales=list(distritos_locales or []),
            municipios=list(municipios or []),
            secciones=list(secciones or []),
            limites_localidad=list(limites_localidad or []),
            localidades_puntuales=list(localidades_puntuales or []),
            manzanas=list(manzanas or []),
        )
        expediente._validar_coherencia()
        expediente._validar_nivel_geoelectoral()
        return expediente

    def descripcion(self) -> str:
        """Resumen humano-legible del expediente."""
        return (
            f"Expediente MGE [{self.id}] — {self.proceso} / {self.entidad}. "
            f"Nivel: {self.nivel}. "
            f"DF: {len(self.distritos_federales)}, DL: {len(self.distritos_locales)}, "
            f"Mun: {len(self.municipios)}, Sec: {len(self.secciones)}, "
            f"Loc: {len(self.limites_localidad) + len(self.localidades_puntuales)}, "
            f"Manzanas: {len(self.manzanas)}"
        )

    # --- Validaciones internas del agregado ---
    def _validar_coherencia(self) -> None:
        """
        Garantiza que todos los objetos pertenecen al mismo proceso y entidad.
        """
        proc_id = self.proceso.id
        ent_id = self.entidad.entidad

        def check(obj_name: str, obj_list: List[object], get_proc, get_ent) -> None:
            for o in obj_list:
                if get_proc(o) != proc_id:
                    raise InconsistenciaExpedienteMGE(
                        f"{obj_name} con proceso_electoral_id={get_proc(o)} no coincide con {proc_id}"
                    )
                if get_ent(o) != ent_id:
                    raise InconsistenciaExpedienteMGE(
                        f"{obj_name} con entidad_id={get_ent(o)} no coincide con {ent_id}"
                    )

        check(
            "DistritoElectoralFederal",
            self.distritos_federales,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "DistritoElectoralLocal",
            self.distritos_locales,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "Municipio", self.municipios, lambda x: x.proceso_electoral_id, lambda x: x.entidad_id
        )
        check(
            "SeccionElectoral",
            self.secciones,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "LimiteLocalidad",
            self.limites_localidad,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        # LocalidadPuntual tiene nombres de campos ligeramente distintos (entidad_int, municipio_int)
        for lp in self.localidades_puntuales:
            if lp.proceso_electoral_id != proc_id:
                raise InconsistenciaExpedienteMGE(
                    f"LocalidadPuntual con proceso_electoral_id={lp.proceso_electoral_id} no coincide con {proc_id}"
                )
            if getattr(lp, "entidad_int", None) != ent_id:
                raise InconsistenciaExpedienteMGE(
                    f"LocalidadPuntual con entidad_int={getattr(lp, 'entidad_int', None)} no coincide con {ent_id}"
                )

        check("Manzana", self.manzanas, lambda x: x.proceso_electoral_id, lambda x: x.entidad_id)

    def _validar_nivel_geoelectoral(self) -> None:
        """
        Garantiza que el contenido corresponde al nivel declarado.

                Reglas generales:
                - Fuera del nivel sección y entidad, no puede coexistir información de distrito federal y local.
                - El expediente puede incluir niveles inferiores solo como contexto, nunca cambia el punto de lectura.
                - No valida geometría, solo coherencia relacional del punto de lectura.

                Reglas por nivel:
                - entidad: nivel máximo de agregación; puede contener catálogos de DF, DL, municipios y secciones simultáneamente
                    sin interpretarlos como intersecciones, solo como panorama completo de la entidad.
                - distrito_electoral_federal: requiere exactamente un DF; no admite DL; secciones (si hay) adscritas al DF;
                    no admite municipios como foco.
                - distrito_electoral_local: requiere exactamente un DL; no admite DF; secciones adscritas al DL; no admite
                    municipios como foco.
                - municipio: requiere exactamente un municipio; no admite DF/DL; secciones/localidades/manzanas deben pertenecer
                    al municipio declarado; municipio no es punto de intersección DF/DL.
                - seccion: requiere exactamente una sección; único nivel que permite coexistir DF y DL, ambos deben coincidir con
                    la sección; municipio, si se incluye, debe coincidir; localidades/manzanas deben corresponder a la sección.
        """

        # Regla estructural clave: fuera de sección y entidad no pueden coexistir DF y DL
        if (
            self.nivel not in {"seccion", "entidad"}
            and self.distritos_federales
            and self.distritos_locales
        ):
            raise InconsistenciaExpedienteMGE(
                "No se permite coexistencia de distrito federal y local fuera del nivel sección"
            )

        if self.nivel == "entidad":
            return

        if self.nivel == "distrito_electoral_federal":
            if len(self.distritos_federales) != 1:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_federal requiere exactamente un DF"
                )
            if self.distritos_locales:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_federal no admite distritos locales"
                )
            if self.municipios:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_federal no admite municipios como foco"
                )

            distrito_id = self.distritos_federales[0].id
            if any(sec.distrito_electoral_federal_id != distrito_id for sec in self.secciones):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del distrito federal declarado en el expediente"
                )
            return

        if self.nivel == "distrito_electoral_local":
            if len(self.distritos_locales) != 1:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_local requiere exactamente un DL"
                )
            if self.distritos_federales:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_local no admite distritos federales"
                )
            if self.municipios:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito_electoral_local no admite municipios como foco"
                )

            distrito_id = self.distritos_locales[0].id
            if any(sec.distrito_electoral_local_id != distrito_id for sec in self.secciones):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del distrito local declarado en el expediente"
                )
            return

        if self.nivel == "municipio":
            if len(self.municipios) != 1:
                raise InconsistenciaExpedienteMGE(
                    "Nivel municipio requiere exactamente un municipio"
                )
            if self.distritos_federales or self.distritos_locales:
                raise InconsistenciaExpedienteMGE("Nivel municipio no debe incluir distritos")

            municipio_id = self.municipios[0].municipio_id

            if any(sec.municipio_id != municipio_id for sec in self.secciones):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del municipio declarado en el expediente"
                )
            if any(ll.municipio_id != municipio_id for ll in self.limites_localidad):
                raise InconsistenciaExpedienteMGE(
                    "Localidad fuera del municipio declarado en el expediente"
                )
            if any(lp.municipio_int != municipio_id for lp in self.localidades_puntuales):
                raise InconsistenciaExpedienteMGE(
                    "Localidad puntual fuera del municipio declarado en el expediente"
                )
            if any(mz.municipio_id != municipio_id for mz in self.manzanas):
                raise InconsistenciaExpedienteMGE(
                    "Manzana fuera del municipio declarado en el expediente"
                )
            return

        if self.nivel == "seccion":
            if len(self.secciones) != 1:
                raise InconsistenciaExpedienteMGE("Nivel sección requiere exactamente una sección")
            seccion = self.secciones[0]

            if self.distritos_federales and any(
                df.id != seccion.distrito_electoral_federal_id for df in self.distritos_federales
            ):
                raise InconsistenciaExpedienteMGE(
                    "Distrito federal no coincide con la sección declarada"
                )
            if self.distritos_locales and any(
                dl.id != seccion.distrito_electoral_local_id for dl in self.distritos_locales
            ):
                raise InconsistenciaExpedienteMGE(
                    "Distrito local no coincide con la sección declarada"
                )

            if self.municipios:
                if (
                    len(self.municipios) != 1
                    or self.municipios[0].municipio_id != seccion.municipio_id
                ):
                    raise InconsistenciaExpedienteMGE(
                        "Municipio proporcionado no coincide con la sección declarada"
                    )

            seccion_ids_permitidos = {seccion.id, seccion.seccion}
            if any(mz.seccion_id not in seccion_ids_permitidos for mz in self.manzanas):
                raise InconsistenciaExpedienteMGE(
                    "Manzana fuera de la sección declarada en el expediente"
                )
