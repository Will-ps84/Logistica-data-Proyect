import pandas as pd
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import os

# ---------------------
# Cargar datos
# ---------------------
df = pd.read_csv("data/ventas.csv")

# Convertir columna Fecha a datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Extraer mes y año para filtros
df["Mes"] = df["Fecha"].dt.strftime("%Y-%m")

# Crear columna VentaTotal
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]

# ---------------------
# Inicializar app
# ---------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server  # para Render

# ---------------------
# Layout
# ---------------------
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard de Ventas", className="text-center text-primary mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona Cliente:"),
            dcc.Dropdown(
                id='filtro-cliente',
                options=[{'label': c, 'value': c} for c in sorted(df["Cliente"].unique())],
                value=None,
                placeholder="Todos los clientes"
            ),
        ], width=6),
        dbc.Col([
            html.Label("Selecciona Mes:"),
            dcc.Dropdown(
                id='filtro-mes',
                options=[{'label': m, 'value': m} for m in sorted(df["Mes"].unique())],
                value=None,
                placeholder="Todos los meses"
            ),
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-ventas-mes'), width=6),
        dbc.Col(dcc.Graph(id='grafico-ventas-cliente'), width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Listado de clientes y ventas totales", className="mt-4"),
            dash_table.DataTable(
                id='tabla-clientes',
                columns=[
                    {"name": "Cliente", "id": "Cliente"},
                    {"name": "Total Ventas", "id": "VentaTotal"}
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center'},
                page_size=10
            )
        ], width=12)
    ])
], fluid=True)

# ---------------------
# Callbacks
# ---------------------
@app.callback(
    [
        dash.dependencies.Output('grafico-ventas-mes', 'figure'),
        dash.dependencies.Output('grafico-ventas-cliente', 'figure'),
        dash.dependencies.Output('tabla-clientes', 'data')
    ],
    [
        dash.dependencies.Input('filtro-cliente', 'value'),
        dash.dependencies.Input('filtro-mes', 'value')
    ]
)
def actualizar_dashboard(cliente_seleccionado, mes_seleccionado):
    dff = df.copy()
    
    if cliente_seleccionado:
        dff = dff[dff["Cliente"] == cliente_seleccionado]
    if mes_seleccionado:
        dff = dff[dff["Mes"] == mes_seleccionado]
    
    # Ventas por mes
    ventas_mes = dff.groupby("Mes")["VentaTotal"].sum().reset_index()
    fig_mes = px.bar(ventas_mes, x="Mes", y="VentaTotal", text="VentaTotal", title="Ventas por Mes")
    
    # Ventas por cliente
    ventas_cliente = dff.groupby("Cliente")["VentaTotal"].sum().reset_index()
    fig_cliente = px.pie(ventas_cliente, names="Cliente", values="VentaTotal", title="Ventas por Cliente")
    
    # Tabla clientes
    tabla_data = ventas_cliente.to_dict('records')
    
    return fig_mes, fig_cliente, tabla_data

# ---------------------
# Run server
# ---------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
