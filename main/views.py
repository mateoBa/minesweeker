from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'Hello, World!'})


'''
r = requests.get(url, headers={'Authorization': 'Token f537b208354de36bcc527ad4001cba971658b6a4'})
'''
