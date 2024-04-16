import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class BadRequestError(Exception):
    """Custom exception for bad request errors."""
    pass

def generate_csv(application_vanity_domain, application_id, client_id, client_secret, output_file_name):
    try:
        # Get access token
        access_token = get_token(application_vanity_domain, client_id, client_secret)

        # Define parameters for pagination and variables to collect
        start_index = 1
        count = 50
        all_items = []
        tenants = {}

        # Loop
        while True:
            # Get users
            results = get_users_json(application_vanity_domain, application_id, access_token, start_index, count)

            # if no items break (failsafe #1)
            if not results.get('items'):
                break 

            # Loop through users
            for item in results.get('items'):

                # Get tenantId for user
                tenant_id = item['tenantId']

                # if tenant information has not already been collected then fetch 
                if tenant_id not in tenants:

                    # Get tenant
                    tenant_name = get_tenant_name(application_vanity_domain, access_token, tenant_id)
                    
                    # Add to collection
                    tenants[tenant_id] = tenant_name

                # Get information from existing collection
                else:
                    tenant_name = tenants[tenant_id]

                # Add to item
                item['tenantName'] = tenant_name

                # Append item to all_items
                all_items.append(item)

            # If no more records exist, break (failsafe #2)
            if start_index + count > results.get('totalResults'):
                break

            # Increase start_index by page count
            start_index += count 

        # Convert to df
        output_df = pd.DataFrame.from_records(all_items)

        # Output to csv
        output_df[['tenantName', 'givenName', 'familyName', 'email', 'status']].to_csv(clean_file_name(output_file_name), index=False)

    except (AuthenticationError, BadRequestError) as error:
        print(error)
        return
    

def get_token(application_vanity_domain, client_id, client_secret):
    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/oauth2/token?pretty=true'

    # Headers to indicate the type of data being sent
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Data payload
    payload = {
        'grant_type': 'client_credentials',
    }

    try:
        # Make the request using HTTP Basic Authentication
        response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(client_id, client_secret))

    except:
        raise BadRequestError("Domain name is not valid - please rerun script & enter a valid domain name")

    if response.status_code == 401:
        raise AuthenticationError("Client credentials are not valid - please rerun script & enter valid credentials")
    elif response.status_code == 400:
        raise BadRequestError("Application vanity domain is not valid - please rerun script & enter valid credentials")
    
    # Return json
    return response.json().get('access_token')
    


def get_users_json(application_vanity_domain, application_id, access_token, start_index, count):
    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/applications/{application_id}/users'

    # Define parameters
    querystring = {
        'count': str(count),
        'start_index': str(start_index),
        'fields': 'givenName, familyName, email, status, tenantId'
    }

    # Set the headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    # Perform the GET request
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 404:
        raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
    elif response.status_code == 403:
        raise BadRequestError("Client is not authorized to perform the user export - please rerun script")

    # Return json
    return response.json()


def get_tenant_name(application_vanity_domain, access_token, tenant_id):
    url = f"https://{application_vanity_domain}/api/v1/tenants/{tenant_id}"

    # Define parameters
    querystring = {
        'fields': 'displayName'
    }

    headers = {
        "If-None-Match": "",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 403:
        raise AuthenticationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

    return response.json().get('displayName', 'Unknown Tenant')


def get_non_empty_response(prompt):
    while True:
        response = input(prompt)
        if response:  # This checks if the response is not empty
            return response
        else:
            print("This field cannot be empty. Please enter a valid response.")

def clean_file_name(file_name):
    split_name = file_name.split('.csv')
    if len(split_name) == 1:
        return f'{file_name}.csv'
    else:
        return file_name