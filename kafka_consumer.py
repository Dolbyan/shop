import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "kafka_consumer_settings"
django.setup()
from admin_app.app.utilities import KafkaService
from admin_app.app.models import Items as AdminItems
from ecomm.main_app.models import Items as UserItems
from django.core.exceptions import ObjectDoesNotExist


class KafkaConsumerApp:
    def __init__(self):
        self.kafka_service = KafkaService()

    # def set_django_settings(self, source):
    #
    #     if source == "user":
    #         os.environ['DJANGO_SETTINGS_MODULE'] = "adminservice.eshop.settings"
    #     elif source == "admin":
    #         os.environ['DJANGO_SETTINGS_MODULE'] = "ecomm.ecomm.settings"
    #
    #     django.setup()

    def process_message(self, message):

        operation = message.get('operation')
        model = message.get('model')
        data = message.get('data')
        source = message.get("source")

        # self.set_django_settings(source)

        if source == "user":
            self.update_admin_inventory(data)
        elif source == "admin" and model == 'Items':
            if operation == 'create':
                self.handle_create(data)
            elif operation == 'update':
                self.handle_update(data)
            elif operation == 'delete':
                self.handle_delete(data)

    def update_admin_inventory(self, data):
        try:
            item = AdminItems.objects.using('admin_db').get(id=data.get("id"))
            item.amount -= int(data.get('amount'))
            item.save()
        except ObjectDoesNotExist:
            print(f"Item with id {data.get('id')} does not exist.")

    def handle_create(self, data):
        item = UserItems.objects.using('ecomm_db').create(
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
            item = UserItems.objects.using('ecomm_db').get(id=data.get('id'))
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
            item = UserItems.objects.using('ecomm_db').get(id=data.get('id'))
            item.delete()
        except ObjectDoesNotExist:
            print(f"Item with id {data.get('id')} does not exist.")

    def start_consuming(self):

        self.kafka_service.consume_messages('inventory_updates', 'group_inventory', self.process_message)


if __name__ == "__main__":
    consumer_service = KafkaConsumerApp()
    consumer_service.kafka_service.consume_messages('inventory_updates', 'inventory_group',
                                                    consumer_service.process_message)
    print(consumer_service.kafka_service.consume_messages('inventory_updates', 'inventory_group',
                                                          consumer_service.process_message))
