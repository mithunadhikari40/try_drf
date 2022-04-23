from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class AuthTokenization(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # print(f"Truehe all data is ${user}")
        token, created = Token.objects.get_or_create(user=user)
        print(f"The token data is ${token}")

        return Response({
            'token': token.key,
            'id': user.pk,
            # 'user': user,
            # 'all': serializer.validated_data,
            'email': user.email,
            'created':created
            # 'all_token': token
        })
