from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'chat'

urlpatterns = [
    path(r'all/', login_required(views.DialogsView.as_view()), name='dialogs'),
    path(r'create/<int:user_id>/', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    path(r'<int:chat_id>/', login_required(views.MessagesView.as_view()), name='messages'),
    path(r'delete/<int:chat_id>/<int:pk>/', views.delete_message, name='delete_message'),
    path(r'edit/<int:chat_id>/<int:pk>/', views.edit_message, name='edit_message'),
]
