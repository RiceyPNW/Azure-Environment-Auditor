#Gets Azure authentication helper
from azure.identity import DefaultAzureCredential

def get_credential():
    return DefaultAzureCredential() # Azure credential object