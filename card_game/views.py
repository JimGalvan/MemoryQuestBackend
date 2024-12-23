import random
import string

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

    join_code = generate_join_code()

    # create the Player
    player = Player.objects.create(name=player_name)

    # Save room to database
    room = Room.objects.create(
        join_code=join_code,
        owner=player,
    )
    room.players.add(player)

    return JsonResponse({"id": room.id, "join_code": join_code}, status=201)


@api_view(["GET"])
def get_room(request, room_id):
    join_code = request.query_params.get("joinCode")
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    # Check if the join code is correct
    if join_code and room.join_code != join_code:
        return JsonResponse({"error": "Invalid join code"}, status=400)

    players = room.players.all()
    players_data = [{"id": player.id, "name": player.name} for player in players]

    return JsonResponse({"players": players_data}, status=200)


@api_view(["POST"])
def join_room(request):
    join_code = request.data.get("joinCode")
    player_name = request.data.get("playerName")
    room_id = request.data.get("roomId")

    if not join_code or not player_name:
        return JsonResponse({"error": "Join code and username are required"}, status=400)

    try:
        room = Room.objects.get(join_code=join_code)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Invalid join code"}, status=404)

    player = Player.objects.create(name=player_name)
    room.players.add(player)

    return JsonResponse({"room_id": room.id}, status=200)
