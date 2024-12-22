import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MemoryGameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name = None
        self.game_id = None

    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = f"game_{self.game_id}"

        # Join game group
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data["action"]

        if action == "flip_card":
            card_index = data["card_index"]
            # Process the flip (e.g., check if it's a match)
            # Send the updated state to the group
            await self.channel_layer.group_send(
                self.game_group_name,
                {"type": "game_update", "card_index": card_index, "user": self.scope["user"].id},
            )

    async def game_update(self, event):
        await self.send(text_data=json.dumps(event))
