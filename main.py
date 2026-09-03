import os

from azure_auth import get_credential
from resources import get_resource_groups
from static_web_apps import get_static_web_apps
from reporting import save_report_json
from checks import run_checks


def build_report():
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

    if not subscription_id:
        print("AZURE_SUBSCRIPTION_ID is not set.")
        return

    credential = get_credential()

    report = {
        "resource_groups": get_resource_groups(
            credential,
            subscription_id
        ),
        "static_web_apps": get_static_web_apps(
            credential,
            subscription_id
        )
    }

    report["findings"] = run_checks(report)

    return report


def display_report(report):
    print("\nAZURE ENVIRONMENT AUDIT")
    print("=" * 50)

    print(f"Resource Groups: {len(report['resource_groups'])}")
    print(f"Static Web Apps: {len(report['static_web_apps'])}")
    print(f"Findings: {len(report['findings'])}")

    print("\nRESOURCE GROUPS")
    print("=" * 50)

    for group in report["resource_groups"]:
        print(f"Name: {group['name']}")
        print(f"Location: {group['location']}")
        print(f"Tags: {group['tags']}")
        print()

    print("\nSTATIC WEB APPS")
    print("=" * 50)

    for app in report["static_web_apps"]:
        print(f"Name: {app['name']}")
        print(f"Resource Group: {app['resource_group']}")
        print(f"Location: {app['location']}")
        print(f"SKU: {app['sku']}")
        print(f"Hostname: {app['default_hostname']}")
        print(f"Tags: {app['tags']}")
        print()

    print("\nFINDINGS")
    print("-" * 50)

    if not report["findings"]:
        print("No findings.")
    else:
        for finding in report["findings"]:
            print(
                f"[{finding['severity']}] "
                f"{finding['resource']}: "
                f"{finding['message']}"
            )


def display_github_summary(report):
    print("\nAZURE ENVIRONMENT AUDIT")
    print("=" * 50)
    print(f"Resource Groups: {len(report['resource_groups'])}")
    print(f"Static Web Apps: {len(report['static_web_apps'])}")
    print(f"Findings: {len(report['findings'])}")
    print("Audit completed successfully.")


if __name__ == "__main__":
    report = build_report()

    if report:
        if os.getenv("GITHUB_ACTIONS") == "true":
            display_github_summary(report)
        else:
            display_report(report)

        save_report_json(report)