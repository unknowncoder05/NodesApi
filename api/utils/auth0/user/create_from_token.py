from api.users.serializers import Auth0CreateUserSerializer

def create_from_token(key:str, token:dict):
    user_sub = token['sub']
    user_serializer = Auth0CreateUserSerializer(data=dict(user_sub=user_sub, key=key))
    user_serializer.is_valid(raise_exception=True)
    return user_serializer.save()
