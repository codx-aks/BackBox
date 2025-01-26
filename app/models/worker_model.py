from app.models.base_model import BaseModel
from datetime import datetime

class Worker(BaseModel):
    def __init__(self):
        super().__init__()
        
    def get_next_watch_id(self):
        """Get the next available watch_id"""
        try:
            result = self.collection.find_one(
                {},
                {'watch_id': 1},
                sort=[('watch_id', -1)]
            )
            if result and 'watch_id' in result:
                return result['watch_id'] + 1
            return 0
        except Exception as e:
            return str(e)

    def create_worker(self, worker_data):
        worker = {
            'watch_id': self.get_next_watch_id(),
            'worker_name': worker_data['worker_name'],
            'social_security_number': worker_data['social_security_number'],
            'phone_number': worker_data['phone_number'],
            'status': 'ACTIVE',
            'health_parameters': {},
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.insert_one(worker)

    def update_worker_data(self, watch_id, worker_data):
        """
        Update worker's location, heart rate, and elevation
        """
        try:
            update_data = {
                'current_location': {
                    'lat': float(worker_data['latitude']),
                    'lng': float(worker_data['longitude'])
                },
                'heart_rate': int(worker_data['heart_rate']),
                'absolute_elevation': float(worker_data['absolute_elevation']),
                'last_updated': datetime.utcnow()
            }
            
            historical_data = {
                'timestamp': datetime.utcnow(),
                'location': update_data['current_location'],
                'heart_rate': update_data['heart_rate'],
                'absolute_elevation': update_data['absolute_elevation']
            }
            
            self.collection.update_one(
                {'watch_id': int(watch_id)},
                {
                    '$set': update_data,
                    '$push': {
                        'health_history': historical_data
                    }
                }
            )
            return True
            
        except Exception as e:
            return str(e)

    def get_all_workers(self):
        return self.find_many({})
    def get_worker_by_watch_id(self, watch_id):
        try:
            return self.find_one({'watch_id': int(watch_id)})
        except Exception as e:
            return str(e)