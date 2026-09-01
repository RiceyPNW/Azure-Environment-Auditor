import json
from pathlib import Path

def save_report_json(report):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    output_file = reports_dir / "azure_report.json"

    with open(output_file, "w") as file:
        json.dump(report, file, indent=4)

    return output_file