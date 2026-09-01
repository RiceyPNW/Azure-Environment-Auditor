def run_checks(report):
    findings = []

    for group in report["resource_groups"]:
        if not group["tags"]:
            findings.append({
                "severity": "INFO",
                "resource": group["name"],
                "message": "Resource group has no tags"
            })

    for app in report["static_web_apps"]:
        if not app["tags"]:
            findings.append({
                "severity": "INFO",
                "resource": app["name"],
                "message": "Static Web App has no tags"
            })

    return findings