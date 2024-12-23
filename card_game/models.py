import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        abstract = True


class MemoryGame(BaseModel):
    player1 = models.ForeignKey(User, related_name="games_as_player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name="games_as_player2", on_delete=models.CASCADE)
    board_state = models.JSONField()
    current_turn = models.ForeignKey(User, related_name="current_turn", on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)


class Player(BaseModel):
    name = models.CharField(max_length=50, unique=False)


class Room(BaseModel):
    join_code = models.CharField(max_length=6, unique=True)  # Short human-readable code
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owned_rooms")
    players = models.ManyToManyField(Player, related_name="joined_rooms")
    game = models.OneToOneField(MemoryGame, on_delete=models.CASCADE, null=True, blank=True)
