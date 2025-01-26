from app.models.alert_model import Alert


class AlertController:
    def __init__(self):
        self.alert_model = Alert()

    def add_alert(self, alert_data):
        required_fields = ["alert_id", "severity", "watch_id", "lat", "long", "alert_type"]
        for field in required_fields:
            if field not in alert_data:
                return {"error": f"Missing required field: {field}"}, 400

        if alert_data["severity"] not in ["low", "medium", "high"]:
            return {"error": "Invalid severity value. Use 'low', 'medium', or 'high'."}, 400

        result = self.alert_model.create_alert(alert_data)
        if result:
            return {"message": "Alert added successfully", "alert_id": alert_data["alert_id"]}
        return {"error": "Failed to add alert"}, 500

    def get_all_alerts(self):
        alerts = self.alert_model.get_all_alerts()
        return [alert for alert in alerts]

    def get_alert(self, alert_id):
        alert = self.alert_model.get_alert_by_id(alert_id)
        if alert:
            return alert
        return {"error": f"Alert with ID {alert_id} not found"}, 404

    def update_alert(self, alert_id, updates):
        result = self.alert_model.update_alert(alert_id, updates)
        if result:
            return {"message": f"Alert with ID {alert_id} updated successfully"}
        return {"error": f"Failed to update alert with ID {alert_id}"}, 500

    def delete_alert(self, alert_id):
        result = self.alert_model.delete_alert(alert_id)
        if result:
            return {"message": f"Alert with ID {alert_id} deleted successfully"}
        return {"error": f"Failed to delete alert with ID {alert_id}"}, 500


