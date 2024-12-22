from django.contrib.auth.models import User
from django.db import models


class MemoryGame(models.Model):
    player1 = models.ForeignKey(User, related_name="games_as_player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name="games_as_player2", on_delete=models.CASCADE)
    board_state = models.JSONField()  # List of shuffled cards
    current_turn = models.ForeignKey(User, related_name="current_turn", on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
