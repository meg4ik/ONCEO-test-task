# tasks.py

from celery import Celery
from .database.models import Order

celery = Celery(__name__)

@celery.task
def write_status_change_to_file(order_id, new_status):
    order = Order.query.get(order_id)
    
    with open('status_changes.log', 'a') as file:
        file.write(f"Order ID {order_id} status changed to {new_status}\n")
