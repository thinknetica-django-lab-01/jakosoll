import json
from channels.generic.websocket import WebsocketConsumer
from main.models import Product


class ChatConsumer(WebsocketConsumer):
    """docstring for ChatConsumer"""

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message: str = text_data_json['message']
        response_message: str = get_response_message(message)

        self.send(text_data=json.dumps({'message': response_message}))


def get_response_message(message: str) -> str:
    """
    Function takes product name and return count, 
    if it exists
    """
    dash_index: int = message.find('#')
    if dash_index == -1:
        return 'Пожалуйста, укажите название товара после #'

    product_name: str = message[dash_index + 1:].strip()
    try:
        product_count: int = Product.objects.get(name=product_name).amount
    except Product.DoesNotExist:
        return 'Ничего не найдено'
    if product_count == 0:
        return 'Товар закончился'
    return f'В наличии {product_count} шт.'
