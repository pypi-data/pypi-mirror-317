import logging

import dash
import dash_bootstrap_components as dbc  # Import Dash Bootstrap Components
from dash import Input, Output, State, html

from ai_sec.reporting.app_layout import render_home_page, render_linter_page

logger = logging.getLogger(__name__)


def register_callbacks(app, linter_data):
    """
    Register callbacks to handle modal functionality and dynamic content in the dashboard.
    """

    # Callback to handle modal open/close and content rendering
    @app.callback(
        [
            Output("context-modal", "is_open"),
            Output("modal-body", "children"),
            Output("linting-table", "active_cell"),
        ],
        [Input("linting-table", "active_cell"), Input("close-modal", "n_clicks")],
        [State("linting-table", "data"), State("context-modal", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_modal(active_cell, n_clicks_close, table_data, is_open):
        """
        Handle modal toggle based on user actions (click on table or close modal).
        """
        try:
            ctx = dash.callback_context
            if ctx.triggered[0]["prop_id"] == "close-modal.n_clicks":
                return False, "", None

            if active_cell:
                row_index = active_cell["row"]
                if row_index < len(table_data):
                    linter_entry = table_data[row_index]

                    # Fetch description, links, context, and resource for additional context
                    description = linter_entry.get(
                        "Description", "No details available."
                    )
                    links = linter_entry.get("Links", [])
                    context = linter_entry.get(
                        "Context", "No additional context available."
                    )
                    resource = linter_entry.get(
                        "Additional Context", None
                    )  # Set to None if unavailable

                    # Process links for display as clickable elements
                    if isinstance(links, str):
                        links = [link.strip() for link in links.split(",")]

                    link_elements = []
                    for link in links:
                        if link:
                            link_elements.append(
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-link",
                                            style={"marginRight": "5px"},
                                        ),
                                        html.A(
                                            href=link,
                                            children=link,
                                            target="_blank",
                                            style={
                                                "color": "#3399f3",
                                                "wordWrap": "break-word",
                                            },
                                        ),
                                    ],
                                    className="modal-link-item",
                                )
                            )

                    # Build the modal content with the conditional Resource
                    modal_content = html.Div(
                        [
                            html.P(description, className="modal-description"),
                            (
                                html.P(
                                    f"Resource: {resource}", className="modal-resource"
                                )
                                if resource
                                else None
                            ),
                            html.P(context, className="modal-context"),
                            html.Div(link_elements, className="modal-links"),
                        ],
                        className="modal-content-wrapper",
                    )
                    return True, modal_content, active_cell
            return is_open, "", active_cell

        except Exception as e:
            logger.error(f"Error in toggle_modal: {e}")
            return is_open, html.P("Error loading details"), active_cell

    # Callback to update the URL based on pie chart interaction
    @app.callback(Output("url", "pathname"), [Input("pie-chart", "clickData")])
    def update_url_from_pie_click(click_data):
        if click_data:
            clicked_linter = click_data["points"][0]["label"].lower()
            return f"/{clicked_linter}"
        return dash.no_update

    # Callback to render the page content dynamically based on the URL
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page_content(pathname):
        """
        Display the page content and update the sidebar dynamically based on the URL.
        """
        try:
            linter_name = pathname.strip("/").lower()
            available_linters = [
                linter.lower()
                for linter in set([entry["Linter"] for entry in linter_data])
            ]
            if linter_name in available_linters:
                return render_linter_page(linter_name, linter_data)
            return render_home_page(linter_data)
        except Exception as e:
            logger.error(f"Error in display_page_content: {e}")
            return html.Div("Error occurred while rendering the page.")

    @app.callback(
        Output(
            "navbar-title", "children"
        ),  # Assuming the Navbar title component has id 'navbar-title'
        [Input("url", "pathname")],
    )
    def update_header_title(pathname):
        """
        Update the header title based on the current pathname.
        """
        if pathname == "/":
            return "Dashboard"
        else:
            # Extract linter name from the pathname
            linter_name = pathname.strip("/").capitalize()
            return f"{linter_name} Linting Results"


def create_sidebar(linter_data, current_path):
    """Create a sidebar for navigating between linters with a home button and improved AI_Sec styling."""
    enabled_linters = list(set([entry["Linter"] for entry in linter_data]))

    links = [
        dbc.NavLink(
            linter,
            href=f"/{linter.lower()}",
            active=(
                "exact" if f"/{linter.lower()}" == current_path else ""
            ),  # Mark active based on URL path
            style={
                "fontSize": "16px",
                "padding": "12px 20px",
                "borderRadius": "6px",
                "textAlign": "center",
                "color": (
                    "#ffffff" if f"/{linter.lower()}" == current_path else "#b0bec5"
                ),  # Active link color
                "backgroundColor": (
                    "#0056b3" if f"/{linter.lower()}" == current_path else "transparent"
                ),  # Active link background color
                "transition": "background-color 0.3s, color 0.3s",
            },
        )
        for linter in enabled_linters
    ]

    return html.Div(
        [
            # Sidebar Content (Logo and AI_Sec title)
            html.Div(
                [
                    html.Img(
                        src="/assets/logo.webp",
                        className="logo",
                        style={
                            "width": "60%",  # Smaller logo for balance
                            "height": "auto",
                            "margin": "0 auto",
                            "paddingBottom": "10px",
                        },
                    ),
                    html.H2(
                        "AI_SEC",
                        className="sidebar-title",
                        style={
                            "fontSize": "22px",
                            "fontWeight": "bold",
                            "color": "#00bfa5",  # Updated color
                            "marginTop": "10px",
                            "marginBottom": "20px",
                            "textAlign": "center",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "backgroundColor": "#1E2A38",
                    "padding": "15px 0",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)",
                },
            ),
            # Home icon and navigation links
            html.Div(
                dbc.NavLink(
                    html.Img(
                        src="/assets/home-solid.svg",
                        style={"width": "30px", "height": "auto"},
                    ),
                    href="/",
                    active=(
                        "exact" if current_path == "/" else ""
                    ),  # Home link active check
                    className="home-link",
                    style={"textAlign": "center", "marginBottom": "20px"},
                )
            ),
            html.Hr(
                style={"border": "1px solid #E0E0E0", "width": "80%", "margin": "auto"}
            ),  # Divider
            # Navigation links for Linters
            dbc.Nav(
                links,
                vertical=True,
                pills=True,
                style={
                    "paddingTop": "10px",
                    "paddingLeft": "10px",
                    "paddingRight": "10px",
                    "textAlign": "center",
                },
            ),
        ],
        className="sidebar",
        id="sidebar-wrapper",
        style={
            "backgroundColor": "#2E3C4A",
            "padding": "15px",
            "width": "220px",
            "height": "100vh",
            "boxShadow": "2px 0 8px rgba(0, 0, 0, 0.1)",
        },
    )
