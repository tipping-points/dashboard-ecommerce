# E-commerce Analytics Dashboard

Dashboard interactivo de análisis de e-commerce desarrollado para **Nuclio Digital School**.

## Herramientas Incluidas

| Herramienta | Puerto | Descripción |
|-------------|--------|-------------|
| **Streamlit** | 8501 | Dashboard interactivo con KPIs y visualizaciones |
| **Metabase** | 3000 | Herramienta de BI para exploración de datos |
| **PostgreSQL** | 5432 | Base de datos con el dataset de Olist |

## Requisitos

- Docker Desktop instalado y corriendo
- Git

## Despliegue Rápido

```bash
git clone https://github.com/tipping-points/dashboard-ecommerce.git
cd dashboard-ecommerce
docker-compose up -d --build
```

## Acceso a las Herramientas

### Streamlit Dashboard
```
http://localhost:8501
```
Dashboard listo para usar con visualizaciones de KPIs.

### Metabase
```
http://localhost:3000
```

**Configuración inicial de Metabase:**
1. Abrir http://localhost:3000
2. Crear cuenta de administrador
3. Conectar a la base de datos:
   - Tipo: **PostgreSQL**
   - Host: **postgres**
   - Puerto: **5432**
   - Base de datos: **ecommerce**
   - Usuario: **nuclio**
   - Contraseña: **nuclio123**
4. Explorar la tabla `ventas` con todos los datos

### PostgreSQL (conexión directa)
```
Host: localhost
Puerto: 5432
Base de datos: ecommerce
Usuario: nuclio
Contraseña: nuclio123
```

## Estructura del Proyecto

```
dashboard-ecommerce/
├── app/
│   ├── .streamlit/config.toml
│   ├── data/olist_dashboard_dataset.csv
│   └── main.py
├── init-db/
│   ├── 01-init.sql
│   ├── 02-load-data.sh
│   └── data.csv
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Comandos Útiles

**Iniciar todo:**
```bash
docker-compose up -d --build
```

**Ver logs:**
```bash
docker-compose logs -f
```

**Parar todo:**
```bash
docker-compose down
```

**Reiniciar con datos limpios:**
```bash
docker-compose down -v
docker-compose up -d --build
```

## Dataset

El dataset proviene de **Olist**, plataforma de e-commerce brasileña.

**Tabla `ventas`:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| order_id | VARCHAR | ID único de la orden |
| customer_id | VARCHAR | ID del cliente |
| fecha | DATE | Fecha de la compra |
| ano | INTEGER | Año |
| mes | INTEGER | Mes (1-12) |
| estado | VARCHAR | Estado de Brasil (SP, RJ, etc.) |
| categoria | VARCHAR | Categoría del producto |
| precio | DECIMAL | Precio del producto |
| dias_entrega | DECIMAL | Días hasta la entrega |
| rating | INTEGER | Calificación (1-5) |
| metodo_pago | VARCHAR | Forma de pago |

## Licencia

Proyecto educativo para Nuclio Digital School.
