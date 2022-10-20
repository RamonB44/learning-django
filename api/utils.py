from pickle import FALSE
from rest_framework.views import exception_handler

def rename(self,key,new_key):
    ind = self._keys.index(key)  #get the index of old key, O(N) operation
    self._keys[ind] = new_key    #replace old key with new key in self._keys
    self[new_key] = self[key]    #add the new key, this is added at the end of self._keys
    self._keys.pop(-1)           #pop the last item in self._keys
    
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    # print(exc.get_codes()['code'])
    if response is not None:
        # print(exc.get_codes()['code'])
        if exc.get_codes() == "no_active_account":
            response.status_code = 200
            response.data['error'] = [
                {
                    'type': 'password',
                    'message': 'Contraseña incorrecta',
                }]
        elif exc.get_codes() == 'no_email_account':
            response.status_code = 200
            response.data['error'] = [
                {
                    'type': 'email',
                    'message': 'Correo no encontrado',
                }]
        elif exc.get_codes() == 'not_authenticated':
            response.status_code = 200
            response.data['error'] = [
                {
                    'type': 'not_authenticated',
                    'message': 'Usuario no logeado',
                }]
            response.data["is_valid"] = False
        elif exc.get_codes()['code'] == 'token_not_valid':
            response.status_code = 200
            response.data['error'] = [
                {
                    'type': 'token_not_valid',
                    'message': exc.detail['detail']
                }]
            response.data["is_valid"] = False
        
    return response

def custom_user_authentication_rule(user):
    # Prior to Django 1.10, inactive users could be authenticated with the
    # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
    # prevents inactive users from authenticating.  App designers can still
    # allow inactive users to authenticate by opting for the new
    # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
    # users from authenticating to enforce a reasonable policy and provide
    # sensible backwards compatibility with older Django versions.
    return user is not None and user.is_active