# E-commerce Analytics Dashboard

Dashboard interactivo de análisis de e-commerce desarrollado para **Nuclio Digital School**.

## Descripción

Este dashboard educativo demuestra:
- Visiones por stakeholder (CEO, CMO, COO)
- Árbol de KPIs interactivo
- Fichas Técnicas de cada KPI (10 componentes)
- Dashboard Personas para cada stakeholder
- Análisis del dataset Olist de e-commerce brasileño

## Requisitos

- Docker
- Docker Compose

## Despliegue Rápido

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd ecommerce-dashboard
```

2. Construir y ejecutar:
```bash
docker-compose up -d --build
```

3. Abrir en el navegador:
```
http://localhost:8501
```

## Estructura del Proyecto

```
ecommerce-dashboard/
├── app/
│   ├── .streamlit/
│   │   └── config.toml      # Configuración de tema
│   ├── data/
│   │   └── olist_dashboard_dataset.csv
│   └── main.py              # Aplicación principal
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Tecnologías

- **Streamlit**: Framework de dashboard
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **Docker**: Containerización

## Framework Educativo

### Árbol de KPIs
- North Star Metric (GMV)
- Objetivos estratégicos
- Estrategias
- Tácticas
- KPIs operacionales

### Dashboard Personas
Cada stakeholder tiene un perfil definido con:
- Objetivos
- Pain Points
- Necesidades del Dashboard
- KPIs principales

### Ficha Técnica de KPI
Cada KPI incluye 10 componentes:
1. Nombre del Indicador
2. Definición de Negocio
3. Objetivo (Target)
4. Frecuencia de Medición
5. Fuente de Datos
6. Fórmula Matemática
7. Unidad de Medida
8. Responsable
9. Tipo de KPI
10. Relación con NSM

## Colores Nuclio

- Amarillo: `#FFC630`
- Negro: `#141414`
- Blanco: `#FFFFFF`

## Licencia

Proyecto educativo para Nuclio Digital School.
