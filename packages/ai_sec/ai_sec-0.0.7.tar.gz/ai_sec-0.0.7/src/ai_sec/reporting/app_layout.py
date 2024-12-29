import logging

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dash_table.Format import Format

from ai_sec.reporting.components import (
    create_card,
    create_data_table,
    create_footer,
    create_modal,
    create_pie_chart,
)

logger = logging.getLogger()


# Content layout
def create_content_layout():
    """Create the content area where data will be displayed."""
    return html.Div(id="page-content", className="content")


def create_severity_summary_cards(severity_counts):
    """
    Generate summary cards for severity levels based on issue counts.

    :param severity_counts: Dictionary with severity levels and their counts
    :return: Div with summary cards for each severity level
    """
    return html.Div(
        [
            create_card(
                "Critical",
                severity_counts["critical"],
                "#FF4136",
                "bi bi-exclamation-circle-fill",
            ),
            create_card(
                "High",
                severity_counts["high"],
                "#FF851B",
                "bi bi-exclamation-circle-fill",
            ),
            create_card(
                "Medium", severity_counts["medium"], "#FFD700", "bi bi-info-circle-fill"
            ),
            create_card(
                "Low", severity_counts["low"], "#90EE90", "bi bi-info-circle-fill"
            ),
            create_card(
                "Warning",
                severity_counts["warning"],
                "#B0C4DE",
                "bi bi-info-circle-fill",
            ),
        ],
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(5, 1fr)",
            "gap": "20px",
            "alignItems": "center",
            "justifyContent": "center",
            "marginTop": "20px",
            "marginBottom": "40px",
        },
    )


def render_home_page(linter_data):
    # Convert linter data to DataFrame
    df = pd.DataFrame(linter_data)

    # Calculate severity counts
    severity_counts = {
        "critical": (df["Severity"] == "CRITICAL").sum(),
        "high": (df["Severity"] == "HIGH").sum(),
        "medium": (df["Severity"] == "MEDIUM").sum(),
        "low": (df["Severity"] == "LOW").sum(),
        "warning": (df["Severity"] == "WARNING").sum(),
    }

    # Create the pie chart
    issue_counts = df.groupby("Linter").size().reset_index(name="Count")
    fig = px.pie(
        issue_counts,
        names="Linter",
        values="Count",
        title="Linter Breakdown",
        hole=0.3,
        color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"],
    )
    fig.update_layout(
        title_x=0.5,
        title_font=dict(
            size=22, family="Open Sans, sans-serif", color="rgb(42, 63, 95)"
        ),
        margin=dict(t=50),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
    )

    # Assemble layout
    return html.Div(
        [
            # Pie chart
            html.Div(
                dcc.Graph(
                    id="pie-chart",
                    figure=fig,
                    style={"width": "50%", "margin": "0 auto", "height": "auto"},
                ),
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "minHeight": "70vh",
                },
            ),
            # Severity summary cards
            create_severity_summary_cards(severity_counts),
            # Instruction text
            html.H2(
                "Select a section of the chart to explore specific issues.",
                className="summary-text",
                style={
                    "textAlign": "center",
                    "fontSize": "18px",
                    "color": "#333",
                    "marginTop": "20px",
                },
            ),
        ]
    )


def render_linter_page(linter_name, linter_data, report_summary=None):
    """Render the page for a specific linter with concise table, summary cards, and modal for details."""

    linter_name_lower = linter_name.lower()
    filtered_data = [d for d in linter_data if d["Linter"].lower() == linter_name_lower]

    if len(filtered_data) == 0:
        return html.P(f"No data for {linter_name_lower}.")

    # Create DataFrame from filtered linter data
    df = pd.DataFrame(filtered_data)
    issue_summary = None

    # Define summary cards based on linter type
    if linter_name_lower == "checkov":
        total_issues = len(df)
        passed_issues = df[df["Context"] == "PASSED"].shape[0]
        unknown_issues = df[df["Severity"] == "UNKNOWN"].shape[0]
        pass_percentage = (
            (passed_issues / total_issues) * 100 if total_issues > 0 else 0
        )

        # Conditional color for Pass Percentage
        pass_percentage_color = (
            "danger"
            if pass_percentage < 50
            else "warning" if pass_percentage < 70 else "success"
        )

        # Checkov-specific summary
        issue_summary = html.Div(
            [
                create_card("Total Issues", total_issues, "#343a40"),
                create_card(
                    "Passed Issues", passed_issues, "#2ECC40", "bi bi-check-circle-fill"
                ),
                create_card(
                    "Unknown Issues",
                    unknown_issues,
                    "#FF851B",
                    "bi bi-question-circle-fill",
                ),
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
                                color=pass_percentage_color,
                                className="mb-3",
                                style={"height": "20px"},
                            ),
                            html.H5(
                                f"{pass_percentage:.2f}%",
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
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(2, 1fr)",
                "gap": "20px",
                "alignItems": "center",
                "justifyContent": "center",
            },
        )

        # Filter out passed issues for table display
        df = df[df["Context"] != "PASSED"]
    else:
        # Non-Checkov summary with Critical & Medium Percentage
        total_issues = len(df)
        critical_issues = df[df["Severity"] == "CRITICAL"].shape[0]
        high_issues = df[df["Severity"] == "HIGH"].shape[0]
        critical_high_percentage = (
            ((critical_issues + high_issues) / total_issues) * 100
            if total_issues > 0
            else 0
        )

        # Set conditional color for Critical & High Percentage bar
        critical_high_percentage_color = (
            "danger"
            if critical_high_percentage > 50
            else "warning" if critical_high_percentage > 30 else "success"
        )

        # Issue summary for other linters
        issue_summary = html.Div(
            [
                create_card("Total Issues", total_issues, "#343a40"),
                create_card(
                    "Total Critical",
                    critical_issues,
                    "#FF4136",
                    "bi bi-exclamation-circle-fill",
                ),
                create_card(
                    "Total High",
                    high_issues,
                    "#FF851B",
                    "bi bi-exclamation-circle-fill",
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "Critical & High Percentage",
                                className="card-title",
                                style={"fontWeight": "bold", "textAlign": "center"},
                            ),
                            dbc.Progress(
                                value=critical_high_percentage,
                                color=critical_high_percentage_color,
                                className="mb-3",
                                style={"height": "20px"},
                            ),
                            html.H5(
                                f"{critical_high_percentage:.2f}% (Critical + High)",
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
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(2, 1fr)",
                "gap": "20px",
                "alignItems": "center",
                "justifyContent": "center",
            },
        )

    # Fill NaN/None values to avoid rendering issues
    df = df.fillna("")

    # Convert 'Links' to a string for display
    if "Links" in df.columns:
        df["Links"] = df["Links"].apply(
            lambda links: ", ".join(links) if isinstance(links, list) else str(links)
        )

    # Sort by Severity in descending order
    severity_order = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 1}
    df["SeveritySort"] = df["Severity"].map(severity_order)
    df = df.sort_values(by="SeveritySort", ascending=False).drop(
        columns=["SeveritySort"]
    )

    # Define table columns
    columns = [
        {"name": "File", "id": "File"},
        {
            "name": "Line",
            "id": "Line",
            "type": "numeric",
            "format": Format(group=False),
        },
        {"name": "Severity", "id": "Severity"},
        {"name": "Description", "id": "Description"},
        {"name": "Links", "id": "Links"},
    ]

    # Create table, pie chart, and modal components
    table = create_data_table(df, columns)
    pie_chart_div = create_pie_chart(df, "Severity", "Severity Distribution")
    modal = create_modal()

    # Log the rendering
    logger.info(f"Rendering page for {linter_name_lower} with {len(df)} issues.")

    # Assemble layout
    return html.Div(
        [
            html.Div(style={"height": "30px"}),  # Spacer with 30px height
            pie_chart_div,  # Pie chart at the top
            issue_summary if issue_summary else html.Div(),  # Linter-specific summary
            table,  # Data table below the summary
            modal,  # Modal for detailed context
            create_footer(),  # Footer
        ]
    )
