import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os

# Cargar dataset
df = pd.read_csv("data/ventas.csv")
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]
df["AñoMes"] = df["Fecha"].dt.to_period("M").astype(str)

# Inicializar app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout interactivo
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard Interactivo de Ventas", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona Cliente:"),
            dcc.Dropdown(
                id="dropdown-cliente",
                options=[{"label": c, "value": c} for c in sorted(df["Cliente"].unique())],
                multi=True,
                placeholder="Todos los clientes"
            ),
        ], width=4),
        dbc.Col([
            html.Label("Selecciona Producto:"),
            dcc.Dropdown(
                id="dropdown-producto",
                options=[{"label": p, "value": p} for p in sorted(df["Producto"].unique())],
                multi=True,
                placeholder="Todos los productos"
            ),
        ], width=4),
        dbc.Col([
            html.Label("Rango de fechas:"),
            dcc.DatePickerRange(
                id="date-picker",
                start_date=df["Fecha"].min(),
                end_date=df["Fecha"].max()
            ),
        ], width=4)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graf-ventas-mes"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graf-top-clientes"), width=6),
        dbc.Col(dcc.Graph(id="graf-top-productos"), width=6)
    ])
], fluid=True)

# Callback para actualizar gráficos según filtros
@app.callback(
    Output("graf-ventas-mes", "figure"),
    Output("graf-top-clientes", "figure"),
    Output("graf-top-productos", "figure"),
    Input("dropdown-cliente", "value"),
    Input("dropdown-producto", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_graphs(clientes, productos, start_date, end_date):
    dff = df.copy()
    
    # Filtrar por cliente
    if clientes:
        dff = dff[dff["Cliente"].isin(clientes)]
    
    # Filtrar por producto
    if productos:
        dff = dff[dff["Producto"].isin(productos)]
    
    # Filtrar por fechas
    dff = dff[(dff["Fecha"] >= pd.to_datetime(start_date)) & (dff["Fecha"] <= pd.to_datetime(end_date))]

    # Ventas mes a mes
    ventas_mes = dff.groupby("AñoMes")["VentaTotal"].sum().reset_index()
    fig_ventas_mes = px.bar(ventas_mes, x="AñoMes", y="VentaTotal", title="Ventas Mes a Mes")

    # Top clientes
    top_cliente = dff.groupby("Cliente")["VentaTotal"].sum().sort_values(ascending=False).reset_index().head(5)
    fig_top_cliente = px.bar(top_cliente, x="Cliente", y="VentaTotal", title="Top Clientes")

    # Top productos
    top_producto = dff.groupby("Producto")["VentaTotal"].sum().sort_values(ascending=False).reset_index().head(5)
    fig_top_producto = px.bar(top_producto, x="Producto", y="VentaTotal", title="Top Productos")

    return fig_ventas_mes, fig_top_cliente, fig_top_producto

# Puerto dinámico para Render
port = int(os.environ.get("PORT", 8050))
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render asigna el puerto dinámicamente
    app.run_server(debug=True, host="0.0.0.0", port=port)
