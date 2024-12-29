import requests


class Contacts:
    base_url = 'https://users.go-mailer.com'

    def __init__(self, api_key):
        self.api_key = api_key

    def synchronize(self, email, data={}):
        if not email:
            raise Exception('Email must be specified.')
        elif not bool(data):
            raise Exception('User data must be specified.')

        body = data
        body['email'] = email
        headers = {'Authorization': f'Bearer {self.api_key}'}

        response = requests.post(
            f'{self.base_url}/api/contacts', json=body, headers=headers)
        return response
