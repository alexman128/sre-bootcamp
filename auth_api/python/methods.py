import jwt
import jsonify
import sys

secret = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

# These functions need to be implemented
class Token:

    def generate_token(self, username, password):
        #puse ese payload pero no estoy seguro si el correcto es el que ustedes usaron en su ejemplo:
        #aunque en las instrucciones dice que el payload debe de ser el rol y en este caso seria el username
        '''
                {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
        }
        '''

        encoded_jwt = jwt.encode({"username": username}, secret, algorithm="HS256")

        print(encoded_jwt)
        
        return encoded_jwt


class Restricted:

    def access_data(self, authorization):
        if not authorization:
            return 'token is missing'
        try:
            print(f"secret: {secret}")
            print(f"authorization: {authorization}")
            data = jwt.decode(authorization, secret, algorithms=["HS256"])
        except:
            e = sys.exc_info()[0]
            print(f"Exception: {e}")
            return 'wrong token'

        return 'You are under protected data'
