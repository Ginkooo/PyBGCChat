from fbchat import Client
from fbchat.models import Message, ThreadType
import os


user = os.environ['FBUSER']
password = os.environ['FBPASS']

client = Client(user, password)

users = client.fetchAllUsers()

print(users)
