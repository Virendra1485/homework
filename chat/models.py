from django.db import models
from account.models import UserAccount


class Conversation(models.Model):
    participants = models.ManyToManyField(UserAccount, related_name='conversations')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
