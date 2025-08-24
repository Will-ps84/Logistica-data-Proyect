import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Cargar datos
df = pd.read_csv("data/ventas.csv")
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# Crear la app Dash
app = Dash(__name__)
app.title = "Logística Data Project"

# Gráficos con Plotly
fig_ventas_producto = px.bar(df.groupby("Producto")["Cantidad"].sum().reset_index(),
                             x="Producto", y="Cantidad", title="Ventas por Producto")

fig_ventas_cliente = px.bar(df.groupby("Cliente")["VentaTotal"].sum().reset_index().sort_values(by="VentaTotal", ascending=False).head(10),
                            x="Cliente", y="VentaTotal", title="Top 10 Clientes por Ventas")

fig_ventas_tiempo = px.line(df.groupby("Fecha")["VentaTotal"].sum().reset_index(),
                            x="Fecha", y="VentaTotal", title="Tendencia de Ventas Diarias")

# Layout
app.layout = html.Div([
    html.H1("📊 Logística Data Project", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("Ventas Totales"),
            html.P(f"S/ {df['VentaTotal'].sum():,.2f}")
        ], style={'width': '30%', 'display':'inline-block'}),
        
        html.Div([
            html.H3("Cantidad Total Vendida"),
            html.P(f"{df['Cantidad'].sum()}")
        ], style={'width': '30%', 'display':'inline-block'}),
        
        html.Div([
            html.H3("Ticket Promedio"),
            html.P(f"S/ {df['VentaTotal'].mean():,.2f}")
        ], style={'width': '30%', 'display':'inline-block'})
    ], style={'textAlign': 'center'}),

    html.Hr(),

    dcc.Graph(figure=fig_ventas_producto),
    dcc.Graph(figure=fig_ventas_cliente),
    dcc.Graph(figure=fig_ventas_tiempo)
])

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
import os
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Logística"),
    # tus gráficos y KPIs aquí
])

if __name__ == "__main__":
    # Obtener puerto asignado por Render
    port = int(os.environ.get("PORT", 8050))  # usa 8050 por defecto local
    app.run(host="0.0.0.0", port=port)
