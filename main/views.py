from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.controllers import UserController


class GameApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_controller = UserController(request.user)
        return Response({'games': user_controller.get_games_by_user()})

    def post(self, request):
        user = request.user
        user_controller = UserController(user)
        game = user_controller.create_game(request.data.get('columns'),
                                           request.data.get('rows'),
                                           request.data.get('mines'))
        return Response({'matrix': game})



