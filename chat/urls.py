from django.urls import path
from .views import ConversationListView, ChatView

urlpatterns = [
    path('chats/', ConversationListView.as_view(), name="chats"),
    path('chat/<int:worker_id>/', ChatView.as_view(), name="chat"),
]
