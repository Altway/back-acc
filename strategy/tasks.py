from celery import shared_task

@shared_task
def random_task(total):
    for i in range(total):
        print(i)
    return f"Allez là {total}"