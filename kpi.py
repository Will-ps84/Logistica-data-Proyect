import pandas as pd

# Cargar dataset
df = pd.read_csv("data/ventas.csv")

# Eliminar espacios en nombres de columnas
df.columns = df.columns.str.strip()

df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# KPIs
ventas_totales = df["VentaTotal"].sum()
cantidad_total = df["Cantidad"].sum()
ticket_promedio = df["VentaTotal"].mean()
producto_mas_vendido = df.groupby("Producto")["Cantidad"].sum().idxmax()
cliente_top = df.groupby("Cliente")["VentaTotal"].sum().idxmax()

# Resultados
print("📊 Indicadores Logísticos")
print(f"Ventas Totales: S/ {ventas_totales:.2f}")
print(f"Cantidad Total de Productos Vendidos: {cantidad_total}")
print(f"Ticket Promedio por Venta: S/ {ticket_promedio:.2f}")
print(f"Producto más vendido: {producto_mas_vendido}")
print(f"Cliente con mayor compra: {cliente_top}")

