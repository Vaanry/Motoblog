from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, ListView
from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
# Create your views here.
User = get_user_model()


class DialogsView(ListView):
    
    def get_queryset(self):
        self.user = self.request.user
        chats = Chat.objects.filter(members__in=[self.user.id]).order_by('-last_message__pub_date')
        return chats
    
    paginate_by = 10
    template_name = 'dialogs/dialogs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_profile': self.user,
            'unreaded_dialogs_counter': self.user.chat_set.unreaded(user=self.user).count()
        })
        return context  
      

class MessagesView(ListView):
  
    def get_queryset(self):
        self.chat_id = self.kwargs["chat_id"]
        chat = get_object_or_404(Chat, id=self.chat_id)
        user = self.request.user
        if chat and user in chat.members.all():
            chat.message_set.filter(is_readed=False).exclude(author=user).update(is_readed=True)
        else:
            raise PermissionDenied
        messages = Message.objects.filter(chat=self.chat_id).order_by('-pub_date')
        return messages

    paginate_by = 10
    template_name = 'dialogs/messages.html'

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('chat:messages', kwargs={'chat_id': chat_id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'user_profile': user,
            'form': MessageForm(),
            'unreaded_dialogs_counter': user.chat_set.unreaded(user=user).count()
        })
        return context


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chat:messages', kwargs={'chat_id': chat.id}))


@login_required
def edit_message(request, chat_id, pk):
    instance = get_object_or_404(Message, pk=pk)
    if instance.author != request.user:
        raise PermissionDenied
    form = MessageForm(request.POST or None, instance=instance)
    context = {'form': form,
               'comment': instance}
    if form.is_valid():
        form.save()
        return redirect('chat:messages', chat_id)
    return render(request, 'dialogs/messages.html', context)


@login_required
def delete_message(request, chat_id, pk):
    instance = get_object_or_404(Message, pk=pk)
    if instance.author != request.user:
        raise PermissionDenied
    form = MessageForm(instance=instance)
    context = {'form': form,
               'instance': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('chat:messages', chat_id)
    return render(request, 'dialogs/messages.html', context)
