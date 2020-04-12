from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.controllers import UserController
from main.models import SettingUser


class GameApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'games': UserController.get_games_by_user(request.user)})

    def post(self, request):
        matrix = UserController.create_game(request.user,
                                            request.data.get('columns'),
                                            request.data.get('rows'),
                                            request.data.get('mines'))
        return Response({'matrix': matrix})

    def put(self, request):
        # todo: check if exists SettingUsers
        settings = SettingUser.objects.get(user=request.user)
        x, y = request.data.get('x'), request.data.get('y')
        result = UserController.press(request.user, settings.game_selected, x, y)
        return Response(result)

