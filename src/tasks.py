import logging
from celery import Celery
from src import celery_config
import fcntl

celery = Celery(__name__)
celery.config_from_object(celery_config)

@celery.task
def write_status_change_to_file(order_id, new_status):
    logging.info('Task started')
    try:
        with open('status_changes.log', 'a') as file:
            fcntl.flock(file, fcntl.LOCK_EX)

            try:
                file.write(f"Order ID {order_id} status changed to {new_status}\n")
                logging.info('Status change written to file')
            finally:
                fcntl.flock(file, fcntl.LOCK_UN)

    except Exception as e:
        logging.error(f'Error: {e}')
