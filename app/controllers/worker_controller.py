from app.models.worker_model import Worker
from app.models.project_model import Project
from app.models.alert_model import Alert
from datetime import datetime
import uuid

class WorkerController:
    def __init__(self):
        self.worker_model = Worker()
        self.project_model = Project()
        self.alert_model = Alert()
        
        # Health monitoring thresholds
        self.HEART_RATE_MIN = 60
        self.HEART_RATE_MAX = 120
    
    def create_worker(self, worker_data):
        try:
            required_fields = ['worker_name', 'social_security_number', 'phone_number']
            for field in required_fields:
                if field not in worker_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }
            
            worker_id = self.worker_model.create_worker(worker_data)
            
            if worker_id:
                worker = self.worker_model.find_by_id(worker_id)
                return {
                    "status": "success",
                    "message": "Worker created successfully",
                    "worker_id": worker_id,
                    "watch_id": worker.get('watch_id')
                }
            return {
                "status": "error",
                "message": "Failed to create worker"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def check_health_status(self, heart_rate, watch_id, lat, lng):
        """Check heart rate and create alert if necessary"""
        try:
            if heart_rate < self.HEART_RATE_MIN or heart_rate > self.HEART_RATE_MAX:
                print(f"Abnormal heart rate detected: {heart_rate}")  # Debug print
                severity = "high" if (heart_rate < self.HEART_RATE_MIN - 10 or 
                                    heart_rate > self.HEART_RATE_MAX + 10) else "medium"
                alert_data = {
                    'alert_id': str(uuid.uuid4()),
                    'severity': severity,
                    'watch_id': watch_id,
                    'lat': float(lat),  # Ensure float
                    'long': float(lng),  # Ensure float
                    'alert_type': "Abnormal Heart Rate",
                    'timestamp': datetime.utcnow()
                }
                print(f"Creating heart rate alert: {alert_data}")  # Debug print
                result = self.alert_model.create_alert(alert_data)
                print(f"Heart rate alert creation result: {result}")  # Debug print
                if result:
                    return alert_data
        except Exception as e:
            print(f"Error in check_health_status: {str(e)}")  # Debug print
        return None

    def check_hazardous_conditions(self, worker_data, current_floor):
        """Check if worker is in hazardous conditions"""
        try:
            project = self.project_model.get_project_details()
            if not project:
                print("No project details found")  # Debug print
                return None

            lat = float(worker_data['latitude'])
            lng = float(worker_data['longitude'])
            elevation = float(worker_data['absolute_elevation'])
            watch_id = worker_data['watch_id']

            print(f"Checking hazard for floor {current_floor}")  # Debug print
            in_hazard_zone = self.project_model.check_hazardous_zone(current_floor, lat, lng)
            above_danger_elevation = elevation > project.get('danger_elevation', 0)

            print(f"In hazard zone: {in_hazard_zone}, Above danger elevation: {above_danger_elevation}")  # Debug print

            if in_hazard_zone or above_danger_elevation:
                severity = "high" if (in_hazard_zone and above_danger_elevation) else "medium"
                alert_data = {
                    'alert_id': str(uuid.uuid4()),
                    'severity': severity,
                    'watch_id': watch_id,
                    'lat': lat,
                    'long': lng,
                    'alert_type': "Hazardous Zone Alert",
                    'timestamp': datetime.utcnow()
                }
                print(f"Creating hazard alert: {alert_data}")  # Debug print
                result = self.alert_model.create_alert(alert_data)
                print(f"Hazard alert creation result: {result}")  # Debug print
                if result:
                    return alert_data
        except Exception as e:
            print(f"Error in check_hazardous_conditions: {str(e)}")  # Debug print
        return None

    def update_worker_data(self, worker_data):
        try:
            # Validate required fields
            required_fields = ['watch_id', 'latitude', 'longitude', 'heart_rate', 'absolute_elevation']
            for field in required_fields:
                if field not in worker_data:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }

            # Validate data types
            try:
                watch_id = int(worker_data['watch_id'])
                lat = float(worker_data['latitude'])
                lng = float(worker_data['longitude'])
                heart_rate = int(worker_data['heart_rate'])
                elevation = float(worker_data['absolute_elevation'])
            except ValueError:
                return {
                    "status": "error",
                    "message": "Invalid data types. Please check your input values"
                }

            # Validate ranges
            if not (-90 <= lat <= 90):
                return {
                    "status": "error",
                    "message": "Latitude must be between -90 and 90"
                }
                
            if not (-180 <= lng <= 180):
                return {
                    "status": "error",
                    "message": "Longitude must be between -180 and 180"
                }
                
            if not (0 <= heart_rate <= 250):
                return {
                    "status": "error",
                    "message": "Heart rate must be between 0 and 250"
                }

            # Check if worker exists
            worker = self.worker_model.get_worker_by_watch_id(watch_id)
            if not worker:
                return {
                    "status": "error",
                    "message": f"No worker found with watch_id: {watch_id}"
                }

            # Get project details and calculate floor
            project = self.project_model.get_project_details()
            if not project:
                return {
                    "status": "error",
                    "message": "Project details not found"
                }

            current_floor = self.project_model.calculate_floor(
                elevation,
                float(project['sea_level_ground_elevation']),
                float(project['floor_height'])
            )

            # Check conditions and generate alerts
            alerts = []
            
            # Check heart rate
            health_alert = self.check_health_status(heart_rate, watch_id, lat, lng)
            if health_alert:
                alerts.append(health_alert)

            # Check hazardous conditions
            hazard_alert = self.check_hazardous_conditions(worker_data, current_floor)
            if hazard_alert:
                alerts.append(hazard_alert)

            # Update worker data
            result = self.worker_model.update_worker_data(watch_id, worker_data)
            
            if result:
                response = {
                    "status": "success",
                    "message": "Worker data updated successfully",
                    "watch_id": watch_id,
                    "current_floor": current_floor,
                    "data": {
                        "location": {
                            "latitude": lat,
                            "longitude": lng
                        },
                        "heart_rate": heart_rate,
                        "absolute_elevation": elevation
                    }
                }
                
                if alerts:
                    response["alerts"] = alerts
                
                return response

            return {
                "status": "error",
                "message": "Failed to update worker data"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_all_workers(self):
        try:
            workers = self.worker_model.get_all_workers()
            return {
                "status": "success",
                "workers": workers
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_worker_by_watch_id(self, watch_id):
        try:
            worker = self.worker_model.get_worker_by_watch_id(watch_id)
            if worker:
                return {
                    "status": "success",
                    "worker": worker
                }
            return {
                "status": "error",
                "message": f"No worker found with watch_id: {watch_id}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }