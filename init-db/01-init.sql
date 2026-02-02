-- Crear base de datos para Metabase
CREATE DATABASE metabase;

-- Crear tabla de ventas en la base de datos ecommerce
\c ecommerce;

CREATE TABLE IF NOT EXISTS ventas (
    order_id VARCHAR(50),
    order_item_id DECIMAL(10,2),
    customer_id VARCHAR(50),
    fecha DATE,
    ano INTEGER,
    mes INTEGER,
    mes_nombre VARCHAR(20),
    dia_semana VARCHAR(20),
    estado VARCHAR(10),
    ciudad VARCHAR(100),
    categoria VARCHAR(100),
    peso_producto_g DECIMAL(10,2),
    precio DECIMAL(10,2),
    costo_envio DECIMAL(10,2),
    valor_total_pagado DECIMAL(10,2),
    metodo_pago VARCHAR(50),
    cuotas DECIMAL(10,2),
    estado_orden VARCHAR(50),
    dias_entrega DECIMAL(10,2),
    dias_retraso DECIMAL(10,2),
    rating DECIMAL(10,2)
);

-- Crear índices para mejor rendimiento
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_estado ON ventas(estado);
CREATE INDEX idx_ventas_categoria ON ventas(categoria);
CREATE INDEX idx_ventas_ano ON ventas(ano);
CREATE INDEX idx_ventas_ciudad ON ventas(ciudad);
