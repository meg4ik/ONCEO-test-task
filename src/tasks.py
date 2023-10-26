import logging
from celery import Celery
from src import celery_config

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(message)s')

celery = Celery(__name__)
celery.config_from_object(celery_config)

@celery.task
def write_status_change_to_file():
        with open('status_changes.log', 'a') as file:
            file.write(f"some\n")
    # logging.info(f'Starting task for order: {order_id}')
    # try:
    #     order = Order.query.get(order_id)
    #     logging.info(f'Order queried: {order_id}')
        

    #     logging.info(f'Status change written to file for order: {order_id}')
        
    # except Exception as e:
    #     logging.error(f'Error: {e}')
    # logging.info(f'Ending task for order: {order_id}')
