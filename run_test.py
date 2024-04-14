import export_users

application_vanity_domain = 'invoexp-donato.us.wristband.dev'
application_id = '65ozodiubbcyba3mbdgupupz6y'
client_id = 'ploopscbu5cmzi4hndvcsyepi4'
client_secret = 'dc0a4ba0a4e10cb670c1c95a66d11698'    

export_users.generate_csv(application_vanity_domain, application_id, client_id, client_secret)
