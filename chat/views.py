from django.shortcuts import render
from .models import Conversation, Message
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import UserAccount


def conversation_detail(request, conversation_id):
    user = request.user
    conversation = Conversation.objects.get(id=conversation_id)
    messages = conversation.message_set.all()
    return render(request, 'chat/conversation_detail.html', {'conversation': conversation, 'messages': messages})


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = "chat/conversation_list_page.html"
    context_object_name = "conversations"


    def get_queryset(self):
        return self.request.user.conversations.all()


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation

    def get_object(self, queryset=None):
        return Conversation.objects.get(id=self.kwargs.get("pk"))


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        worker_id = self.kwargs.get("worker_id")
        worker = UserAccount.objects.get(pk=worker_id)
        current_user = self.request.user.id
        users = [worker_id, current_user]
        from django.db.models import Count
        conversation = Conversation.objects.filter(participants__in=users).annotate(
            participant_count=Count('participants')).filter(participant_count=len(users)).first()

        messages = Message.objects.filter(conversation=conversation).all()

        context = {
                'messages': messages,
                'receiver': worker
        }

        return context
