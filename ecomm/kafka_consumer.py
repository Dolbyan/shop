import os
import django

# Point to the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomm.settings")
django.setup()

from main_app.utilities import KafkaService
from main_app.models import Items
from django.core.exceptions import ObjectDoesNotExist


class KafkaConsumerApp:
    def __init__(self):
        self.kafka_service = KafkaService()

    def process_message(self, message):

        operation = message.get('operation')
        model = message.get('model')
        data = message.get('data')

        if model == 'Items':
            if operation == 'create':
                self.handle_create(data)
            elif operation == 'update':
                self.handle_update(data)
            elif operation == 'delete':
                self.handle_delete(data)

    def handle_create(self, data):
        item = Items.objects.create(
            name=data.get('name'),
            type=data.get('category'),
            description=data.get('description'),
            price=float(data.get('price')),
            amount=int(data.get('amount')),
            image=data.get('image_url'),
            image_name=data.get("image_name")
        )
        item.save()

    def handle_update(self, data):
        try:
            item = Items.objects.get(id=data.get('id'))
            item.name = data.get('name', item.name)
            item.type = data.get('category', item.type)
            item.description = data.get('description', item.description)
            item.price = float(data.get('price', item.price))
            item.amount = int(data.get('amount', item.amount))
            item.image = data.get('image_url', item.image)
            item.image_name = data.get("image_name", item.image_name)
            item.save()
        except ObjectDoesNotExist:
            print(f"Item with id {data.get('id')} does not exist.")

    def handle_delete(self, data):

        try:
            item = Items.objects.get(id=data.get('id'))
            item.delete()
        except ObjectDoesNotExist:
            print(f"Item with id {data.get('id')} does not exist.")

    def start_consuming(self):

        self.kafka_service.consume_messages('inventory_updates', 'group_inventory', self.process_message)

if __name__ == "__main__":
    consumer_service = KafkaConsumerApp()
    consumer_service.kafka_service.consume_messages('inventory_updates', 'inventory_group', consumer_service.process_message)
    print(consumer_service.kafka_service.consume_messages('inventory_updates', 'inventory_group', consumer_service.process_message))