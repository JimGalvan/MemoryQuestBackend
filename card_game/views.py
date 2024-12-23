import random
import string
import uuid

from django.http import JsonResponse
from rest_framework.decorators import api_view

from card_game.models import Room, Player


def generate_join_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@api_view(["POST"])
def create_room(request):
    player_name = request.data.get("playerName")

    if not player_name:
        return JsonResponse({"error": "Username is required"}, status=400)

    room_id = str(uuid.uuid4())
    join_code = generate_join_code()

    # create the Player
    player = Player.objects.create(name=player_name)

    # Save room to database
    room = Room.objects.create(
        join_code=join_code,
        owner=player,
    )
    room.players.add(player)

    return JsonResponse({"room_id": room_id, "join_code": join_code}, status=201)
