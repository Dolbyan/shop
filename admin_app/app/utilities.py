import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.permissions import BasePermission
from confluent_kafka import Producer, Consumer
import json

class S3Client():
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file, bucket_name="ecommshop", acl="public-read"):
        try:
            self.s3.upload_fileobj(
                file,
                bucket_name,
                file.name,
                ExtraArgs={
                    "ContentType": file.content_type,
                    "ACL": acl,
                }
            )
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

        return True

    def get_file_url(self, file_name):
        try:
            response = self.s3.generate_presigned_url("get_object",
                                                      Params={"Bucket": self.bucket_name,
                                                              "Key": file_name},
                                                      ExpiresIn=3600)
        except ClientError as e:
            print(e)
            return None
        return response

class JWT:
    @staticmethod
    def generate_token(user):
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    @staticmethod
    def authenticate_request(request):
        from .models import User

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user = User.objects.filter(id=payload["id"]).first()
        if not user:
            raise AuthenticationFailed("User not found!")
        print("GIT AUTO")
        return user

class IsAuthenticatedJWT(BasePermission):
    def has_permission(self, request, view):
        from .models import User
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Brak tokenu w ciasteczkach.")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token wygasł.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Nieprawidłowy token.")

        user = User.objects.filter(id=payload["id"]).first()

        if not user:
            raise AuthenticationFailed("Użytkownik nie istnieje.")

        request.user = user
        return True

class KafkaService:
    def __init__(self):
        self.bootstrap_servers = 'kafka:9092'


    def kafka_producer(self):
        producer = Producer({
            'bootstrap.servers': self.bootstrap_servers
        })
        return producer


    def send_message(self, topic, operation, model_name, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass
        message = {
            'operation': operation,
            'model': model_name,
            'data': data
        }
        print("Wiadomość przed serializacją:", message)
        message_json = json.dumps(message)
        print("Wiadomość po serializacji:", message_json)
        producer = self.kafka_producer()
        producer.produce(topic, message_json)
        producer.flush()


    def kafka_consumer(self, group_id):
        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'latest'
        })
        return consumer

    def consume_messages(self, topic, group_id, process_message_function):
        consumer = self.kafka_consumer(group_id)
        consumer.subscribe([topic])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            process_message_function(json.loads(msg.value().decode('utf-8')))
