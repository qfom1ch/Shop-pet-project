from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def send_mail_about_order(payment_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(payment_id=payment_id)
    subject = f'Ваш заказ #{order.id}!'
    subject_for_manager = f'Поступил заказ #{order.id}!'
    message = f'''Здравствуйте {order.first_name}!
    Ваш заказ успешно принят. Начинаем упаковывать и отправлять!
    Ваш идентификатор заказа {order.id}.'''
    message_for_manager = f'''Поступил заказ {order.id}.
    Информация о заказе: {settings.DOMAIN_NAME}/admin/orders/order/{order.id}/change/
    '''
    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email],
        fail_silently=False)


    mail_sent_for_manager = send_mail(
        subject=subject_for_manager,
        message=message_for_manager,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['viip222@yandex.ru'],
        fail_silently=False)

    return mail_sent, mail_sent_for_manager


