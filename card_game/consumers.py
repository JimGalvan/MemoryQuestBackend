import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer


def generate_board():
    colors = ["#FF5733", "#33FF57", "#3357FF", "#FFC300", "#C70039", "#900C3F"]
    pairs = []
    for i in range(4):
        pairs.append({"number": i + 1, "color": colors[i % len(colors)]})
        pairs.append({"number": i + 1, "color": colors[i % len(colors)]})
    random.shuffle(pairs)
    return pairs


class MemoryGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.group_name = f"game_{self.game_id}"

        # Initialize game state (store in-memory or use a persistent store)
        self.game_state = {
            "board": generate_board(),  # Randomized board data
            "flipped_cards": [],
            "matched_pairs": []
        }

        # Join the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # send the initial board state
        await self.send(text_data=json.dumps({
            "type": "board_state",
            "board": self.game_state["board"]
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "flip_card":
            card_index = data["card_index"]
            await self.handle_flip(card_index)

    async def handle_flip(self, card_index):
        board = self.game_state["board"]
        flipped_cards = self.game_state["flipped_cards"]
        matched_pairs = self.game_state["matched_pairs"]

        # Check if the card is already matched
        if card_index in matched_pairs:
            return

        # Add the card to flipped cards
        flipped_cards.append(card_index)

        if len(flipped_cards) == 2:
            # Check for a match
            card1 = board[flipped_cards[0]]
            card2 = board[flipped_cards[1]]
            is_match = card1["number"] == card2["number"]

            if is_match:
                matched_pairs.extend(flipped_cards)
                self.game_state["flipped_cards"] = []
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "game_update",
                        "card_indices": flipped_cards,
                        "match": True,
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "game_update",
                        "card_indices": flipped_cards,
                        "match": False,
                    }
                )
                # Reset flipped cards after a delay
                self.game_state["flipped_cards"] = []

        else:
            # Send flip update to all clients
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "game_update",
                    "card_indices": [card_index],
                    "match": None,
                }
            )

    async def send_game_update(self, card_index, match):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "game_update",
                "card_index": card_index,
                "match": match,
            }
        )

    async def reset_flipped_cards(self, event):
        self.game_state["flipped_cards"] = []
        await self.send(text_data=json.dumps({"type": "reset_flipped_cards"}))

    async def game_update(self, event):
        await self.send(text_data=json.dumps(event))

