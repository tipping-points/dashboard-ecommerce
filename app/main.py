"""
Dashboard Interactivo de E-commerce - Nuclio Digital School
Ejemplo educativo para estudiantes de Data Visualization

Este dashboard muestra:
- Visiones por stakeholder (CEO, CMO, COO)
- Árbol de KPIs interactivo
- Fichas Técnicas de cada KPI
- Dashboard Personas para cada stakeholder
- KPIs del dataset Olist de e-commerce brasileño
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS NUCLIO
# =============================================================================
st.set_page_config(
    page_title="E-commerce Dashboard | Nuclio Digital School",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='40' fill='%23FFC630'/><circle cx='50' cy='50' r='15' fill='%23141414'/></svg>",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores Nuclio Digital School
NUCLIO_COLORS = {
    'yellow': '#FFC630',
    'black': '#141414',
    'white': '#FFFFFF',
    'gray_light': '#F5F5F5',
    'gray_text': '#666666',
    'gray_medium': '#969696',
    'blue_light': '#E8F4F8',
    'green_light': '#E8F5E9',
    'green': '#4CAF50',
    'green_dark': '#2E7D32',
    'purple': '#9C7CF4',
    'purple_light': '#B39DDB',
    'brown': '#8B4513',
    'red': '#E74C3C',
    'red_light': '#FFEBEE',
    'orange': '#FF9800',
    'blue': '#2196F3'
}

# =============================================================================
# DASHBOARD PERSONAS - Perfiles de Stakeholders
# =============================================================================
DASHBOARD_PERSONAS = {
    'CEO': {
        'nombre': 'Carlos Mendoza',
        'cargo': 'Chief Executive Officer (CEO)',
        'foto_emoji': '',
        'descripcion': 'Ejecutivo con 15 años de experiencia en retail y e-commerce. Responsable de la visión estratégica y el crecimiento sostenible del negocio.',
        'objetivos': [
            'Maximizar el valor del negocio (GMV)',
            'Asegurar crecimiento sostenible (+25% anual)',
            'Mantener satisfacción del cliente alta',
            'Tomar decisiones estratégicas basadas en datos'
        ],
        'pain_points': [
            'Falta de visión consolidada del negocio',
            'Dificultad para identificar tendencias a tiempo',
            'Información dispersa en múltiples reportes',
            'Necesita insights rápidos para reuniones de directorio'
        ],
        'necesidades_dashboard': [
            'KPIs de alto nivel en una sola vista',
            'Tendencias y comparativas temporales',
            'Alertas cuando hay desviaciones importantes',
            'Drill-down a regiones y categorías principales'
        ],
        'frecuencia_uso': 'Diaria (revisión rápida) / Semanal (análisis profundo)',
        'kpis_principales': ['GMV', 'Total Órdenes', 'AOV', 'Clientes Únicos', 'Rating General'],
        'color': NUCLIO_COLORS['yellow']
    },
    'CMO': {
        'nombre': 'María García',
        'cargo': 'Chief Marketing Officer (CMO)',
        'foto_emoji': '',
        'descripcion': 'Experta en marketing digital con enfoque en growth hacking y análisis de comportamiento del consumidor. Lidera las estrategias de adquisición y retención.',
        'objetivos': [
            'Optimizar el costo de adquisición de clientes (CAC)',
            'Incrementar la tasa de conversión',
            'Aumentar la recurrencia de clientes',
            'Maximizar el ROI de campañas de marketing'
        ],
        'pain_points': [
            'Dificultad para atribuir ventas a campañas específicas',
            'No saber qué categorías promocionar',
            'Entender patrones de comportamiento de compra',
            'Identificar segmentos de clientes más rentables'
        ],
        'necesidades_dashboard': [
            'Métricas de conversión y funnel de ventas',
            'Análisis de categorías y productos',
            'Patrones de compra por día/hora',
            'Segmentación geográfica y demográfica'
        ],
        'frecuencia_uso': 'Diaria (optimización de campañas) / Semanal (reportes)',
        'kpis_principales': ['AOV', 'Tasa Conversión', '% Clientes Recurrentes', 'CAC', 'Ventas por Categoría'],
        'color': NUCLIO_COLORS['purple']
    },
    'COO': {
        'nombre': 'Roberto Silva',
        'cargo': 'Chief Operations Officer (COO)',
        'foto_emoji': '',
        'descripcion': 'Ingeniero industrial con expertise en logística y optimización de procesos. Responsable de la eficiencia operacional y satisfacción del cliente.',
        'objetivos': [
            'Reducir tiempos de entrega a menos de 7 días',
            'Mantener rating de satisfacción >= 4.0',
            'Optimizar costos logísticos',
            'Mejorar la experiencia post-compra'
        ],
        'pain_points': [
            'Variabilidad en tiempos de entrega por región',
            'Identificar cuellos de botella operacionales',
            'Correlacionar entregas con satisfacción',
            'Gestionar vendedores con bajo desempeño'
        ],
        'necesidades_dashboard': [
            'Métricas de tiempo de entrega por estado',
            'Distribución de ratings y reviews',
            'Correlación entrega-satisfacción',
            'Alertas de SLAs incumplidos'
        ],
        'frecuencia_uso': 'Diaria (monitoreo operacional) / Semanal (mejora continua)',
        'kpis_principales': ['Tiempo Entrega', '% Entregas Rápidas', 'Rating', '% Satisfechos', 'Reviews Negativos'],
        'color': NUCLIO_COLORS['green']
    }
}

# =============================================================================
# FICHAS TÉCNICAS DE KPIs
# =============================================================================
KPI_FICHAS_TECNICAS = {
    'GMV': {
        'nombre': 'GMV (Gross Merchandise Value)',
        'definicion': 'Valor total bruto de todas las mercancías vendidas en la plataforma durante un período determinado. Es la métrica principal que refleja el volumen de negocio.',
        'objetivo': 'Maximizar - Crecimiento del 25% anual',
        'frecuencia': 'Diaria (monitoreo) / Semanal (análisis) / Mensual (reporte ejecutivo)',
        'fuente': 'Base de datos de órdenes - tabla orders + order_items',
        'formula': 'GMV = SUM(precio_producto) para todas las órdenes completadas',
        'unidad': 'R$ (Reales Brasileños)',
        'responsable': 'CEO / Director Comercial',
        'tipo': 'North Star Metric (Estratégico)',
        'relacion_nsm': 'ES la North Star Metric - Todas las demás métricas contribuyen a esta'
    },
    'AOV': {
        'nombre': 'AOV (Average Order Value)',
        'definicion': 'Valor promedio de cada orden realizada. Indica cuánto gasta en promedio cada cliente por transacción.',
        'objetivo': 'R$ 150 o superior',
        'frecuencia': 'Semanal (análisis) / Mensual (reporte)',
        'fuente': 'Base de datos de órdenes - tabla orders',
        'formula': 'AOV = GMV / Número Total de Órdenes',
        'unidad': 'R$ (Reales Brasileños)',
        'responsable': 'CMO / Director de Marketing',
        'tipo': 'KPI Estratégico',
        'relacion_nsm': 'Impacto directo: Aumentar AOV incrementa GMV sin necesidad de más clientes'
    },
    'Total_Ordenes': {
        'nombre': 'Total de Órdenes',
        'definicion': 'Número total de transacciones completadas exitosamente en la plataforma.',
        'objetivo': 'Crecimiento del 20% anual',
        'frecuencia': 'Diaria (monitoreo) / Semanal (análisis)',
        'fuente': 'Base de datos de órdenes - tabla orders (status = delivered)',
        'formula': 'Total Órdenes = COUNT(DISTINCT order_id) WHERE status = "delivered"',
        'unidad': 'Unidades (número de órdenes)',
        'responsable': 'CEO / Director Comercial',
        'tipo': 'KPI Estratégico',
        'relacion_nsm': 'Impacto directo: Más órdenes = Mayor GMV (GMV = Órdenes x AOV)'
    },
    'Total_Clientes': {
        'nombre': 'Total de Clientes Únicos',
        'definicion': 'Número de clientes diferentes que han realizado al menos una compra.',
        'objetivo': 'Crecimiento del 30% anual en nuevos clientes',
        'frecuencia': 'Semanal / Mensual',
        'fuente': 'Base de datos de clientes - tabla customers',
        'formula': 'Total Clientes = COUNT(DISTINCT customer_id)',
        'unidad': 'Unidades (número de clientes)',
        'responsable': 'CMO / Director de Adquisición',
        'tipo': 'KPI Estratégico',
        'relacion_nsm': 'Impacto indirecto: Más clientes potencialmente generan más órdenes y mayor GMV'
    },
    'CAC': {
        'nombre': 'CAC (Customer Acquisition Cost)',
        'definicion': 'Costo promedio de adquirir un nuevo cliente, incluyendo gastos de marketing y ventas.',
        'objetivo': '<= R$ 45 por cliente',
        'frecuencia': 'Mensual',
        'fuente': 'Sistema financiero + CRM - gastos marketing / nuevos clientes',
        'formula': 'CAC = (Gastos Marketing + Gastos Ventas) / Nuevos Clientes Adquiridos',
        'unidad': 'R$ (Reales Brasileños)',
        'responsable': 'CMO / Director de Marketing',
        'tipo': 'KPI Táctico',
        'relacion_nsm': 'Impacto en rentabilidad: CAC bajo permite escalar adquisición manteniendo márgenes'
    },
    'Tasa_Conversion': {
        'nombre': 'Tasa de Conversión',
        'definicion': 'Porcentaje de visitantes que completan una compra del total de visitantes al sitio.',
        'objetivo': '>= 3.5% (incremento de +1.5pp)',
        'frecuencia': 'Diaria / Semanal',
        'fuente': 'Google Analytics + Base de órdenes',
        'formula': 'Tasa Conversión = (Órdenes Completadas / Sesiones Totales) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'CMO / Product Manager',
        'tipo': 'KPI Táctico',
        'relacion_nsm': 'Impacto alto: Mejorar conversión maximiza GMV con el mismo tráfico'
    },
    'Abandono_Carrito': {
        'nombre': 'Tasa de Abandono de Carrito',
        'definicion': 'Porcentaje de usuarios que agregan productos al carrito pero no completan la compra.',
        'objetivo': '<= 65% (reducción de -5pp)',
        'frecuencia': 'Diaria / Semanal',
        'fuente': 'Sistema de e-commerce - eventos de carrito',
        'formula': 'Abandono = (Carritos Abandonados / Carritos Creados) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'Product Manager / UX Lead',
        'tipo': 'KPI Táctico',
        'relacion_nsm': 'Impacto medio-alto: Reducir abandono aumenta conversiones y GMV'
    },
    'Rating_Promedio': {
        'nombre': 'Rating Promedio de Clientes',
        'definicion': 'Puntuación promedio otorgada por clientes a sus compras, en escala de 1 a 5 estrellas.',
        'objetivo': '>= 4.0 estrellas',
        'frecuencia': 'Diaria (monitoreo) / Semanal (análisis)',
        'fuente': 'Base de datos de reviews - tabla order_reviews',
        'formula': 'Rating Promedio = AVG(review_score) WHERE review_score IS NOT NULL',
        'unidad': 'Puntuación (1-5 estrellas)',
        'responsable': 'COO / Director de Operaciones',
        'tipo': 'KPI Operativo',
        'relacion_nsm': 'Impacto en retención: Clientes satisfechos compran más y recomiendan'
    },
    'Tiempo_Entrega': {
        'nombre': 'Tiempo Promedio de Entrega',
        'definicion': 'Número promedio de días desde la compra hasta la entrega del producto al cliente.',
        'objetivo': '<= 7 días promedio',
        'frecuencia': 'Diaria (monitoreo) / Semanal (análisis)',
        'fuente': 'Base de datos de órdenes - diferencia entre order_delivered y order_purchase',
        'formula': 'Tiempo Entrega = AVG(fecha_entrega - fecha_compra) en días',
        'unidad': 'Días',
        'responsable': 'COO / Director de Logística',
        'tipo': 'KPI Operativo',
        'relacion_nsm': 'Impacto en satisfacción: Entregas rápidas mejoran rating y recompra'
    },
    'Entregas_Rapidas': {
        'nombre': 'Porcentaje de Entregas Rápidas',
        'definicion': 'Porcentaje de órdenes entregadas en 7 días o menos desde la compra.',
        'objetivo': '>= 60% de entregas en 7 días o menos',
        'frecuencia': 'Semanal',
        'fuente': 'Base de datos de órdenes - tabla orders',
        'formula': '% Rápidas = (Órdenes con entrega <= 7 días / Total Órdenes) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'COO / Director de Logística',
        'tipo': 'KPI Operativo',
        'relacion_nsm': 'Impacto en experiencia: Más entregas rápidas = mejor NPS y retención'
    },
    'Clientes_Satisfechos': {
        'nombre': 'Porcentaje de Clientes Satisfechos',
        'definicion': 'Porcentaje de clientes que califican su experiencia con 4 o 5 estrellas.',
        'objetivo': '>= 80% de clientes satisfechos',
        'frecuencia': 'Semanal / Mensual',
        'fuente': 'Base de datos de reviews - tabla order_reviews',
        'formula': '% Satisfechos = (Reviews con score >= 4 / Total Reviews) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'COO / Director de Customer Success',
        'tipo': 'KPI Operativo',
        'relacion_nsm': 'Impacto en LTV: Clientes satisfechos tienen mayor lifetime value'
    },
    'NPS': {
        'nombre': 'NPS (Net Promoter Score)',
        'definicion': 'Métrica que mide la lealtad del cliente basada en la probabilidad de recomendar la empresa.',
        'objetivo': '>= 45 puntos',
        'frecuencia': 'Mensual / Trimestral',
        'fuente': 'Encuestas NPS - pregunta "¿Qué tan probable es que recomiende..."',
        'formula': 'NPS = % Promotores (9-10) - % Detractores (0-6)',
        'unidad': 'Puntuación (-100 a +100)',
        'responsable': 'CEO / Director de Customer Experience',
        'tipo': 'KPI Estratégico',
        'relacion_nsm': 'Impacto en crecimiento orgánico: NPS alto genera referidos y reduce CAC'
    },
    'Clientes_Recurrentes': {
        'nombre': 'Porcentaje de Clientes Recurrentes',
        'definicion': 'Porcentaje de clientes que han realizado más de una compra en un período.',
        'objetivo': 'Incremento de +8pp anual',
        'frecuencia': 'Mensual',
        'fuente': 'Base de datos de órdenes - agrupado por customer_id',
        'formula': '% Recurrentes = (Clientes con >1 orden / Total Clientes) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'CMO / Director de Retención',
        'tipo': 'KPI Táctico',
        'relacion_nsm': 'Impacto alto: Clientes recurrentes generan GMV con menor CAC'
    },
    'Visitas_Organicas': {
        'nombre': 'Crecimiento de Visitas Orgánicas',
        'definicion': 'Incremento porcentual de visitas provenientes de búsqueda orgánica (SEO).',
        'objetivo': '+20% de crecimiento anual',
        'frecuencia': 'Semanal / Mensual',
        'fuente': 'Google Analytics - canal orgánico',
        'formula': 'Crecimiento = ((Visitas Actuales - Visitas Anteriores) / Visitas Anteriores) x 100',
        'unidad': 'Porcentaje (%)',
        'responsable': 'CMO / SEO Manager',
        'tipo': 'KPI Táctico',
        'relacion_nsm': 'Impacto en eficiencia: Tráfico orgánico no tiene costo marginal'
    }
}

# CSS personalizado con estilo Nuclio
st.markdown(f"""
<style>
    /* Fuente principal */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}

    /* Header principal */
    .main-header {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['black']} 0%, #2d2d2d 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .nuclio-logo {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .logo-circle {{
        width: 40px;
        height: 40px;
        background: {NUCLIO_COLORS['yellow']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .logo-inner {{
        width: 15px;
        height: 15px;
        background: {NUCLIO_COLORS['white']};
        border-radius: 50%;
    }}

    .header-title {{
        color: {NUCLIO_COLORS['white']};
        font-size: 1.1rem;
        font-weight: 500;
    }}

    .header-slogan {{
        color: {NUCLIO_COLORS['gray_medium']};
        font-size: 0.85rem;
    }}

    .header-slogan span {{
        color: {NUCLIO_COLORS['yellow']};
    }}

    /* Métricas KPI mejoradas */
    .kpi-card {{
        background: {NUCLIO_COLORS['white']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #eee;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }}

    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: {NUCLIO_COLORS['yellow']};
    }}

    .kpi-card.green::before {{
        background: {NUCLIO_COLORS['green']};
    }}

    .kpi-card.purple::before {{
        background: {NUCLIO_COLORS['purple']};
    }}

    .kpi-card.red::before {{
        background: {NUCLIO_COLORS['red']};
    }}

    .kpi-title {{
        color: {NUCLIO_COLORS['gray_text']};
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {NUCLIO_COLORS['black']};
        line-height: 1.1;
    }}

    .kpi-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.75rem;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 20px;
    }}

    .kpi-delta.positive {{
        color: {NUCLIO_COLORS['green_dark']};
        background: {NUCLIO_COLORS['green_light']};
    }}

    .kpi-delta.negative {{
        color: {NUCLIO_COLORS['red']};
        background: {NUCLIO_COLORS['red_light']};
    }}

    /* Ficha Técnica del KPI */
    .ficha-tecnica {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['gray_light']} 0%, #fff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid {NUCLIO_COLORS['yellow']};
    }}

    .ficha-tecnica h4 {{
        color: {NUCLIO_COLORS['black']};
        margin: 0 0 1rem 0;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .ficha-row {{
        display: flex;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid #eee;
        padding-bottom: 0.75rem;
    }}

    .ficha-row:last-child {{
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }}

    .ficha-label {{
        font-weight: 600;
        color: {NUCLIO_COLORS['black']};
        width: 180px;
        flex-shrink: 0;
        font-size: 0.85rem;
    }}

    .ficha-value {{
        color: {NUCLIO_COLORS['gray_text']};
        font-size: 0.85rem;
        line-height: 1.4;
    }}

    /* Dashboard Persona Card */
    .persona-card {{
        background: {NUCLIO_COLORS['white']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-top: 5px solid;
    }}

    .persona-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }}

    .persona-avatar {{
        font-size: 3rem;
        width: 70px;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
    }}

    .persona-info h3 {{
        margin: 0;
        font-size: 1.2rem;
        color: {NUCLIO_COLORS['black']};
    }}

    .persona-info p {{
        margin: 0.25rem 0 0 0;
        color: {NUCLIO_COLORS['gray_text']};
        font-size: 0.9rem;
    }}

    .persona-section {{
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }}

    .persona-section h4 {{
        font-size: 0.85rem;
        color: {NUCLIO_COLORS['black']};
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .persona-list {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}

    .persona-list li {{
        padding: 0.35rem 0;
        padding-left: 1.25rem;
        position: relative;
        font-size: 0.85rem;
        color: {NUCLIO_COLORS['gray_text']};
    }}

    .persona-list li::before {{
        content: '•';
        position: absolute;
        left: 0;
        font-weight: bold;
    }}

    .persona-tag {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }}

    /* Sección de stakeholder */
    .stakeholder-badge {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 0.75rem 1.25rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }}

    .badge-ceo {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['yellow']}30 0%, {NUCLIO_COLORS['yellow']}10 100%);
        color: #B8860B;
        border: 2px solid {NUCLIO_COLORS['yellow']};
    }}

    .badge-cmo {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['purple']}30 0%, {NUCLIO_COLORS['purple']}10 100%);
        color: {NUCLIO_COLORS['purple']};
        border: 2px solid {NUCLIO_COLORS['purple']};
    }}

    .badge-coo {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['green']}30 0%, {NUCLIO_COLORS['green']}10 100%);
        color: {NUCLIO_COLORS['green']};
        border: 2px solid {NUCLIO_COLORS['green']};
    }}

    /* Árbol de KPIs */
    .kpi-tree-node {{
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        font-weight: 500;
        text-align: center;
        font-size: 0.85rem;
    }}

    .node-nsm {{
        background: {NUCLIO_COLORS['black']};
        color: {NUCLIO_COLORS['white']};
    }}

    .node-objective {{
        background: #333;
        color: {NUCLIO_COLORS['white']};
    }}

    .node-strategy {{
        background: {NUCLIO_COLORS['yellow']};
        color: {NUCLIO_COLORS['black']};
    }}

    .node-tactic {{
        background: {NUCLIO_COLORS['purple']};
        color: {NUCLIO_COLORS['white']};
    }}

    .node-kpi {{
        background: {NUCLIO_COLORS['green']};
        color: {NUCLIO_COLORS['white']};
    }}

    /* Sidebar - Contraste mejorado */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NUCLIO_COLORS['black']} 0%, #1a1a1a 100%);
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdown"] {{
        color: {NUCLIO_COLORS['white']} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h4 {{
        color: {NUCLIO_COLORS['white']} !important;
    }}

    [data-testid="stSidebar"] label {{
        color: {NUCLIO_COLORS['white']} !important;
    }}

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
        color: {NUCLIO_COLORS['white']} !important;
        font-weight: 600;
    }}

    [data-testid="stSidebar"] [data-testid="stMetricValue"],
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: {NUCLIO_COLORS['white']} !important;
    }}

    [data-testid="stSidebar"] .sidebar-title {{
        color: {NUCLIO_COLORS['white']} !important;
        font-size: 1.5rem;
        font-weight: 700;
    }}

    [data-testid="stSidebar"] .sidebar-subtitle {{
        color: #cccccc !important;
        font-size: 0.9rem;
    }}

    [data-testid="stSidebar"] .sidebar-section-title {{
        color: {NUCLIO_COLORS['yellow']} !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    [data-testid="stSidebar"] .sidebar-metric-value {{
        color: {NUCLIO_COLORS['yellow']} !important;
        font-size: 2rem;
        font-weight: 700;
    }}

    [data-testid="stSidebar"] .sidebar-metric-label {{
        color: #cccccc !important;
        font-size: 0.85rem;
    }}

    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {NUCLIO_COLORS['gray_light']};
        padding: 8px;
        border-radius: 12px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }}

    .stTabs [aria-selected="true"] {{
        background: {NUCLIO_COLORS['yellow']} !important;
        color: {NUCLIO_COLORS['black']} !important;
    }}

    /* Info boxes */
    .info-box {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['blue_light']} 0%, #fff 100%);
        border-left: 4px solid {NUCLIO_COLORS['blue']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        color: {NUCLIO_COLORS['black']};
    }}

    .info-box strong {{
        color: {NUCLIO_COLORS['blue']};
    }}

    .success-box {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['green_light']} 0%, #fff 100%);
        border-left: 4px solid {NUCLIO_COLORS['green']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        color: {NUCLIO_COLORS['black']};
    }}

    .success-box strong {{
        color: {NUCLIO_COLORS['green_dark']};
    }}

    .warning-box {{
        background: linear-gradient(135deg, #FFF8E1 0%, #fff 100%);
        border-left: 4px solid {NUCLIO_COLORS['orange']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
    }}

    /* Info box amarilla */
    .info-box-yellow {{
        background: linear-gradient(135deg, #FFFDE7 0%, #FFF 100%);
        border-left: 4px solid {NUCLIO_COLORS['yellow']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        color: {NUCLIO_COLORS['black']};
    }}

    .info-box-yellow strong {{
        color: #B8860B;
    }}

    .info-box-yellow p {{
        color: {NUCLIO_COLORS['black']};
        margin: 0;
    }}

    /* Info box púrpura */
    .info-box-purple {{
        background: linear-gradient(135deg, #F3E5F5 0%, #FFF 100%);
        border-left: 4px solid {NUCLIO_COLORS['purple']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        color: {NUCLIO_COLORS['black']};
    }}

    .info-box-purple strong {{
        color: {NUCLIO_COLORS['purple']};
    }}

    .info-box-purple p {{
        color: {NUCLIO_COLORS['black']};
        margin: 0;
    }}

    /* Info box verde */
    .info-box-green {{
        background: linear-gradient(135deg, {NUCLIO_COLORS['green_light']} 0%, #FFF 100%);
        border-left: 4px solid {NUCLIO_COLORS['green']};
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        color: {NUCLIO_COLORS['black']};
    }}

    .info-box-green strong {{
        color: {NUCLIO_COLORS['green_dark']};
    }}

    .info-box-green p {{
        color: {NUCLIO_COLORS['black']};
        margin: 0;
    }}

    /* Fondo principal claro */
    .stApp {{
        background-color: #FFFFFF;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: #FFFFFF;
    }}

    [data-testid="stHeader"] {{
        background-color: transparent;
    }}

    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Divider con estilo */
    .custom-divider {{
        height: 2px;
        background: linear-gradient(to right, transparent, {NUCLIO_COLORS['yellow']}, transparent);
        margin: 2rem 0;
    }}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CARGA DE DATOS
# =============================================================================
@st.cache_data
def load_data():
    """Carga el dataset de Olist"""
    data_path = Path(__file__).parent / "data" / "olist_dashboard_dataset.csv"

    if not data_path.exists():
        # Generar datos de ejemplo si no existe el archivo
        np.random.seed(42)
        n_records = 10000

        categories = ['Bed Bath Table', 'Health Beauty', 'Sports Leisure', 'Computers Accessories',
                     'Furniture Decor', 'Toys', 'Watches Gifts', 'Telephony', 'Auto', 'Baby']
        states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO', 'DF', 'PE']
        payment_methods = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        dates = pd.date_range('2017-01-01', '2018-08-31', periods=n_records)

        df = pd.DataFrame({
            'order_id': [f'order_{i}' for i in range(n_records)],
            'customer_id': [f'customer_{np.random.randint(1, 5000)}' for _ in range(n_records)],
            'fecha': dates,
            'ano': [d.year for d in dates],
            'mes': [d.month for d in dates],
            'mes_nombre': [d.strftime('%Y-%m') for d in dates],
            'dia_semana': np.random.choice(days, n_records),
            'estado': np.random.choice(states, n_records, p=[0.35, 0.15, 0.12, 0.08, 0.08, 0.06, 0.06, 0.04, 0.03, 0.03]),
            'categoria': np.random.choice(categories, n_records),
            'precio': np.random.exponential(100, n_records) + 10,
            'costo_envio': np.random.exponential(15, n_records) + 5,
            'valor_total_pagado': np.random.exponential(120, n_records) + 15,
            'metodo_pago': np.random.choice(payment_methods, n_records, p=[0.76, 0.19, 0.03, 0.02]),
            'cuotas': np.random.choice(range(1, 11), n_records),
            'dias_entrega': np.random.exponential(10, n_records) + 2,
            'rating': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.05, 0.05, 0.1, 0.23, 0.57])
        })

        return df

    df = pd.read_csv(data_path)
    column_mapping = {'año': 'ano'}
    df = df.rename(columns=column_mapping)
    return df


def calculate_kpis(df):
    """Calcula los KPIs principales del dashboard"""
    total_orders = df['order_id'].nunique()
    gmv = df['precio'].sum()
    aov = df['precio'].mean()
    avg_rating = df['rating'].mean()
    avg_delivery_days = df['dias_entrega'].mean()
    fast_delivery_pct = (df['dias_entrega'] <= 7).mean() * 100
    satisfied_customers_pct = (df['rating'] >= 4).mean() * 100
    total_customers = df['customer_id'].nunique()

    orders_per_customer = df.groupby('customer_id')['order_id'].nunique()
    recurrent_customers_pct = (orders_per_customer > 1).mean() * 100

    return {
        'total_orders': total_orders,
        'gmv': gmv,
        'aov': aov,
        'avg_rating': avg_rating,
        'avg_delivery_days': avg_delivery_days,
        'fast_delivery_pct': fast_delivery_pct,
        'satisfied_customers_pct': satisfied_customers_pct,
        'total_customers': total_customers,
        'recurrent_customers_pct': recurrent_customers_pct
    }


# =============================================================================
# COMPONENTES DE UI
# =============================================================================
def render_header():
    """Renderiza el header con el estilo de Nuclio"""
    st.markdown("""
    <div class="main-header">
        <div class="nuclio-logo">
            <div class="logo-circle">
                <div class="logo-inner"></div>
            </div>
            <div>
                <div class="header-title">Nuclio Digital School</div>
                <div class="header-slogan">Learn <span>[to be]</span> the future</div>
            </div>
        </div>
        <div style="color: white; font-size: 1.5rem; font-weight: 600;">
            E-commerce Analytics Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard_persona(stakeholder_key):
    """Renderiza la tarjeta de Dashboard Persona"""
    persona = DASHBOARD_PERSONAS.get(stakeholder_key)
    if not persona:
        return

    color = persona['color']
    objetivos_html = ''.join([f'<li>{obj}</li>' for obj in persona['objetivos']])
    pain_points_html = ''.join([f'<li>{pp}</li>' for pp in persona['pain_points']])
    necesidades_html = ''.join([f'<li>{nec}</li>' for nec in persona['necesidades_dashboard']])
    kpis_html = ''.join([f'<span class="persona-tag" style="background: {color}20; color: {color};">{kpi}</span>' for kpi in persona['kpis_principales']])

    st.markdown(f"""
    <div class="persona-card" style="border-top-color: {color};">
        <div class="persona-header">
            <div class="persona-avatar">{persona['foto_emoji']}</div>
            <div class="persona-info">
                <h3>{persona['nombre']}</h3>
                <p>{persona['cargo']}</p>
            </div>
        </div>
        <p style="color: {NUCLIO_COLORS['gray_text']}; font-size: 0.9rem; margin: 0;">
            {persona['descripcion']}
        </p>

        <div class="persona-section">
            <h4>Objetivos</h4>
            <ul class="persona-list" style="--bullet-color: {color};">{objetivos_html}</ul>
        </div>

        <div class="persona-section">
            <h4>Pain Points</h4>
            <ul class="persona-list">{pain_points_html}</ul>
        </div>

        <div class="persona-section">
            <h4>Necesidades del Dashboard</h4>
            <ul class="persona-list">{necesidades_html}</ul>
        </div>

        <div class="persona-section">
            <h4>Frecuencia de Uso</h4>
            <p style="font-size: 0.85rem; color: {NUCLIO_COLORS['gray_text']}; margin: 0;">
                {persona['frecuencia_uso']}
            </p>
        </div>

        <div class="persona-section">
            <h4>KPIs Principales</h4>
            <div>{kpis_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_ficha_tecnica(kpi_key):
    """Renderiza la ficha técnica de un KPI"""
    if kpi_key not in KPI_FICHAS_TECNICAS:
        return

    ficha = KPI_FICHAS_TECNICAS[kpi_key]

    st.markdown(f"""
    <div class="ficha-tecnica">
        <h4>Ficha Técnica: {ficha['nombre']}</h4>
        <div class="ficha-row">
            <span class="ficha-label">Definición de Negocio</span>
            <span class="ficha-value">{ficha['definicion']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Objetivo (Target)</span>
            <span class="ficha-value">{ficha['objetivo']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Frecuencia de Medición</span>
            <span class="ficha-value">{ficha['frecuencia']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Fuente de Datos</span>
            <span class="ficha-value">{ficha['fuente']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Fórmula Matemática</span>
            <span class="ficha-value"><code>{ficha['formula']}</code></span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Unidad de Medida</span>
            <span class="ficha-value">{ficha['unidad']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Responsable</span>
            <span class="ficha-value">{ficha['responsable']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Tipo de KPI</span>
            <span class="ficha-value">{ficha['tipo']}</span>
        </div>
        <div class="ficha-row">
            <span class="ficha-label">Relación con NSM</span>
            <span class="ficha-value">{ficha['relacion_nsm']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card_enhanced(title, value, delta=None, delta_label="vs período anterior",
                             prefix="", suffix="", kpi_key=None, color="yellow"):
    """Renderiza una tarjeta de KPI mejorada con opción de ficha técnica"""
    delta_html = ""
    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        delta_sign = "+" if delta >= 0 else ""
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div class="kpi-delta {delta_class}">{arrow} {delta_sign}{delta:.1f}% {delta_label}</div>'

    st.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

    if kpi_key and kpi_key in KPI_FICHAS_TECNICAS:
        with st.expander(f"Ver Ficha Técnica de {title}"):
            render_ficha_tecnica(kpi_key)


def render_gauge_chart(value, max_val, target, title, color):
    """Renderiza un gráfico de gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 14}},
        delta={'reference': target, 'increasing': {'color': NUCLIO_COLORS['green']},
               'decreasing': {'color': NUCLIO_COLORS['red']}},
        gauge={
            'axis': {'range': [None, max_val], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, target * 0.7], 'color': NUCLIO_COLORS['red_light']},
                {'range': [target * 0.7, target], 'color': '#FFF8E1'},
                {'range': [target, max_val], 'color': NUCLIO_COLORS['green_light']}
            ],
            'threshold': {
                'line': {'color': NUCLIO_COLORS['black'], 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))

    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    return fig


def render_stakeholder_badge(stakeholder):
    """Renderiza el badge del stakeholder"""
    badges = {
        'CEO': ('badge-ceo', 'CEO - Chief Executive Officer', 'Visión Estratégica'),
        'CMO': ('badge-cmo', 'CMO - Chief Marketing Officer', 'Performance de Marketing'),
        'COO': ('badge-coo', 'COO - Chief Operations Officer', 'Eficiencia Operacional')
    }

    badge_class, title, subtitle = badges.get(stakeholder, ('badge-ceo', stakeholder, ''))

    st.markdown(f"""
    <div class="stakeholder-badge {badge_class}">
        <div>
            <div style="font-size: 1rem;">{title}</div>
            <div style="font-size: 0.75rem; font-weight: 400; opacity: 0.8;">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_tree():
    """Renderiza el árbol de KPIs interactivo mejorado"""
    st.markdown("### Árbol de KPIs - E-commerce")

    st.markdown("""
    <div class="info-box">
        <strong>Framework de KPIs:</strong> El árbol muestra la jerarquía completa desde la
        North Star Metric hasta los KPIs operacionales. Cada nivel representa mayor detalle y accionabilidad.
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    nodes = [
        {'label': 'GMV\n(Gross Merchandise Value)', 'x': 0.5, 'y': 1.0,
         'color': NUCLIO_COLORS['black'], 'text_color': 'white', 'size': 0.095},
        {'label': 'Aumentar Ingresos\n+25% en 12 meses', 'x': 0.5, 'y': 0.85,
         'color': '#333333', 'text_color': 'white', 'size': 0.09},
        {'label': 'Incrementar\nAdquisición', 'x': 0.17, 'y': 0.65,
         'color': NUCLIO_COLORS['yellow'], 'text_color': 'black', 'size': 0.08},
        {'label': 'Mejorar\nConversión', 'x': 0.5, 'y': 0.65,
         'color': NUCLIO_COLORS['yellow'], 'text_color': 'black', 'size': 0.08},
        {'label': 'Aumentar\nRetención', 'x': 0.83, 'y': 0.65,
         'color': NUCLIO_COLORS['yellow'], 'text_color': 'black', 'size': 0.08},
        {'label': 'Optimizar\nCampañas', 'x': 0.08, 'y': 0.45,
         'color': NUCLIO_COLORS['purple'], 'text_color': 'white', 'size': 0.07},
        {'label': 'Mejorar\nSEO', 'x': 0.26, 'y': 0.45,
         'color': NUCLIO_COLORS['purple'], 'text_color': 'white', 'size': 0.07},
        {'label': 'Reducir Fricción\nCheckout', 'x': 0.5, 'y': 0.45,
         'color': NUCLIO_COLORS['purple'], 'text_color': 'white', 'size': 0.07},
        {'label': 'Programa\nFidelización', 'x': 0.74, 'y': 0.45,
         'color': NUCLIO_COLORS['purple'], 'text_color': 'white', 'size': 0.07},
        {'label': 'Mejorar\nPostventa', 'x': 0.92, 'y': 0.45,
         'color': NUCLIO_COLORS['purple'], 'text_color': 'white', 'size': 0.07},
        {'label': 'CAC\n<=45 EUR', 'x': 0.04, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'Visitas\nOrgánicas\n+20%', 'x': 0.17, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'Tasa\nConversión\n+1.5pp', 'x': 0.30, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'Abandono\nCarrito\n-5pp', 'x': 0.43, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': '%Clientes\nRecurrentes\n+8pp', 'x': 0.57, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'NPS\n>=45', 'x': 0.70, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'Rating\n>=4.0', 'x': 0.83, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
        {'label': 'Entregas\n<=7días\n60%', 'x': 0.96, 'y': 0.22,
         'color': NUCLIO_COLORS['green'], 'text_color': 'white', 'size': 0.055},
    ]

    for node in nodes:
        fig.add_shape(
            type="rect",
            x0=node['x'] - node['size'] + 0.005,
            y0=node['y'] - 0.055,
            x1=node['x'] + node['size'] + 0.005,
            y1=node['y'] + 0.055,
            fillcolor='rgba(0,0,0,0.1)',
            line=dict(width=0),
            layer="below"
        )
        fig.add_shape(
            type="rect",
            x0=node['x'] - node['size'],
            y0=node['y'] - 0.06,
            x1=node['x'] + node['size'],
            y1=node['y'] + 0.06,
            fillcolor=node['color'],
            line=dict(width=0),
            layer="below"
        )
        fig.add_annotation(
            x=node['x'], y=node['y'],
            text=node['label'],
            showarrow=False,
            font=dict(size=9, color=node['text_color'], family='Inter'),
            align="center"
        )

    connections = [
        (0.5, 0.94, 0.5, 0.91),
        (0.5, 0.79, 0.17, 0.71), (0.5, 0.79, 0.5, 0.71), (0.5, 0.79, 0.83, 0.71),
        (0.17, 0.59, 0.08, 0.51), (0.17, 0.59, 0.26, 0.51),
        (0.5, 0.59, 0.5, 0.51),
        (0.83, 0.59, 0.74, 0.51), (0.83, 0.59, 0.92, 0.51),
        (0.08, 0.39, 0.04, 0.28),
        (0.26, 0.39, 0.17, 0.28), (0.26, 0.39, 0.30, 0.28),
        (0.5, 0.39, 0.43, 0.28), (0.5, 0.39, 0.57, 0.28),
        (0.74, 0.39, 0.70, 0.28),
        (0.92, 0.39, 0.83, 0.28), (0.92, 0.39, 0.96, 0.28),
    ]

    for x0, y0, x1, y1 in connections:
        fig.add_shape(
            type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color=NUCLIO_COLORS['gray_medium'], width=2),
            layer="below"
        )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[-0.02, 1.02]),
        yaxis=dict(visible=False, range=[0.12, 1.08]),
        margin=dict(l=10, r=10, t=10, b=10),
        height=550,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Leyenda del Árbol")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="kpi-tree-node node-nsm">North Star Metric</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-tree-node node-objective">Objetivo</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-tree-node node-strategy">Estrategia</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="kpi-tree-node node-tactic">Táctica</div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="kpi-tree-node node-kpi">KPI</div>', unsafe_allow_html=True)


def render_ceo_dashboard(df, kpis):
    """Dashboard para el CEO - Visión estratégica con fichas técnicas"""
    render_stakeholder_badge('CEO')

    # Mostrar Dashboard Persona
    with st.expander("Ver Dashboard Persona - CEO", expanded=False):
        render_dashboard_persona('CEO')

    st.markdown("""
    <div class="info-box-yellow">
        <p><strong>Visión Estratégica:</strong> Este dashboard presenta los KPIs de alto nivel
        para la toma de decisiones estratégicas. Cada KPI incluye su ficha técnica completa
        con definición, fórmula, objetivo y responsable.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### KPIs Estratégicos")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card_enhanced("GMV Total", f"{kpis['gmv']:,.0f}", delta=12.5, prefix="R$ ", kpi_key='GMV', color='yellow')
    with col2:
        render_kpi_card_enhanced("Total Órdenes", f"{kpis['total_orders']:,}", delta=8.3, kpi_key='Total_Ordenes', color='yellow')
    with col3:
        render_kpi_card_enhanced("Ticket Promedio (AOV)", f"{kpis['aov']:.2f}", delta=3.7, prefix="R$ ", kpi_key='AOV', color='yellow')
    with col4:
        render_kpi_card_enhanced("Clientes Únicos", f"{kpis['total_customers']:,}", delta=15.2, kpi_key='Total_Clientes', color='yellow')

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### Progreso hacia Objetivos")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = render_gauge_chart(kpis['avg_rating'], 5, 4.0, "Rating Promedio", NUCLIO_COLORS['yellow'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_gauge_chart(kpis['satisfied_customers_pct'], 100, 80, "% Clientes Satisfechos", NUCLIO_COLORS['green'])
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = render_gauge_chart(kpis['fast_delivery_pct'], 100, 60, "% Entregas Rápidas", NUCLIO_COLORS['purple'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Evolución de GMV por Mes")
        monthly_gmv = df.groupby('mes_nombre')['precio'].sum().reset_index()
        monthly_gmv.columns = ['Mes', 'GMV']
        monthly_gmv = monthly_gmv.sort_values('Mes')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_gmv['Mes'], y=monthly_gmv['GMV'],
            mode='lines+markers', fill='tozeroy',
            line=dict(color=NUCLIO_COLORS['yellow'], width=3),
            marker=dict(size=8, color=NUCLIO_COLORS['black']),
            fillcolor='rgba(255, 198, 48, 0.2)'
        ))

        z = np.polyfit(range(len(monthly_gmv)), monthly_gmv['GMV'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=monthly_gmv['Mes'], y=p(range(len(monthly_gmv))),
            mode='lines', line=dict(color=NUCLIO_COLORS['red'], width=2, dash='dash'),
            name='Tendencia'
        ))

        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=60),
                         xaxis_title="", yaxis_title="GMV (R$)",
                         plot_bgcolor='white', paper_bgcolor='white',
                         showlegend=True, legend=dict(orientation='h', y=-0.15))
        fig.update_xaxes(tickangle=45, gridcolor='#eee')
        fig.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Distribución por Estado (Top 10)")
        state_gmv = df.groupby('estado')['precio'].sum().nlargest(10).reset_index()
        state_gmv.columns = ['Estado', 'GMV']

        fig = px.bar(state_gmv, x='Estado', y='GMV', color='GMV',
                    color_continuous_scale=[[0, NUCLIO_COLORS['gray_light']],
                                           [0.5, NUCLIO_COLORS['yellow']],
                                           [1, NUCLIO_COLORS['black']]])
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                         xaxis_title="", yaxis_title="GMV (R$)",
                         plot_bgcolor='white', paper_bgcolor='white',
                         coloraxis_showscale=False)
        fig.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)


def render_cmo_dashboard(df, kpis):
    """Dashboard para el CMO - Performance de Marketing con fichas técnicas"""
    render_stakeholder_badge('CMO')

    with st.expander("Ver Dashboard Persona - CMO", expanded=False):
        render_dashboard_persona('CMO')

    st.markdown("""
    <div class="info-box-purple">
        <p><strong>Performance de Marketing:</strong> Métricas clave para evaluar la efectividad
        de las campañas, segmentación de clientes y comportamiento de compra. Incluye fichas
        técnicas de cada indicador.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### KPIs de Marketing")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card_enhanced("Ticket Promedio (AOV)", f"{kpis['aov']:.2f}", delta=5.2, prefix="R$ ", kpi_key='AOV', color='purple')
    with col2:
        credit_card_pct = (df['metodo_pago'] == 'Credit Card').mean() * 100
        render_kpi_card_enhanced("% Pago con Tarjeta", f"{credit_card_pct:.1f}", suffix="%", color='purple')
    with col3:
        render_kpi_card_enhanced("% Clientes Recurrentes", f"{kpis['recurrent_customers_pct']:.1f}", delta=2.3, suffix="%", kpi_key='Clientes_Recurrentes', color='purple')
    with col4:
        render_kpi_card_enhanced("Rating Promedio", f"{kpis['avg_rating']:.2f}", delta=2.1, suffix="/5", kpi_key='Rating_Promedio', color='purple')

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Categorías por Ventas")
        cat_sales = df.groupby('categoria').agg({'precio': 'sum', 'order_id': 'nunique', 'rating': 'mean'}).reset_index()
        cat_sales.columns = ['Categoría', 'Ventas', 'Órdenes', 'Rating']
        cat_sales = cat_sales.nlargest(10, 'Ventas')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=cat_sales['Categoría'], x=cat_sales['Ventas'], orientation='h',
            marker=dict(color=cat_sales['Ventas'],
                       colorscale=[[0, NUCLIO_COLORS['purple_light']], [1, NUCLIO_COLORS['purple']]]),
            text=[f"R$ {v:,.0f}" for v in cat_sales['Ventas']],
            textposition='inside', textfont=dict(color='white')
        ))
        fig.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=20),
                         yaxis_title="", xaxis_title="Ventas (R$)",
                         plot_bgcolor='white', paper_bgcolor='white')
        fig.update_xaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Distribución de Métodos de Pago")
        payment_dist = df['metodo_pago'].value_counts().reset_index()
        payment_dist.columns = ['Método', 'Cantidad']

        fig = go.Figure(data=[go.Pie(
            labels=payment_dist['Método'], values=payment_dist['Cantidad'], hole=0.5,
            marker=dict(colors=[NUCLIO_COLORS['yellow'], NUCLIO_COLORS['purple'],
                               NUCLIO_COLORS['green'], NUCLIO_COLORS['gray_medium']]),
            textinfo='label+percent', textposition='outside'
        )])
        fig.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=20), showlegend=False,
                         annotations=[dict(text='Pagos', x=0.5, y=0.5, font_size=16, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Patrón de Ventas por Día de la Semana")
    day_translation = {
        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_sales = df.groupby('dia_semana').agg({'precio': ['sum', 'mean', 'count']}).reset_index()
    day_sales.columns = ['Día', 'Total Ventas', 'Ticket Promedio', 'Núm Órdenes']
    day_sales['Día_orden'] = day_sales['Día'].map({d: i for i, d in enumerate(day_order)})
    day_sales = day_sales.sort_values('Día_orden')
    day_sales['Día_ES'] = day_sales['Día'].map(day_translation)

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Ventas Totales por Día', 'Ticket Promedio por Día'))
    fig.add_trace(go.Bar(x=day_sales['Día_ES'], y=day_sales['Total Ventas'],
                        marker_color=NUCLIO_COLORS['yellow'], name='Ventas'), row=1, col=1)
    fig.add_trace(go.Bar(x=day_sales['Día_ES'], y=day_sales['Ticket Promedio'],
                        marker_color=NUCLIO_COLORS['purple'], name='Ticket'), row=1, col=2)
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20),
                     plot_bgcolor='white', paper_bgcolor='white', showlegend=False)
    fig.update_yaxes(gridcolor='#eee')
    st.plotly_chart(fig, use_container_width=True)


def render_coo_dashboard(df, kpis):
    """Dashboard para el COO - Eficiencia Operacional con fichas técnicas"""
    render_stakeholder_badge('COO')

    with st.expander("Ver Dashboard Persona - COO", expanded=False):
        render_dashboard_persona('COO')

    st.markdown("""
    <div class="info-box-green">
        <p><strong>Eficiencia Operacional:</strong> Métricas de desempeño operativo,
        tiempos de entrega, satisfacción del cliente y eficiencia logística. Cada KPI
        incluye su ficha técnica con fórmula y objetivo.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### KPIs Operacionales")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card_enhanced("Tiempo Entrega Prom.", f"{kpis['avg_delivery_days']:.1f}", delta=-8.5, suffix=" días", kpi_key='Tiempo_Entrega', color='green')
    with col2:
        render_kpi_card_enhanced("% Entregas Rápidas", f"{kpis['fast_delivery_pct']:.1f}", delta=5.3, suffix="%", kpi_key='Entregas_Rapidas', color='green')
    with col3:
        render_kpi_card_enhanced("% Clientes Satisfechos", f"{kpis['satisfied_customers_pct']:.1f}", delta=3.2, suffix="%", kpi_key='Clientes_Satisfechos', color='green')
    with col4:
        render_kpi_card_enhanced("Rating Promedio", f"{kpis['avg_rating']:.2f}", delta=1.8, suffix="/5", kpi_key='Rating_Promedio', color='green')

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### Estado de Objetivos Operacionales")
    col1, col2, col3 = st.columns(3)

    with col1:
        delivery_score = max(0, 100 - (kpis['avg_delivery_days'] - 7) * 10)
        fig = render_gauge_chart(min(delivery_score, 100), 100, 70, "Score Entrega (7 días = 100)", NUCLIO_COLORS['green'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_gauge_chart(kpis['avg_rating'], 5, 4.0, "Rating Objetivo >= 4.0", NUCLIO_COLORS['yellow'])
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = render_gauge_chart(kpis['satisfied_customers_pct'], 100, 80, "Satisfacción Objetivo >= 80%", NUCLIO_COLORS['purple'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribución de Ratings")
        rating_dist = df['rating'].value_counts().sort_index().reset_index()
        rating_dist.columns = ['Rating', 'Cantidad']
        colors = [NUCLIO_COLORS['red'], NUCLIO_COLORS['orange'], NUCLIO_COLORS['yellow'],
                 NUCLIO_COLORS['green'], NUCLIO_COLORS['green_dark']]

        fig = go.Figure(data=[go.Bar(x=rating_dist['Rating'], y=rating_dist['Cantidad'],
                                    marker_color=colors, text=rating_dist['Cantidad'], textposition='outside')])
        fig.add_vline(x=3.5, line_dash="dash", line_color=NUCLIO_COLORS['black'], annotation_text="Umbral Satisfacción")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                         xaxis_title="Rating (estrellas)", yaxis_title="Cantidad de Reviews",
                         plot_bgcolor='white', paper_bgcolor='white')
        fig.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Tiempo de Entrega por Estado")
        state_delivery = df.groupby('estado').agg({'dias_entrega': 'mean', 'order_id': 'count'}).reset_index()
        state_delivery.columns = ['Estado', 'Días Promedio', 'Órdenes']
        state_delivery = state_delivery.nlargest(10, 'Órdenes')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=state_delivery['Estado'], y=state_delivery['Días Promedio'],
            marker_color=[NUCLIO_COLORS['green'] if d <= 7 else NUCLIO_COLORS['orange'] if d <= 14 else NUCLIO_COLORS['red']
                         for d in state_delivery['Días Promedio']],
            text=[f"{d:.1f}d" for d in state_delivery['Días Promedio']], textposition='outside'
        ))
        fig.add_hline(y=7, line_dash="dash", line_color=NUCLIO_COLORS['green'], annotation_text="Objetivo: 7 días")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                         xaxis_title="", yaxis_title="Días Promedio",
                         plot_bgcolor='white', paper_bgcolor='white')
        fig.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Análisis: Impacto del Tiempo de Entrega en el Rating")
    col1, col2 = st.columns([2, 1])

    with col1:
        df_temp = df.copy()
        df_temp['delivery_bin'] = pd.cut(df_temp['dias_entrega'], bins=[0, 7, 14, 21, 100],
                                        labels=['1-7 días\n(Rápido)', '8-14 días\n(Normal)',
                                               '15-21 días\n(Lento)', '>21 días\n(Muy lento)'])
        delivery_analysis = df_temp.groupby('delivery_bin', observed=True).agg({'rating': ['mean', 'count'], 'order_id': 'nunique'}).reset_index()
        delivery_analysis.columns = ['Rango', 'Rating Promedio', 'Total Reviews', 'Órdenes']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=delivery_analysis['Rango'], y=delivery_analysis['Rating Promedio'],
            marker_color=[NUCLIO_COLORS['green'], NUCLIO_COLORS['yellow'], NUCLIO_COLORS['orange'], NUCLIO_COLORS['red']],
            text=[f"{r:.2f}" for r in delivery_analysis['Rating Promedio']], textposition='outside'
        ))
        fig.add_hline(y=4.0, line_dash="dash", line_color=NUCLIO_COLORS['black'], annotation_text="Objetivo Rating: 4.0")
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20),
                         xaxis_title="Tiempo de Entrega", yaxis_title="Rating Promedio",
                         plot_bgcolor='white', paper_bgcolor='white', yaxis=dict(range=[0, 5]))
        fig.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="warning-box">
            <strong>Insight Clave:</strong><br><br>
            El gráfico muestra una <strong>correlación directa</strong> entre tiempo de entrega y satisfacción.<br><br>
            <strong>Recomendación:</strong> Priorizar reducir entregas >14 días para mejorar el rating global.
        </div>
        """, unsafe_allow_html=True)


def render_about_section():
    """Sección de información educativa mejorada"""
    st.markdown("## Guía Educativa del Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["Framework de KPIs", "Dashboard Personas", "Fichas Técnicas", "Dataset Olist"])

    with tab1:
        st.markdown("""
        ### Framework de KPIs para E-commerce

        Este dashboard implementa el framework de **árbol de KPIs** que conecta la estrategia
        de negocio con métricas accionables.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### Jerarquía del Árbol

            | Nivel | Descripción | Ejemplo |
            |-------|-------------|---------|
            | **North Star Metric** | Métrica principal que refleja el éxito del negocio | GMV |
            | **Objetivo** | Meta estratégica medible | +25% ingresos en 12 meses |
            | **Estrategia** | Camino para lograr el objetivo | Mejorar conversión |
            | **Táctica** | Acción concreta | Reducir fricción en checkout |
            | **KPI** | Métrica que mide el éxito de la táctica | Tasa de abandono carrito |
            """)

        with col2:
            st.markdown("""
            #### Stakeholders y sus KPIs

            | Rol | Enfoque | KPIs Principales |
            |-----|---------|------------------|
            | **CEO** | Estratégico | GMV, Órdenes, AOV, Clientes |
            | **CMO** | Marketing | CAC, Conversión, Recurrencia |
            | **COO** | Operaciones | Entrega, Rating, Satisfacción |
            """)

    with tab2:
        st.markdown("""
        ### ¿Qué es un Dashboard Persona?

        Un **Dashboard Persona** es un perfil ficticio pero realista que representa al usuario
        típico del dashboard. Ayuda a diseñar visualizaciones centradas en las necesidades reales.
        """)

        st.markdown("#### Componentes de un Dashboard Persona")
        st.markdown("""
        | Componente | Descripción | Ejemplo |
        |------------|-------------|---------|
        | **Nombre y Cargo** | Identidad del persona | Carlos Mendoza, CEO |
        | **Descripción** | Background profesional | 15 años en retail y e-commerce |
        | **Objetivos** | Qué quiere lograr | Maximizar GMV, asegurar crecimiento |
        | **Pain Points** | Problemas actuales | Falta de visión consolidada |
        | **Necesidades** | Qué necesita del dashboard | KPIs de alto nivel en una vista |
        | **Frecuencia** | Cuándo usa el dashboard | Diaria / Semanal |
        | **KPIs Principales** | Métricas que más le importan | GMV, Órdenes, AOV |
        """)

        st.markdown("---")
        st.markdown("#### Ejemplos de Dashboard Personas")
        col1, col2, col3 = st.columns(3)
        with col1:
            render_dashboard_persona('CEO')
        with col2:
            render_dashboard_persona('CMO')
        with col3:
            render_dashboard_persona('COO')

    with tab3:
        st.markdown("""
        ### Estructura de una Ficha Técnica de KPI

        Cada KPI debe documentarse con una **ficha técnica** que incluye 10 componentes esenciales:
        """)

        st.markdown("""
        | Componente | Descripción | Ejemplo |
        |------------|-------------|---------|
        | **Nombre del Indicador** | Nombre claro y descriptivo | GMV (Gross Merchandise Value) |
        | **Definición de Negocio** | Qué mide exactamente | Valor total de mercancías vendidas |
        | **Objetivo (Target)** | Meta numérica específica | Crecimiento del 25% anual |
        | **Frecuencia de Medición** | Cada cuánto se mide | Diaria / Semanal / Mensual |
        | **Fuente de Datos** | De dónde provienen los datos | Base de datos de órdenes |
        | **Fórmula Matemática** | Cálculo exacto | SUM(precio) de órdenes completadas |
        | **Unidad de Medida** | En qué se expresa | R$ (Reales) |
        | **Responsable** | Quién es accountable | CEO / Director Comercial |
        | **Tipo de KPI** | Clasificación | Estratégico / Táctico / Operativo |
        | **Relación con NSM** | Cómo impacta la North Star | Directo: ES la NSM |
        """)

        st.markdown("---")
        st.markdown("#### Ejemplo Completo: KPI Rating Promedio")
        render_ficha_tecnica('Rating_Promedio')

    with tab4:
        st.markdown("""
        ### Dataset de Olist

        El dataset proviene de **Olist**, una plataforma de e-commerce brasileña que conecta
        pequeños comercios con marketplaces.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### Variables Principales

            | Variable | Tipo | Descripción |
            |----------|------|-------------|
            | `order_id` | ID | Identificador único de orden |
            | `customer_id` | ID | Identificador de cliente |
            | `fecha` | Fecha | Fecha de la compra |
            | `estado` | Categórica | Estado de Brasil |
            | `categoria` | Categórica | Categoría del producto |
            | `precio` | Numérica | Precio del producto |
            | `dias_entrega` | Numérica | Días hasta la entrega |
            | `rating` | Numérica | Calificación 1-5 |
            | `metodo_pago` | Categórica | Forma de pago |
            """)

        with col2:
            st.markdown("""
            #### KPIs Calculables

            - **GMV**: Suma de precios
            - **AOV**: Promedio de precios
            - **Órdenes**: Conteo de order_id únicos
            - **Clientes**: Conteo de customer_id únicos
            - **Rating**: Promedio de calificaciones
            - **Tiempo Entrega**: Promedio de dias_entrega
            - **% Entregas Rápidas**: % con dias_entrega <= 7
            - **% Satisfechos**: % con rating >= 4
            """)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box">
        <strong>Siguiente paso:</strong> Usa este dashboard como referencia para crear
        el dashboard de tu proyecto siguiendo la misma estructura:<br><br>
        1. Define tu North Star Metric<br>
        2. Crea los Dashboard Personas de tus stakeholders<br>
        3. Diseña el árbol de KPIs<br>
        4. Documenta cada KPI con su ficha técnica<br>
        5. Diseña vistas por stakeholder
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================
def main():
    render_header()

    df = load_data()
    kpis = calculate_kpis(df)

    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 1rem;">
            <div style="width: 70px; height: 70px; background: {NUCLIO_COLORS['yellow']};
                        border-radius: 50%; margin: 0 auto 1rem; display: flex;
                        align-items: center; justify-content: center;
                        box-shadow: 0 4px 12px rgba(255,198,48,0.4);">
                <div style="width: 25px; height: 25px; background: {NUCLIO_COLORS['black']};
                            border-radius: 50%;"></div>
            </div>
            <h3 style="margin: 0; color: {NUCLIO_COLORS['white']}; font-weight: 700;">E-commerce Dashboard</h3>
            <p style="color: #CCCCCC; font-size: 0.85rem; margin-top: 0.5rem;">
                Dataset Olist - Brasil
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<p style='color: {NUCLIO_COLORS['yellow']}; font-weight: 600; margin-bottom: 0.5rem;'>FILTROS</p>", unsafe_allow_html=True)

        years = sorted(df['ano'].dropna().unique())
        selected_year = st.selectbox("Año", ["Todos"] + [int(y) for y in years])

        states = sorted(df['estado'].dropna().unique())
        selected_state = st.selectbox("Estado", ["Todos"] + list(states))

        categories = sorted(df['categoria'].dropna().unique())
        selected_category = st.selectbox("Categoría", ["Todas"] + list(categories))

        df_filtered = df.copy()
        if selected_year != "Todos":
            df_filtered = df_filtered[df_filtered['ano'] == selected_year]
        if selected_state != "Todos":
            df_filtered = df_filtered[df_filtered['estado'] == selected_state]
        if selected_category != "Todas":
            df_filtered = df_filtered[df_filtered['categoria'] == selected_category]

        kpis_filtered = calculate_kpis(df_filtered)

        st.markdown("---")
        st.markdown(f"<p style='color: {NUCLIO_COLORS['yellow']}; font-weight: 600;'>DATASET INFO</p>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem; margin-top: 0.5rem;">
            <div style="margin-bottom: 0.75rem;">
                <span style="color: #BBBBBB; font-size: 0.75rem; letter-spacing: 1px;">REGISTROS</span><br>
                <span style="color: {NUCLIO_COLORS['yellow']}; font-size: 1.5rem; font-weight: 700;">{len(df_filtered):,}</span>
            </div>
            <div>
                <span style="color: #BBBBBB; font-size: 0.75rem; letter-spacing: 1px;">PERÍODO</span><br>
                <span style="color: {NUCLIO_COLORS['white']}; font-size: 0.9rem; font-weight: 500;">{df_filtered['mes_nombre'].min()}<br>a {df_filtered['mes_nombre'].max()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Árbol de KPIs",
        "CEO Dashboard",
        "CMO Dashboard",
        "COO Dashboard",
        "Guía Educativa"
    ])

    with tab1:
        render_kpi_tree()
        st.markdown("""
        <div class="info-box">
            <strong>Cómo usar el árbol:</strong><br>
            El árbol de KPIs muestra la conexión entre la estrategia y las métricas operacionales.
            Cada dashboard de stakeholder (CEO, CMO, COO) muestra los KPIs relevantes para su rol,
            junto con la ficha técnica completa de cada indicador y el Dashboard Persona.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        render_ceo_dashboard(df_filtered, kpis_filtered)

    with tab3:
        render_cmo_dashboard(df_filtered, kpis_filtered)

    with tab4:
        render_coo_dashboard(df_filtered, kpis_filtered)

    with tab5:
        render_about_section()

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {NUCLIO_COLORS['gray_text']}; padding: 1.5rem;">
        <p style="margin-bottom: 0.5rem;">Dashboard desarrollado para <strong style="color: {NUCLIO_COLORS['yellow']};">Nuclio Digital School</strong></p>
        <p style="font-size: 0.8rem; margin: 0;">Módulo: Data Visualization & Analytics | Dataset: Olist Brazilian E-commerce</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem; color: {NUCLIO_COLORS['gray_medium']};">Learn <span style="color: {NUCLIO_COLORS['yellow']};">[to be]</span> the future</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
