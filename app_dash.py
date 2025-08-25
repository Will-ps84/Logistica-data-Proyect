import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import os

# Cargar dataset
df = pd.read_csv("data/ventas.csv")

# Crear columna de Venta Total
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# Preparar indicadores
total_ventas = df["VentaTotal"].sum()
promedio_venta = df["VentaTotal"].mean()
max_venta = df["VentaTotal"].max()
min_venta = df["VentaTotal"].min()

# Ventas por cliente
ventas_cliente = df.groupby("Cliente")["VentaTotal"].sum().reset_index()

# Ventas mes a mes
df["Fecha"] = pd.to_datetime(df["Fecha"])
ventas_mes = df.groupby(df["Fecha"].dt.to_period("M"))["VentaTotal"].sum().reset_index()
ventas_mes["Fecha"] = ventas_mes["Fecha"].dt.to_timestamp()

# Gráfico ventas mensuales
fig_mes = px.bar(ventas_mes, x="Fecha", y="VentaTotal", title="Ventas Mes a Mes")

# Gráfico ventas por cliente
fig_cliente = px.bar(ventas_cliente, x="Cliente", y="VentaTotal", title="Ventas por Cliente")

# Inicializar app
app = Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1("Dashboard de Ventas", style={"textAlign": "center"}),
    
    html.Div([
        html.Div([
            html.H3("Total Ventas"),
            html.P(f"S/. {total_ventas:,.2f}")
        ], style={"width": "24%", "display": "inline-block", "textAlign": "center", "border": "1px solid #ccc", "padding": "10px"}),
        
        html.Div([
            html.H3("Promedio Venta"),
            html.P(f"S/. {promedio_venta:,.2f}")
        ], style={"width": "24%", "display": "inline-block", "textAlign": "center", "border": "1px solid #ccc", "padding": "10px"}),
        
        html.Div([
            html.H3("Máxima Venta"),
            html.P(f"S/. {max_venta:,.2f}")
        ], style={"width": "24%", "display": "inline-block", "textAlign": "center", "border": "1px solid #ccc", "padding": "10px"}),
        
        html.Div([
            html.H3("Mínima Venta"),
            html.P(f"S/. {min_venta:,.2f}")
        ], style={"width": "24%", "display": "inline-block", "textAlign": "center", "border": "1px solid #ccc", "padding": "10px"}),
    ], style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"}),
    
    dcc.Graph(figure=fig_mes),
    dcc.Graph(figure=fig_cliente)
])

# Puerto dinámico para Render
port = int(os.environ.get("PORT", 8050))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
