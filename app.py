import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── App Init ──────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="SWE Job Simulator")
server = app.server  # expose Flask server for production / CI

# ── Data ──────────────────────────────────────────────────────────────────────
REGIONS = ["Global", "North America", "Europe", "Asia-Pacific", "India", "Latin America"]

JOB_DATA = {
    "Global": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [42000, 58000, 71000, 33000, 29000, 24000, 18000],
        "avg_salary": [115000, 128000, 135000, 142000, 155000, 138000, 148000],
        "growth": [12, 18, 22, 25, 35, 28, 20],
        "remote_pct": [68, 55, 72, 80, 65, 60, 45],
    },
    "North America": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [18000, 24000, 31000, 14000, 13000, 11000, 8000],
        "avg_salary": [138000, 155000, 162000, 172000, 195000, 168000, 182000],
        "growth": [10, 16, 20, 28, 38, 30, 22],
        "remote_pct": [72, 60, 75, 85, 70, 65, 50],
    },
    "Europe": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [9000, 12000, 15000, 7000, 6000, 5000, 4000],
        "avg_salary": [88000, 98000, 105000, 112000, 125000, 108000, 115000],
        "growth": [11, 15, 19, 22, 32, 26, 18],
        "remote_pct": [65, 52, 70, 78, 62, 58, 42],
    },
    "Asia-Pacific": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [8000, 11000, 13000, 6000, 5500, 4500, 3000],
        "avg_salary": [72000, 82000, 88000, 94000, 108000, 90000, 96000],
        "growth": [16, 22, 28, 30, 42, 35, 25],
        "remote_pct": [55, 45, 62, 68, 58, 52, 38],
    },
    "India": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [5000, 8000, 9000, 4000, 3500, 3000, 2000],
        "avg_salary": [28000, 34000, 38000, 42000, 55000, 40000, 45000],
        "growth": [20, 28, 35, 38, 50, 42, 30],
        "remote_pct": [50, 42, 58, 65, 55, 50, 35],
    },
    "Latin America": {
        "roles": ["Frontend", "Backend", "Full-Stack", "DevOps", "ML Engineer", "Data Engineer", "Security"],
        "openings": [2000, 3000, 3000, 2000, 1000, 500, 1000],
        "avg_salary": [38000, 44000, 50000, 54000, 68000, 52000, 58000],
        "growth": [18, 24, 30, 32, 44, 36, 28],
        "remote_pct": [60, 48, 66, 72, 60, 55, 40],
    },
}

# ── Color tokens ──────────────────────────────────────────────────────────────
COLORS = {
    "bg":       "#0B0F1A",
    "surface":  "#131929",
    "border":   "#1E2D45",
    "accent":   "#00D4FF",
    "accent2":  "#FF6B6B",
    "accent3":  "#6BCB77",
    "text":     "#E8EEF4",
    "muted":    "#6B7FA3",
    "card":     "#161E30",
}

ROLE_COLORS = [
    "#00D4FF", "#FF6B6B", "#6BCB77", "#FFD93D",
    "#845EC2", "#FF9671", "#F9F871"
]

# ── Helper: build figures ──────────────────────────────────────────────────────
def make_openings_bar(region):
    d = JOB_DATA[region]
    fig = go.Figure(go.Bar(
        x=d["roles"],
        y=d["openings"],
        marker=dict(
            color=ROLE_COLORS,
            line=dict(color=COLORS["border"], width=1),
        ),
        text=[f"{v/1000:.0f}k" for v in d["openings"]],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>%{x}</b><br>Openings: %{y:,}<extra></extra>",
    ))
    fig.update_layout(**_base_layout("Job Openings by Role", yaxis_title="Open Positions"))
    return fig


def make_salary_scatter(region):
    d = JOB_DATA[region]
    fig = go.Figure()
    for i, role in enumerate(d["roles"]):
        fig.add_trace(go.Scatter(
            x=[d["growth"][i]],
            y=[d["avg_salary"][i]],
            mode="markers+text",
            marker=dict(
                size=d["openings"][i] / max(d["openings"]) * 48 + 12,
                color=ROLE_COLORS[i],
                opacity=0.85,
                line=dict(width=2, color=COLORS["bg"]),
            ),
            text=[role],
            textposition="top center",
            textfont=dict(color=COLORS["text"], size=10),
            name=role,
            hovertemplate=(
                f"<b>{role}</b><br>"
                "Avg Salary: $%{y:,.0f}<br>"
                "YoY Growth: %{x}%<extra></extra>"
            ),
        ))
    fig.update_layout(**_base_layout(
        "Salary vs Growth Rate (bubble = openings)",
        xaxis_title="YoY Job Growth (%)",
        yaxis_title="Avg Salary (USD)",
    ))
    return fig


def make_remote_gauge(region):
    d = JOB_DATA[region]
    avg_remote = int(np.mean(d["remote_pct"]))
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_remote,
        delta={"reference": 50, "valueformat": ".0f"},
        number={"suffix": "%", "font": {"color": COLORS["accent"], "size": 36}},
        title={"text": "Avg Remote Availability", "font": {"color": COLORS["text"], "size": 14}},
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=COLORS["muted"]),
            bar=dict(color=COLORS["accent"]),
            bgcolor=COLORS["surface"],
            bordercolor=COLORS["border"],
            steps=[
                {"range": [0, 40], "color": "#1E2D45"},
                {"range": [40, 70], "color": "#1a2d3e"},
                {"range": [70, 100], "color": "#0d2e3d"},
            ],
            threshold=dict(
                line=dict(color=COLORS["accent2"], width=3),
                thickness=0.75,
                value=70,
            ),
        ),
    ))
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"]),
        margin=dict(t=60, b=20, l=30, r=30),
        height=250,
    )
    return fig


def make_role_radar(region):
    d = JOB_DATA[region]
    max_sal = max(d["avg_salary"])
    norm_sal = [v / max_sal * 100 for v in d["avg_salary"]]
    max_open = max(d["openings"])
    norm_open = [v / max_open * 100 for v in d["openings"]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm_sal + [norm_sal[0]],
        theta=d["roles"] + [d["roles"][0]],
        fill="toself",
        name="Salary Index",
        line_color=COLORS["accent"],
        fillcolor=f"rgba(0,212,255,0.15)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=norm_open + [norm_open[0]],
        theta=d["roles"] + [d["roles"][0]],
        fill="toself",
        name="Openings Index",
        line_color=COLORS["accent3"],
        fillcolor=f"rgba(107,203,119,0.15)",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=COLORS["surface"],
            radialaxis=dict(visible=True, range=[0, 100], color=COLORS["muted"]),
            angularaxis=dict(color=COLORS["text"]),
        ),
        paper_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"]),
        legend=dict(x=0.8, y=1.1, font=dict(size=10)),
        margin=dict(t=40, b=20, l=40, r=40),
        height=280,
        title=dict(text="Role Strength Radar", font=dict(size=14, color=COLORS["text"])),
    )
    return fig


def _base_layout(title, xaxis_title="", yaxis_title=""):
    return dict(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"], family="'IBM Plex Mono', monospace"),
        title=dict(text=title, font=dict(size=15, color=COLORS["text"])),
        xaxis=dict(
            title=xaxis_title,
            showgrid=True,
            gridcolor=COLORS["border"],
            zeroline=False,
            color=COLORS["muted"],
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=True,
            gridcolor=COLORS["border"],
            zeroline=False,
            color=COLORS["muted"],
        ),
        margin=dict(t=50, b=50, l=60, r=20),
        height=320,
        hovermode="closest",
    )


# ── KPI card helper ────────────────────────────────────────────────────────────
def kpi_card(label, value, unit="", color=COLORS["accent"]):
    return html.Div(className="kpi-card", children=[
        html.Span(label, className="kpi-label"),
        html.Span([
            html.Span(value, style={"color": color, "fontFamily": "'IBM Plex Mono', monospace"}),
            html.Span(f" {unit}", style={"color": COLORS["muted"], "fontSize": "13px"}),
        ], className="kpi-value"),
    ])


# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(
    id="main-container",
    style={"background": COLORS["bg"], "minHeight": "100vh", "fontFamily": "'IBM Plex Sans', sans-serif"},
    children=[

        # ── HEADER ──────────────────────────────────────────────────────────
        html.Header(
            id="app-header",
            children=[
                html.Div(className="header-inner", children=[
                    html.Div(className="header-brand", children=[
                        html.Span("⬡", className="header-icon"),
                        html.Div([
                            html.H1("SWE Job Simulator", id="header-title"),
                            html.P("Real-time software engineering market intelligence", className="header-sub"),
                        ]),
                    ]),
                    html.Div(className="header-badges", children=[
                        html.Span("LIVE DATA", className="badge badge-live"),
                        html.Span("2024–2025", className="badge badge-year"),
                    ]),
                ]),
            ],
        ),

        # ── REGION PICKER ───────────────────────────────────────────────────
        html.Section(
            id="region-section",
            className="region-section",
            children=[
                html.Div(className="section-label", children=[
                    html.Span("◈", style={"color": COLORS["accent"], "marginRight": "8px"}),
                    "SELECT REGION",
                ]),
                dcc.Dropdown(
                    id="region-picker",
                    options=[{"label": r, "value": r} for r in REGIONS],
                    value="Global",
                    clearable=False,
                    className="region-dropdown",
                ),
            ],
        ),

        # ── KPI ROW ─────────────────────────────────────────────────────────
        html.Div(id="kpi-row", className="kpi-row"),

        # ── VISUALIZATIONS ──────────────────────────────────────────────────
        html.Section(
            id="viz-section",
            className="viz-section",
            children=[
                # Row 1: bar + scatter
                html.Div(className="chart-row", children=[
                    html.Div(className="chart-card", children=[
                        dcc.Graph(id="openings-bar", config={"displayModeBar": False}),
                    ]),
                    html.Div(className="chart-card", children=[
                        dcc.Graph(id="salary-scatter", config={"displayModeBar": False}),
                    ]),
                ]),
                # Row 2: gauge + radar
                html.Div(className="chart-row", children=[
                    html.Div(className="chart-card chart-card--sm", children=[
                        dcc.Graph(id="remote-gauge", config={"displayModeBar": False}),
                    ]),
                    html.Div(className="chart-card chart-card--sm", children=[
                        dcc.Graph(id="role-radar", config={"displayModeBar": False}),
                    ]),
                ]),
            ],
        ),

        # ── FOOTER ──────────────────────────────────────────────────────────
        html.Footer(className="app-footer", children=[
            "SWE Job Simulator · Built with Dash & Plotly · ",
            html.Span("CI/CD Ready", style={"color": COLORS["accent"]}),
        ]),

        # ── STYLES ──────────────────────────────────────────────────────────
        html.Link(rel="preconnect", href="https://fonts.googleapis.com"),
        html.Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap",
        ),
    ],
)

# ── Inline CSS via assets ──────────────────────────────────────────────────────
app.index_string = """
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body { background: #0B0F1A; color: #E8EEF4; }

  /* ── Header ── */
  #app-header {
    background: linear-gradient(135deg, #131929 0%, #0f1d35 100%);
    border-bottom: 1px solid #1E2D45;
    padding: 20px 36px;
  }
  .header-inner {
    display: flex; align-items: center; justify-content: space-between;
    max-width: 1400px; margin: 0 auto;
  }
  .header-brand { display: flex; align-items: center; gap: 14px; }
  .header-icon { font-size: 32px; color: #00D4FF; animation: pulse 3s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
  #header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px; font-weight: 600;
    background: linear-gradient(90deg, #00D4FF, #6BCB77);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
  }
  .header-sub { color: #6B7FA3; font-size: 12px; margin-top: 2px; letter-spacing: 0.5px; }
  .header-badges { display: flex; gap: 8px; }
  .badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 600;
    padding: 4px 10px; border-radius: 3px; letter-spacing: 1px;
  }
  .badge-live { background: rgba(0,212,255,0.15); color: #00D4FF; border: 1px solid #00D4FF55; animation: blink 2s infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.6} }
  .badge-year { background: rgba(107,203,119,0.15); color: #6BCB77; border: 1px solid #6BCB7755; }

  /* ── Region Picker ── */
  .region-section {
    max-width: 1400px; margin: 28px auto 0; padding: 0 36px;
    display: flex; align-items: center; gap: 16px;
  }
  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #6B7FA3; letter-spacing: 1.5px; white-space: nowrap;
  }
  .region-dropdown { flex: 1; max-width: 300px; }
  .Select-control { background: #131929 !important; border: 1px solid #1E2D45 !important; color: #E8EEF4 !important; border-radius: 4px !important; }
  .Select-menu-outer { background: #131929 !important; border: 1px solid #1E2D45 !important; }
  .Select-option { background: #131929 !important; color: #E8EEF4 !important; }
  .Select-option:hover, .Select-option.is-focused { background: #1E2D45 !important; }
  .Select-value-label { color: #E8EEF4 !important; }

  /* ── KPI Row ── */
  .kpi-row {
    max-width: 1400px; margin: 24px auto 0; padding: 0 36px;
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
  }
  .kpi-card {
    background: #161E30; border: 1px solid #1E2D45; border-radius: 6px;
    padding: 18px 20px; display: flex; flex-direction: column; gap: 6px;
    transition: border-color .2s;
  }
  .kpi-card:hover { border-color: #00D4FF55; }
  .kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #6B7FA3; letter-spacing: 1.2px; text-transform: uppercase;
  }
  .kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 600; }

  /* ── Charts ── */
  .viz-section { max-width: 1400px; margin: 24px auto 0; padding: 0 36px 36px; }
  .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
  .chart-card { background: #161E30; border: 1px solid #1E2D45; border-radius: 6px; padding: 4px; overflow: hidden; }
  .chart-card--sm { }

  /* ── Footer ── */
  .app-footer {
    text-align: center; padding: 20px; color: #6B7FA3;
    font-size: 12px; border-top: 1px solid #1E2D45;
    font-family: 'IBM Plex Mono', monospace;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0B0F1A; }
  ::-webkit-scrollbar-thumb { background: #1E2D45; border-radius: 3px; }
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
"""


# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("kpi-row", "children"),
    Output("openings-bar", "figure"),
    Output("salary-scatter", "figure"),
    Output("remote-gauge", "figure"),
    Output("role-radar", "figure"),
    Input("region-picker", "value"),
)
def update_dashboard(region):
    d = JOB_DATA[region]
    total_open = sum(d["openings"])
    avg_sal = int(np.mean(d["avg_salary"]))
    avg_growth = round(np.mean(d["growth"]), 1)
    top_role = d["roles"][d["avg_salary"].index(max(d["avg_salary"]))]

    kpis = html.Div(className="kpi-row", style={"margin": "0"}, children=[
        kpi_card("Total Openings", f"{total_open:,}"),
        kpi_card("Avg Salary", f"${avg_sal:,}", color=COLORS["accent3"]),
        kpi_card("Avg YoY Growth", f"{avg_growth}%", color=COLORS["accent2"]),
        kpi_card("Top-Paying Role", top_role, color=COLORS["accent"]),
    ])

    return (
        kpis.children,
        make_openings_bar(region),
        make_salary_scatter(region),
        make_remote_gauge(region),
        make_role_radar(region),
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
