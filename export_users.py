import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

def generate_csv(application_vanity_domain, application_id, client_id, client_secret):

    access_token = get_token(application_vanity_domain, client_id, client_secret)

    start_index = 1
    count = 20

    all_items = []
    tenants = {}

    while True:
        results = get_users_json(application_vanity_domain, application_id, access_token, start_index, count)

        if not results.get('items'):
            break 

        # Loop through items to get tenant
        for item in results.get('items'):

            # Get tenantId value
            tenant_id = item['tenantId']

            # If tenantId is not already fetched
            if tenant_id not in tenants:

                # Fetch tenantName
                tenant_name = get_tenant_name(application_vanity_domain, access_token, tenant_id)

                # Add tenantId to tenants dict
                tenants[tenant_id] = tenant_name

            # Get tenantName from tenant dict
            else:
                tenant_name = tenants[tenant_id]
            
            item['tenantName'] = tenant_name
            all_items.append(item)

        if start_index + count > results.get('totalResults'):
            break

        start_index += count 

    output_df = pd.DataFrame.from_records(all_items)

    output_df[['tenantName', 'email', 'status']].to_csv('users.csv', index=False)


def get_token(application_vanity_domain, client_id, client_secret):
    # The URL for the token request
    url = f'https://{application_vanity_domain}/api/v1/oauth2/token?pretty=true'

    # Headers to indicate the type of data being sent
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Data payload
    payload = {
        'grant_type': 'client_credentials',
    }

    # Make the request using HTTP Basic Authentication
    response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(client_id, client_secret))

    # Return json
    return response.json().get('access_token')


def get_users_json(application_vanity_domain, application_id, access_token, start_index, count):
    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/applications/{application_id}/users'

    # Define parameters
    querystring = {
        'count': str(count),
        'start_index': str(start_index),
        'fields': 'email, status, tenantId'
    }

    # Set the headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    # Perform the GET request
    response = requests.get(url, headers=headers, params=querystring)

    # Return json
    return response.json()


def get_tenant_name(application_vanity_domain, access_token, tenant_id):
    url = f"https://{application_vanity_domain}/api/v1/tenants/{tenant_id}"

    headers = {
        "If-None-Match": "",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    return response.json().get('displayName', 'Unknown Tenant')