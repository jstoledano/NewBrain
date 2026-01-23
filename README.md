# New Brain

New Brain es un backend modular orientado a **información normativa, territorial y electoral**.  
Su objetivo es servir como **fuente de verdad estructural**, estable y auditable, para sistemas de consulta, análisis y apoyo a la toma de decisiones relacionadas con la función electoral.

El sistema está diseñado como un **modular monolith**, con bounded contexts explícitos, dominio primero y persistencia como detalle de infraestructura.

---

## Principios de diseño

- Dominio primero: el significado no depende del esquema de base de datos.
- Bounded contexts explícitos y protegidos en código.
- Datos normativos e inmutables por proceso electoral.
- Read-only por defecto para consumidores externos.
- GIS pesado fuera del runtime (resuelto en ingestión).
- Infraestructura simple, reproducible y defendible.

Este proyecto **no** persigue:

- microservicios prematuros,
- event sourcing artificial,
- DDD ceremonial,
- abstracciones sin presión real.

---

## Arquitectura general

- **API**: FastAPI (REST)
- **Lenguaje**: Python
- **Persistencia**: PostgreSQL + PostGIS
- **Contenedores**: Docker + docker-compose
- **CI/CD**: GitHub Actions
- **Formato de intercambio**: JSON / GeoJSON (en bordes)

El backend expone APIs de consulta sobre datos previamente validados y materializados.

---

## Bounded Contexts (backend)

### Marco Geográfico Electoral (MGE)

Contexto fundacional del sistema.

Responsabilidades:

- Modelar la cartografía electoral y judicial aprobada para un proceso electoral.
- Proveer identidad y pertenencia territorial (entidad, municipio, distrito, sección, manzana).
- Servir como base para agregación estadística y referencia territorial.

Características clave:

- Snapshot normativo por proceso electoral.
- Inmutable una vez aprobado.
- Read-only para cualquier consumidor.
- Geometría compleja resuelta en ingestión, no en runtime.

Otros bounded contexts se incorporarán sobre esta base (resultados electorales, organización, etc.), siempre como consumidores del MGE.

---

## Pipeline de ingestión (BGED)

New Brain no modifica ni corrige la cartografía fuente.

La **Base Geográfica Electoral Digital (BGED)** es tratada como *source of truth*.  
Un pipeline offline se encarga de:

1. Leer capas geográficas (preferentemente GeoPackage).
2. Validar geometría y topología básica.
3. Resolver relaciones espaciales costosas (ej. manzana → localidad).
4. Materializar datos finales en PostgreSQL/PostGIS.
5. Marcar el MGE como aprobado para un `proceso_electoral_id`.

Una vez ingeridos:

- el sistema solo consulta,
- no hay joins espaciales en tiempo de ejecución,
- no hay mutaciones del MGE.

---

## Estructura del repositorio

```bash
app/
├── mge/ # Bounded Context: Marco Geográfico Electoral
│ ├── domain/ # Modelo de dominio puro (sin ORM)
│ ├── application/ # Casos de uso (consultas)
│ └── adapters/ # Persistencia, API, infraestructura
├── shared/ # Configuración, logging, utilidades comunes
└── main.py # Inicialización FastAPI

infra/
├── docker/
│ └── docker-compose.yml
└── db/
└── migrations/

scripts/
└── ingest/ # Pipeline de ingestión BGED

tests/
```


Reglas importantes:

- El dominio no importa detalles de infraestructura.
- Los bounded contexts no se importan entre sí sin contratos explícitos.
- El pipeline no vive en la API.

---

## Entorno de desarrollo

### Requisitos

- Python (gestionado con pyenv)
- Docker + docker-compose
- Git

### Flujo recomendado

- Python local para desarrollo y tooling.
- PostgreSQL/PostGIS en contenedor Docker.
- FastAPI ejecutándose localmente o en contenedor (configurable).

---

## Estado del proyecto

New Brain está en **fase inicial activa**.

Prioridades actuales:

- Definición del modelo de dominio MGE.
- Pipeline de ingestión BGED (caso Tlaxcala).
- Modelo lógico mínimo y DDL.
- API de consulta read-only.

El frontend no forma parte de este repositorio.

---

## Alcance y límites

Este backend:

- No gestiona procesos electorales.
- No calcula resultados en tiempo real.
- No reemplaza sistemas oficiales.
- No expone datos mutables sin control normativo.

Su valor está en **estabilidad semántica, trazabilidad y claridad estructural**.

---

## Licencia

Pendiente de definir.
