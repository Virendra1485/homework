from django.urls import path
from .views import ConversationListView, ChatView, PaymentConfirm, PaymentSuccessView

urlpatterns = [
    path('chats/', ConversationListView.as_view(), name="chats"),
    path('chat/<int:worker_id>/', ChatView.as_view(), name="chat"),
    path('payment/confirm/', PaymentConfirm.as_view(), name="confirm_payment"),
    path('payment/success/', PaymentSuccessView.as_view(), name="success_payment"),
]
