import argparse
import json
import os
from datetime import datetime


def generate_html_report(input_file, summary_file, output_file, css_file=None):
    try:
        with open(input_file, "r") as file:
            report_data = json.load(file)

        with open(summary_file, "r") as file:
            summary_data = json.load(file)

        # Extract summary and linter data
        summary = report_data.get("summary", {})
        linters = report_data.get("linters", {})

        # Determine if all severities are UNKNOWN
        all_unknown = all(
            issue.get("Severity", "").lower() == "unknown"
            for linter_issues in linters.values()
            for issue in linter_issues
        )

        # Start building the HTML content
        html = ["<!DOCTYPE html>", "<html>", "<head>", "<meta charset='UTF-8'>"]
        html.append("<title>AI Sec Report</title>")

        # Add optional CSS
        if css_file and os.path.exists(css_file):
            with open(css_file, "r") as css:
                html.append("<style>")
                html.append(css.read())
                html.append("</style>")

        html.append("</head>")
        html.append("<body>")
        html.append("<h1>AI Sec Report</h1>")

        # Severity color mapping
        severity_colors = {
            "critical": "#f5c6cb",  # Soft red
            "high": "#ffe5b4",  # Light orange
            "medium": "#fff3cd",  # Pale yellow
            "low": "#d4edda",  # Soft green
            "warning": "#d1ecf1",  # Light blue
        }

        # Display warning if all severities are UNKNOWN
        if all_unknown:
            html.append(
                "<div style='background-color: #f8d7da; color: #721c24; padding: 15px; border: 1px solid #f5c6cb; "
                "margin-bottom: 20px; border-radius: 5px;'>"
                "<strong>Warning:</strong> All severities are marked as <strong>UNKNOWN</strong>. "
                "To enable insights and improve severity classification, ensure you have set the <code>OPENAI_API_KEY</code>."
                "</div>"
            )

        # Summary Section
        html.append("<h2>Issue Summary</h2>")
        html.append("<div class='summary-table' style='width: 50%; margin: 0 auto;'>")
        html.append("<table>")
        html.append("<thead><tr><th>Severity</th><th>Count</th></tr></thead>")
        html.append("<tbody>")

        for severity, count in summary_data.get("by_severity", {}).items():
            bg_color = severity_colors.get(severity.lower(), "#ffffff")
            html.append(
                f"<tr style='background-color: {bg_color};'><td>{severity.capitalize()}</td><td>{count}</td></tr>"
            )

        html.append("</tbody></table></div>")
        html.append(f"<p style='text-align: center;'><strong>Total Linters:</strong> {summary.get('linted_files', 0)}</p>")
        html.append(f"<p style='text-align: center;'><strong>Total Issues:</strong> {summary_data.get('total_issues', 0)}</p>")

        # List linters
        linter_names = ", ".join(linters.keys())
        html.append(f"<p style='text-align: center;'><strong>Linters Used:</strong> {linter_names}</p>")

        # Add spacing before Lint Issues section
        html.append("<div style='margin-top: 40px;'></div>")

        # Linter Issues Section
        html.append("<h2>Lint Issues</h2>")
        html.append("<div class='scrollable-table'>")  # Add scrollable container
        html.append("<table>")
        html.append(
            "<thead><tr><th>LINTER</th><th>FILE</th><th>LINE</th><th>DESCRIPTION</th><th>SEVERITY</th>"
            "<th>CONTEXT</th><th>LINKS</th></tr></thead>"
        )
        html.append("<tbody>")

        for linter_name, issues in linters.items():
            for issue in issues:
                severity = issue.get("Severity", "").lower()
                bg_color = severity_colors.get(severity, "#ffffff")

                html.append(f"<tr style='background-color: {bg_color};'>")
                html.append(f"<td>{issue.get('Linter', 'N/A')}</td>")
                html.append(f"<td>{issue.get('File', 'N/A')}</td>")
                html.append(f"<td>{issue.get('Line', 'N/A')}</td>")
                html.append(f"<td>{issue.get('Description', 'N/A')}</td>")
                html.append(f"<td>{issue.get('Severity', 'N/A')}</td>")
                html.append(f"<td>{issue.get('Context', 'N/A')}</td>")

                # Process links with the updated logic
                if "Links" in issue:
                    links = issue["Links"]
                    if isinstance(links, list):  # If it's a list, join the links
                        link_html = "<br>".join(f'<a href="{link}" target="_blank">{link}</a>' for link in links)
                    else:  # If it's a string, treat it as a single link
                        link_html = f'<a href="{links}" target="_blank">{links}</a>'
                else:
                    link_html = ""
                html.append(f"<td>{link_html}</td>")

                html.append("</tr>")

        html.append("</tbody></table>")
        html.append("</div>")  # Close scrollable container

        # Footer Section
        html.append("<footer>")
        html.append(
            f"Report generated on <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong>"
        )
        html.append("</footer>")

        html.append("</body></html>")

        # Write the HTML content to the output file
        with open(output_file, "w") as file:
            file.write("\n".join(html))

        print(f"HTML report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")


# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a JSON report to an HTML report.")
    parser.add_argument("--input", required=True, help="Path to the input JSON report file.")
    parser.add_argument("--summary", required=True, help="Path to the summary JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output HTML file.")
    parser.add_argument("--css", help="Path to the optional CSS file for styling.")

    args = parser.parse_args()
    generate_html_report(args.input, args.summary, args.output, args.css)