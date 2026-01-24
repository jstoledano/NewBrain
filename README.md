# New Brain

**New Brain** es una plataforma backend modular para la **gestión, consulta y
explotación de información institucional**, orientada a **soportar la operación,
la toma de decisiones y la mejora continua** en el ámbito electoral y
organizacional.

El sistema está diseñado para **resolver ambigüedad**, **centralizar significado**
y **habilitar decisiones informadas**, no solo para almacenar datos.

---

## Propósito

New Brain existe para proporcionar un **lugar confiable donde el significado
de la información esté resuelto**, de forma
que:

- personas no expertas puedan consultar información correcta,
- equipos operativos puedan tomar decisiones sin reinterpretar datos,
- la organización pueda demostrar cumplimiento, consistencia y mejora,
- distintos tipos de información puedan convivir sin contaminarse.

El foco no está en un tipo de dato, sino en la **función institucional de
la información**.

---

## Principios de diseño

- **Dominio primero**: el significado precede a la tecnología.
- **Monolito modular**: un solo sistema, múltiples dominios bien delimitados.
- **Bounded contexts explícitos**: cada dominio tiene su propio lenguaje e invariantes.
- **Datos inmutables cuando aplica**: cartografía, snapshots y resultados no se reescriben.
- **Consulta segura**: el sistema existe para ser consultado con confianza.
- **Infraestructura como detalle**: bases de datos, contenedores y frameworks no definen el dominio.

El sistema evita deliberadamente:

- microservicios prematuros,
- event sourcing artificial,
- complejidad ceremonial sin presión real.

---

## Qué tipo de sistema es

New Brain **no es**:

- un visor cartográfico aislado,
- un sistema de reportes genérico,
- un repositorio documental pasivo,
- un sistema transaccional operativo.

New Brain **sí es**:

- un **sistema de información institucional**,
- una **fuente de consulta confiable**,
- un **soporte para decisiones basadas en datos**,
- un **marco común para dominios distintos pero relacionados**.

---

## Arquitectura general

- **Lenguaje**: Python
- **Framework API**: FastAPI (REST)
- **Persistencia**: PostgreSQL / PostGIS (cuando aplica)
- **Contenedores**: Podman / Docker
- **CI/CD**: GitHub Actions
- **Layout**: `src/` con empaquetado explícito

El backend se implementa como un **monolito modular**, con un solo proceso y despliegue, pero con **límites de dominio
estrictos en código**.

---

## Bounded contexts (dominios)

New Brain está compuesto por múltiples dominios independientes, cada uno con un propósito claro:

### Marco Geográfico Electoral (MGE)

Registro normativo de información geoelectoral.

- Elimina ambigüedad territorial.
- Define pertenencia y relaciones entre secciones, municipios y distritos.
- Habilita vistas como el *Expediente Sección*.
- Sirve como base de agregación para información estadística e histórica.

### DOCS (Información documentada)

Gestión y control de información institucional documentada  
(alineado con ISO 9001:2015, 7.5 / 7.5.3).

### KPI

Seguimiento, medición y análisis de indicadores  
(alineado con ISO 9001:2015, 9.1).

### VOZMAC

Medición perceptual (encuestas tipo Likert) como insumo analítico  
(alineado con ISO 9001:2015, 9.1).

### PAS

Gestión de no conformidades y acciones correctivas  
(alineado con ISO 9001:2015, 10.2).

### IDEAS

Canal estructurado de sugerencias y oportunidades de mejora.

Cada dominio:

- tiene su propio modelo,
- no importa entidades internas de otros dominios,
- se comunica mediante contratos explícitos.

---

## Organización del repositorio

```shell
src /
└── newbrain /
├── mge /
│ ├── domain /
│ ├── application /
│ └── adapters /
├── shared /
└── main.py

infra /
scripts /
tests /
```

- `domain`: modelo puro (entidades, invariantes, lenguaje).
- `application`: orquestación de casos de uso (principalmente consulta).
- `adapters`: infraestructura (API, persistencia, integración).
- `infra/` y `scripts/` no forman parte del dominio importable.

---

## Estado del proyecto

New Brain se encuentra en **fase activa de diseño e implementación**.

Prioridades actuales:

- Definición y estabilización de modelos de dominio.
- Implementación progresiva del MGE como dominio fundacional.
- Construcción de capacidades de consulta seguras y agregables.

El frontend no forma parte de este repositorio.

---

## Filosofía de evolución

New Brain está diseñado para **crecer por adición de dominios**, no por reescritura.

- Si el lenguaje cambia, se crea un nuevo dominio.
- Si el significado se vuelve ambiguo, se refina el modelo.
- Si un dominio madura, puede separarse en el futuro.

Nada aquí está pensado como desechable.

---

## Licencia

Pendiente de definir.
