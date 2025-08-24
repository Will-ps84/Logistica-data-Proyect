import pandas as pd
import plotly.express as px

# ====== Cargar dataset ======
df = pd.read_csv("data/ventas.csv")

# ====== Crear columna de venta total ======
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# ====== KPIs principales ======
ventas_totales = df["VentaTotal"].sum()
cantidad_total = df["Cantidad"].sum()
ticket_promedio = df["VentaTotal"].mean()
producto_mas_vendido = df.groupby("Producto")["Cantidad"].sum().idxmax()
cliente_top = df.groupby("Cliente")["VentaTotal"].sum().idxmax()

# ====== Mostrar KPIs ======
print("📊 Indicadores Logísticos Mejorados")
print(f"Ventas Totales: S/. {ventas_totales:,.2f}")
print(f"Cantidad Total de Productos Vendidos: {cantidad_total}")
print(f"Ticket Promedio: S/. {ticket_promedio:,.2f}")
print(f"Producto Más Vendido: {producto_mas_vendido}")
print(f"Cliente con Mayor Compra: {cliente_top}")

# ====== Gráficos interactivos ======
# Top 5 productos por cantidad
top_productos = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5)
fig_productos = px.bar(top_productos, x=top_productos.index, y=top_productos.values,
                       labels={"x": "Producto", "y": "Cantidad"},
                       title="Top 5 Productos Vendidos")
fig_productos.show()

# Top 5 clientes por ventas
top_clientes = df.groupby("Cliente")["VentaTotal"].sum().sort_values(ascending=False).head(5)
fig_clientes = px.bar(top_clientes, x=top_clientes.index, y=top_clientes.values,
                      labels={"x": "Cliente", "y": "Ventas"},
                      title="Top 5 Clientes por Ventas")
fig_clientes.show()

# Ventas por mes
df["Fecha"] = pd.to_datetime(df["Fecha"])
ventas_mes = df.groupby(df["Fecha"].dt.to_period("M"))["VentaTotal"].sum().reset_index()
ventas_mes["Fecha"] = ventas_mes["Fecha"].dt.to_timestamp()
fig_mes = px.line(ventas_mes, x="Fecha", y="VentaTotal", title="Ventas Mensuales")
fig_mes.show()
