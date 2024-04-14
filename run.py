import export_users

application_vanity_domain = export_users.get_application_vanity_domain()
application_id = export_users.get_non_empty_response("Enter the application ID: ")
client_id = export_users.get_non_empty_response("Enter the client ID: ")
client_secret = export_users.get_non_empty_response("Enter the client secret: ")

export_users.generate_csv(application_vanity_domain, application_id, client_id, client_secret)