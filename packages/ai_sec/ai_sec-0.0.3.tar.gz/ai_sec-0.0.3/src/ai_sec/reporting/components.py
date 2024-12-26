import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table, dcc, html


def create_header(title="Dashboard"):
    return dbc.Navbar(
        dbc.Container(
            dbc.NavbarBrand(
                title,  # Use the dynamic title here
                id="navbar-title",  # Add this ID to update dynamically
                className="navbar-title",
                style={
                    "fontSize": "28px",
                    "color": "#ffffff",
                    "padding": "8px 20px",
                    "borderRadius": "10px",
                },
            ),
            fluid=True,
            className="d-flex justify-content-center",
        ),
        color="primary",
        dark=True,
        style={
            "width": "100%",
            "background": "linear-gradient(90deg, #4A90E2, #1464F6)",
            "padding": "15px 0",
            "boxShadow": "0px 4px 12px rgba(0, 0, 0, 0.2)",
        },
        sticky="top",
    )


def create_footer():
    return html.Footer(
        html.Div(
            [
                html.Span(
                    "darrenrabbitt.com | All rights reserved | v1.2.5",
                    className="footer-text",
                )
            ],
            className="footer-container",
        )
    )


def create_sidebar(linter_data, current_path):
    enabled_linters = list(set([entry["Linter"] for entry in linter_data]))

    links = [
        dbc.NavLink(
            linter,
            href=f"/{linter.lower()}",
            active="exact" if f"/{linter.lower()}" == current_path else "",
            className=(
                "nav-link"
                if f"/{linter.lower()}" != current_path
                else "nav-link active"
            ),
        )
        for linter in enabled_linters
    ]

    return html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/logo.webp", className="logo"),
                    html.H2("AI_SEC", className="sidebar-title"),
                ],
                className="logo-container",
            ),
            html.Div(
                dbc.NavLink(
                    html.Img(src="/assets/home-solid.svg", className="home-icon"),
                    href="/",
                    active="exact" if current_path == "/" else "",
                    className="home-link",
                )
            ),
            html.Hr(className="sidebar-hr"),
            dbc.Nav(links, vertical=True, pills=True, className="sidebar-nav"),
        ],
        className="sidebar",
        id="sidebar-wrapper",
        style={
            "width": "220px",  # Ensure this width aligns with the CSS settings
            "position": "sticky",
            "top": "0",
            "height": "100vh",
            "overflowY": "auto",
        },
    )


def create_summary_card(title, count, color, icon_class):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.I(
                            className=icon_class,
                            style={"color": color, "fontSize": "24px"},
                        ),
                        html.H4(
                            title,
                            className="card-title",
                            style={
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "marginLeft": "10px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                ),
                html.H2(
                    f"{count}",
                    style={"fontSize": "36px", "textAlign": "center", "color": color},
                ),
            ]
        ),
        className="shadow-sm mb-4",
        style={"borderRadius": "15px", "padding": "20px"},
    )


def create_data_table(df, columns):
    """Generate a Dash DataTable with conditional styling."""
    return dash_table.DataTable(
        id="linting-table",
        columns=columns,
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto", "overflowY": "auto", "minWidth": "100%"},
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "textAlign": "left",
            "padding": "8px",
            "minWidth": "70px",
            "maxWidth": "200px",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
        },
        style_data_conditional=[
            {"if": {"column_id": "Line"}, "width": "85px", "textAlign": "center"},
            {"if": {"column_id": "File"}, "minWidth": "150px", "maxWidth": "250px"},
            {"if": {"column_id": "Severity"}, "width": "80px", "textAlign": "center"},
            {
                "if": {"column_id": "Description"},
                "minWidth": "200px",
                "maxWidth": "300px",
                "wordWrap": "break-word",
            },
            {
                "if": {"column_id": "Links"},
                "minWidth": "200px",
                "maxWidth": "300px",
                "whiteSpace": "normal",
                "wordWrap": "break-word",
            },
            {
                "if": {"filter_query": '{Severity} = "CRITICAL"'},
                "backgroundColor": "#FF4136",
                "color": "white",
            },
            {
                "if": {"filter_query": '{Severity} = "HIGH"'},
                "backgroundColor": "#FF851B",
                "color": "white",
            },
            {
                "if": {"filter_query": '{Severity} = "MEDIUM"'},
                "backgroundColor": "#FFDC00",
                "color": "black",
            },
            {
                "if": {"filter_query": '{Severity} = "LOW"'},
                "backgroundColor": "#01FF70",
                "color": "black",
            },
            {
                "if": {"filter_query": '{Context} = "PASSED"'},
                "backgroundColor": "#2ECC40",
                "color": "white",
            },
        ],
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            "fontWeight": "bold",
            "textAlign": "center",
        },
        style_data={"whiteSpace": "normal", "height": "auto", "wordWrap": "break-word"},
    )


def create_issue_summary(total_issues, passed_issues, unknown_issues, pass_percentage):
    """Generate a summary section with cards for total, passed, unknown issues, and pass percentage."""
    return dbc.Row(
        [
            dbc.Col(
                create_card("Total Issues", total_issues, "#343a40"),
                xs=12,
                sm=6,
                md=3,
                className="mb-4",
            ),
            dbc.Col(
                create_card(
                    "Passed", passed_issues, "#2ECC40", "bi bi-check-circle-fill"
                ),
                xs=12,
                sm=6,
                md=3,
                className="mb-4",
            ),
            dbc.Col(
                create_card(
                    "Unknown",
                    unknown_issues,
                    "#FF851B",
                    "bi bi-exclamation-circle-fill",
                ),
                xs=12,
                sm=6,
                md=3,
                className="mb-4",
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "Pass Percentage",
                                className="card-title",
                                style={"fontWeight": "bold", "textAlign": "center"},
                            ),
                            dbc.Progress(
                                value=pass_percentage,
                                color="info",
                                className="mb-3",
                                style={"height": "20px"},
                            ),
                            html.H5(
                                f"{pass_percentage:.2f}% ({passed_issues}/{total_issues})",
                                style={
                                    "fontSize": "20px",
                                    "textAlign": "center",
                                    "color": "#0074D9",
                                },
                            ),
                        ]
                    ),
                    className="shadow-sm mb-4",
                    style={"borderRadius": "15px", "padding": "20px"},
                ),
                xs=12,
                sm=6,
                md=3,
                className="mb-4",
            ),
        ],
        className="justify-content-center",
    )


def create_modal():
    """Generate a modal for displaying detailed context information."""
    return dbc.Modal(
        [
            dbc.ModalHeader("Details"),
            dbc.ModalBody(id="modal-body"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ml-auto", n_clicks=0)
            ),
        ],
        id="context-modal",
        size="lg",
        is_open=False,
    )


def create_pie_chart(df, column, title):
    """Generate a Pie Chart for the given data and column."""
    fig = px.pie(df, names=column, title=title)
    fig.update_layout(
        title_x=0.5,
        title_font=dict(
            size=22, family="Open Sans, sans-serif", color="rgb(42, 63, 95)"
        ),
        margin=dict(t=50),
    )
    return dcc.Graph(
        figure=fig, style={"width": "60%", "margin": "0 auto", "paddingBottom": "20px"}
    )


def create_card(title, value, color, icon_class=None):
    card_body = [
        html.Div(
            [
                (
                    html.I(
                        className=icon_class, style={"color": color, "fontSize": "24px"}
                    )
                    if icon_class
                    else None
                ),
                html.H4(
                    title,
                    className="card-title",
                    style={
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "marginLeft": "10px" if icon_class else "0px",
                    },
                ),
            ],
            style=(
                {"display": "flex", "alignItems": "center", "justifyContent": "center"}
                if icon_class
                else {}
            ),
        ),
        html.H2(
            f"{value}",
            style={"fontSize": "36px", "textAlign": "center", "color": color},
        ),
    ]
    return dbc.Card(
        dbc.CardBody(card_body),
        className="shadow-sm mb-4",
        style={"borderRadius": "15px", "padding": "20px", "width": "100%"},
    )
