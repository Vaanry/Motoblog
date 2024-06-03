from django.db.models.signals import post_save
from django.dispatch import receiver
 
from chat.models import Message
 
 
# обработчик сохранения объекта сообщения
@receiver(post_save, sender=Message)
def post_save_comment(sender, instance, created, **kwargs):
    # если объект был создан
    if created:
        # указываем чату, в котором находится данное сообщение, что это последнее сообщение
        instance.chat.last_message = instance
        # и обновляем данный внешний ключ чата
        instance.chat.save(update_fields=['last_message'])
