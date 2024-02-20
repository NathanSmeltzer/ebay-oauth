import base64

def _generate_request_headers(credential):
    
    credential_string = f'{credential.client_id}:{credential.client_secret}'
    b64_encoded_credential = base64.b64encode(credential_string.encode()).decode()
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b64_encoded_credential
    }

    return headers


def _generate_application_request_body(credential, scopes):


    body = {
            'grant_type': 'client_credentials',
            'redirect_uri': credential.ru_name,
            'scope': scopes
    }
    

    return body

def _generate_refresh_request_body(scopes, refresh_token):
    if refresh_token == None:
        raise Exception("credential object does not contain refresh_token and/or scopes")
    
    body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'scope':scopes
    }
    return body

def _generate_oauth_request_body(credential, code):
    body = {
            'grant_type': 'authorization_code',
            'redirect_uri': credential.ru_name,
            'code':code
    }
    return body