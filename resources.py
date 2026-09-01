from azure.mgmt.resource.resources import ResourceManagementClient


def get_resource_groups(credential, subscription_id):
    client = ResourceManagementClient(
        credential,
        subscription_id
    )

    resource_groups = []

    for group in client.resource_groups.list():
        resource_groups.append({
            "name": group.name,
            "location": group.location,
            "tags": group.tags or {}
        })

    return resource_groups