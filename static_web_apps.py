from azure.mgmt.web import WebSiteManagementClient

def get_static_web_apps(credential, subscription_id):
    client = WebSiteManagementClient(
        credential,
        subscription_id
    )

    static_apps = []

    for app in client.static_sites.list():
        static_apps.append({
            "name": app.name,
            "location": app.location,
            "resource_group": app.id.split("/")[4],
            "default_hostname": app.default_hostname,
            "sku": app.sku.name if app.sku else "Unknown",
            "tags": app.tags or {} 
        })

    return static_apps