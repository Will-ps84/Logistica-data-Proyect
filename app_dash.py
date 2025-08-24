import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# ====== Leer dataset ======
df = pd.read_csv("data/ventas.csv")
df["VentaTotal"] = df["Cantidad"] * df["PrecioUnitario"]
df["Fecha"] = pd.to_datetime(df["Fecha"])

# ====== Inicializar app Dash con Bootstrap ======
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Logística K-J-W"

# ====== Layout ======
app.layout = dbc.Container([
    html.H1("📊 Dashboard Logística K-J-W Data Project", className="text-center my-4"),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona Producto(s):"),
            dcc.Dropdown(
                id="producto-dropdown",
                options=[{"label": p, "value": p} for p in sorted(df["Producto"].unique())],
                multi=True,
                value=[]
            )
        ], width=6),
        dbc.Col([
            html.Label("Selecciona Rango de Fecha:"),
            dcc.DatePickerRange(
                id="fecha-range",
                start_date=df["Fecha"].min(),
                end_date=df["Fecha"].max(),
                display_format="YYYY-MM-DD"
            )
        ], width=6)
    ], className="mb-4"),
    
    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card(id="ventas-totales", body=True, className="text-center"), width=2),
        dbc.Col(dbc.Card(id="cantidad-total", body=True, className="text-center"), width=2),
        dbc.Col(dbc.Card(id="ticket-promedio", body=True, className="text-center"), width=2),
        dbc.Col(dbc.Card(id="producto-top", body=True, className="text-center"), width=3),
        dbc.Col(dbc.Card(id="cliente-top", body=True, className="text-center"), width=3),
    ], className="mb-4"),
    
    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-productos"), width=6),
        dbc.Col(dcc.Graph(id="grafico-clientes"), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-ventas-mes"), width=12),
    ])
], fluid=True)

# ====== Callbacks ======
@app.callback(
    [
        Output("ventas-totales", "children"),
        Output("cantidad-total", "children"),
        Output("ticket-promedio", "children"),
        Output("producto-top", "children"),
        Output("cliente-top", "children"),
        Output("grafico-productos", "figure"),
        Output("grafico-clientes", "figure"),
        Output("grafico-ventas-mes", "figure"),
    ],
    [
        Input("producto-dropdown", "value"),
        Input("fecha-range", "start_date"),
        Input("fecha-range", "end_date")
    ]
)
def actualizar_dashboard(productos_seleccionados, fecha_inicio, fecha_fin):
    # Filtrar datos
    dff = df.copy()
    if productos_seleccionados:
        dff = dff[dff["Producto"].isin(productos_seleccionados)]
    dff = dff[(dff["Fecha"] >= fecha_inicio) & (dff["Fecha"] <= fecha_fin)]
    
    # KPIs
    ventas_totales = f"💰 Ventas Totales\nS/. {dff['VentaTotal'].sum():,.2f}"
    cantidad_total = f"📦 Cantidad Total\n{dff['Cantidad'].sum()}"
    ticket_promedio = f"📊 Ticket Promedio\nS/. {dff['VentaTotal'].mean():,.2f}"
    producto_top = f"🏆 Producto Top\n{dff.groupby('Producto')['Cantidad'].sum().idxmax() if not dff.empty else 'N/A'}"
    cliente_top = f"👤 Cliente Top\n{dff.groupby('Cliente')['VentaTotal'].sum().idxmax() if not dff.empty else 'N/A'}"
    
    # Gráficos
    top_productos = dff.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5)
    fig_productos = px.bar(top_productos, x=top_productos.index, y=top_productos.values,
                           labels={"x": "Producto", "y": "Cantidad"},
                           title="Top 5 Productos Vendidos")
    
    top_clientes = dff.groupby("Cliente")["VentaTotal"].sum().sort_values(ascending=False).head(5)
    fig_clientes = px.bar(top_clientes, x=top_clientes.index, y=top_clientes.values,
                          labels={"x": "Cliente", "y": "Ventas"},
                          title="Top 5 Clientes por Ventas")
    
    ventas_mes = dff.groupby(dff["Fecha"].dt.to_period("M"))["VentaTotal"].sum().reset_index()
    ventas_mes["Fecha"] = ventas_mes["Fecha"].dt.to_timestamp()
    fig_mes = px.line(ventas_mes, x="Fecha", y="VentaTotal", title="Ventas Mensuales")
    
    return ventas_totales, cantidad_total, ticket_promedio, producto_top, cliente_top, fig_productos, fig_clientes, fig_mes

# ====== Ejecutar app ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
