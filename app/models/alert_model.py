from app.models.base_model import BaseModel
from datetime import datetime
from bson import ObjectId


class Alert(BaseModel):
    def __init__(self):
        super().__init__()

    def create_alert(self, alert_data):
        alert = {
            'alert_id': alert_data['alert_id'],
            'severity': alert_data['severity'],  # low, medium, high
            'watch_id': alert_data['watch_id'],
            'lat': alert_data['lat'],
            'long': alert_data['long'],
            'alert_type': alert_data['alert_type'],  # e.g., "Fire", "Intrusion"
            'timestamp': alert_data.get('timestamp', datetime.utcnow()),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.insert_one(alert)

    def get_all_alerts(self):
        return self.find_many({})

    def get_alert_by_id(self, alert_id):
        return self.find_one({'alert_id': alert_id})

    def update_alert(self, alert_id, updates):
        return self.update_one(
            {'alert_id': alert_id},
            {**updates, 'updated_at': datetime.utcnow()}
        )

    def delete_alert(self, alert_id):
        return self.delete_one({'alert_id': alert_id})
