#!/bin/bash
set -e

# Esperar a que PostgreSQL esté listo
until pg_isready -U nuclio -d ecommerce; do
  echo "Esperando a PostgreSQL..."
  sleep 2
done

echo "Cargando datos del CSV..."

# Cargar datos del CSV a la tabla ventas
psql -U nuclio -d ecommerce -c "\COPY ventas(order_id,order_item_id,customer_id,fecha,ano,mes,mes_nombre,dia_semana,estado,ciudad,categoria,peso_producto_g,precio,costo_envio,valor_total_pagado,metodo_pago,cuotas,estado_orden,dias_entrega,dias_retraso,rating) FROM '/docker-entrypoint-initdb.d/data.csv' WITH CSV HEADER DELIMITER ',';"

echo "Datos cargados exitosamente!"

# Mostrar conteo de registros
psql -U nuclio -d ecommerce -c "SELECT COUNT(*) as total_registros FROM ventas;"
