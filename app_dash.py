# app_dash.py
import os
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# ====== Configuración de la app ======
app = Dash(__name__)
app.title = "Dashboard Logística"

# ====== Leer dataset ======
# Usar variable de entorno para la ruta del CSV, default local
dataset_path = os.getenv("DATA_PATH", "data/ventas.csv")
df = pd.read_csv(dataset_path)

# ====== Calcular KPIs ======
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

ventas_totales = df["VentaTotal"].sum()
cantidad_total = df["Cantidad"].sum()
ticket_promedio = df["VentaTotal"].mean()
producto_mas_vendido = df.groupby("Producto")["Cantidad"].sum().idxmax()
cliente_top = df.groupby("Cliente")["VentaTotal"].sum().idxmax()

# ====== Gráficos ======
# Top 5 productos por cantidad
top_productos = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5)
fig_productos = px.bar(top_productos, x=top_productos.index, y=top_productos.values,
                       labels={"x":"Producto", "y":"Cantidad"},
                       title="Top 5 Productos Vendidos")

# ====== Layout ======
app.layout = html.Div([
    html.H1("Dashboard Logística", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Ventas Totales"),
            html.P(f"S/. {ventas_totales:,.2f}")
        ], className="kpi"),
        html.Div([
            html.H3("Cantidad Total"),
            html.P(f"{cantidad_total}")
        ], className="kpi"),
        html.Div([
            html.H3("Ticket Promedio"),
            html.P(f"S/. {ticket_promedio:,.2f}")
        ], className="kpi"),
        html.Div([
            html.H3("Producto Más Vendido"),
            html.P(f"{producto_mas_vendido}")
        ], className="kpi"),
        html.Div([
            html.H3("Cliente Top"),
            html.P(f"{cliente_top}")
        ], className="kpi"),
    ], style={"display": "flex", "justifyContent": "space-around", "marginBottom": "50px"}),

    dcc.Graph(figure=fig_productos)
])

# ====== Run server ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Render asigna PORT
    app.run(host="0.0.0.0", port=port)
