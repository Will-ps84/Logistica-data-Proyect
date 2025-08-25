# app_dash.py
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os

# --- Cargar dataset ---
df = pd.read_csv("data/ventas.csv")
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# --- KPIs ---
total_ventas = df["VentaTotal"].sum()
promedio_ventas = df["VentaTotal"].mean()
venta_max = df["VentaTotal"].max()
venta_min = df["VentaTotal"].min()

# --- Ventas por cliente ---
ventas_cliente = df.groupby("Cliente")["VentaTotal"].sum().reset_index()
cliente_top = ventas_cliente.loc[ventas_cliente["VentaTotal"].idxmax(), "Cliente"]

# --- Ventas mes a mes ---
df["AñoMes"] = df["Fecha"].dt.to_period("M")
ventas_mes = df.groupby("AñoMes")["VentaTotal"].sum().reset_index()
ventas_mes["AñoMes"] = ventas_mes["AñoMes"].dt.to_timestamp()

# --- Gráficos ---
fig_ventas_mes = px.bar(
    ventas_mes, x="AñoMes", y="VentaTotal",
    title="Ventas Mensuales",
    text="VentaTotal"
)
fig_ventas_mes.update_layout(yaxis_title="Soles", xaxis_title="Mes")

fig_ventas_cliente = px.bar(
    ventas_cliente, x="Cliente", y="VentaTotal",
    title="Ventas por Cliente",
    text="VentaTotal"
)

# --- Dash App ---
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dashboard Logística", className="text-center mt-3"),
    
    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Ventas Totales"),
            dbc.CardBody(html.H4(f"S/. {total_ventas:,.2f}"))
        ], color="primary", inverse=True)),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Promedio por Venta"),
            dbc.CardBody(html.H4(f"S/. {promedio_ventas:,.2f}"))
        ], color="info", inverse=True)),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Venta Máxima"),
            dbc.CardBody(html.H4(f"S/. {venta_max:,.2f}"))
        ], color="success", inverse=True)),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Venta Mínima"),
            dbc.CardBody(html.H4(f"S/. {venta_min:,.2f}"))
        ], color="warning", inverse=True)),
    ], className="mb-4"),
    
    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_ventas_mes), md=6),
        dbc.Col(dcc.Graph(figure=fig_ventas_cliente), md=6),
    ]),
    
    html.Hr(),
    html.P(f"Cliente con mayores ventas: {cliente_top}", className="text-center")
], fluid=True)

# --- Ejecutar ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
