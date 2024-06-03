from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def about(request):
    template_name = 'pages/about.html'
    user = request.user
    context = {}
    if user.is_authenticated:
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
    return render(request, template_name, context)


def rules(request):
    template_name = 'pages/rules.html'
    context = {}
    user = request.user
    if user.is_authenticated:
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
    return render(request, template_name, context)
