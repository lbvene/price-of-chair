from models.alerts.alert import Alert
from common.database import Database

__author__ = 'lbvene'

Database.initialize()

def get_update_and_send_email():
    alerts_needing_update = Alert.find_needing_update()

    for alert in alerts_needing_update:
        alert.load_and_save_item_price()
        alert.send_email_if_price_reached()
