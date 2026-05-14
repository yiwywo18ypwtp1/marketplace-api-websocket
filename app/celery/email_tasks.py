from app.celery.celery_app import celery


@celery.task
def send_order_email(order_id: int):
    print(f"EMAIL SENT FOR ORDER {order_id}")