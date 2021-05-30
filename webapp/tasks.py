import datetime
from time import sleep
from celery import shared_task, Task
from django.core.mail import EmailMessage
from webapp.models import Phone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CallbackTask(Task):
    def on_success(self, retval, task_id, *args, **kwargs):
        channel_layer = get_channel_layer()
        if not channel_layer:
            print("Not found")
            return

        async_to_sync(channel_layer.group_send)(
            "finished_tasks",
            {
                'type': 'task_message',
                'message': f'Finished Task {task_id}.  Result is {retval}, Args is {args} Current time is {datetime.datetime.now()}'
            }
        )
        print(f'Finished Task {task_id}.  Result is {retval}, Args is {args} Current time is {datetime.datetime.now()}')


@shared_task(name="task_send_email")
def send_email(emails: list):
    message_content = "Lab 3 email sender"
    # print('dorova')
    msg = EmailMessage("django lab3", message_content, 'dima.django.lab3@ukr.net', emails)
    msg.send()
    return "successful"


@shared_task(name="task_do_long_work", base=CallbackTask)
def do_long_work(time):
    sleep(time)
    count_entity = Phone.objects.count()
    return count_entity
