from django.shortcuts import render
from .models import Conversation, Message
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from account.models import UserAccount, Payment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from stripe_utils import StripeHelpers


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

    def get(self, request, *args, **kwargs):
        if self.request.user.role == "customer":
            worker = UserAccount.objects.get(pk=self.kwargs.get("worker_id"))
            payment = Payment.objects.filter(paid_location_city=worker.location_city, payment_status="succeeded",
                                             customer=self.request.user).first()
            if not payment:
                payment_intent_id, status = StripeHelpers().create_payment_intent(
                    100 * 100, "INR",
                    self.request.user.stripe_customer_id
                )
                payment = Payment.objects.create(customer=self.request.user, payment_status=status,
                                                 paid_location_city=worker.location_city, amount=100,
                                                 payment_id=payment_intent_id)
                payment.save()
                return HttpResponseRedirect(reverse('confirm_payment') + f'?payment_id={payment.id}')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        worker = UserAccount.objects.get(pk=self.kwargs.get("worker_id"))
        users = [self.kwargs.get("worker_id"), self.request.user.id]
        conversation = Conversation.objects.annotate(count=Count('participants')).filter(count=len(users))
        for user in users:
            conversation = conversation.filter(participants__pk=user)
        if conversation:
            messages = Message.objects.filter(conversation=conversation.first()).all()
            return {'messages': messages, 'receiver': worker}
        return {'receiver': worker}


class PaymentConfirm(TemplateView):
    template_name = 'chat/payment_confirm.html'

    def post(self, request, *args, **kwargs):

        context_data = self.get_context_data()
        url, payment_intent_status = StripeHelpers().confirm_payment_intent(context_data.get("payment").payment_id)
        payment = Payment.objects.get(pk=context_data.get("payment").id)
        payment.payment_status = payment_intent_status
        payment.save()
        return redirect(url)

    def get_context_data(self, **kwargs):
        payment = Payment.objects.get(pk=int(self.request.GET.get("payment_id")))
        return {"payment": payment}


class PaymentSuccessView(TemplateView):
    template_name = 'chat/payment_success.html'

    def get_context_data(self, **kwargs):
        payment_intent_status = StripeHelpers().retrieve_payment_intent(self.request.GET.get("payment_intent"))
        payment = Payment.objects.filter(payment_id=self.request.GET.get("payment_intent")).first()
        payment.payment_status = payment_intent_status
        payment.save()
        return {"payment": payment}
