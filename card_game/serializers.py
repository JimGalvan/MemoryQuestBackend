from rest_framework import serializers

from card_game.models import Room, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']


class RoomSerializer(serializers.ModelSerializer):
    owner = PlayerSerializer()
    players = PlayerSerializer(many=True)

    class Meta:
        model = Room
        fields = ['id', 'join_code', 'owner', 'players', 'game']
