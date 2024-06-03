# -*- coding: utf-8 -*-
 
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class ChatManager(models.Manager):
    use_for_related_fields = True
 
    # Метод принимает пользователя, для которого должна производиться выборка
    # Если пользователь не добавлен, то будет возвращены все диалоги,
    # в которых хотя бы одно сообщение не прочитано
    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_readed=False)
        return qs.exclude(last_message__author=user) if user else qs
        
    
class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )
 
    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))
    # внешний ключ на последнее сообщение,
    # важный момент в том, что название класса Message пишем обычной строкой,
    # поскольку на момент чтения класса Chat интерпретатор Python ничего не знает о классе Message
    # Также необходимо добавить related_name, имя через которое будет ассоциироваться выборка данного сообщения из базы данных
    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True, on_delete=models.SET_NULL)
 
    objects = ChatManager()

    def get_absolute_url(self):
        return reverse('chat:messages', (), {'chat_id': self.pk })
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message

