from app.models.base_model import BaseModel
from datetime import datetime
from bson import ObjectId

class Project(BaseModel):
    def __init__(self):
        super().__init__()
    
    def create_project(self, project_data):
        project = {
            'name': project_data['name'],
            'centre_location': {
                'lat': float(project_data['centre_lat']),
                'lng': float(project_data['centre_long'])
            },
            'status': 'INITIAL',
            'location': project_data['location'],
            'project_code': project_data['project_code'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.insert_one(project)

    def configure_project(self, project_id, config_data):
        update_data = {
            'site_boundary': {
                'topleft': {
                    'lat': float(config_data['siteTopLeft']['latitude']),
                    'lng': float(config_data['siteTopLeft']['longitude'])
                },
                'bottomright': {
                    'lat': float(config_data['siteBottomRight']['latitude']),
                    'lng': float(config_data['siteBottomRight']['longitude'])
                }
            },
            'sea_level_ground_elevation': config_data['sea_level_ground_elevation'],
            'danger_elevation': config_data['danger_elevation'],
            'number_of_floors': config_data['number_of_floors'],
            'floor_height': config_data['floor_height'],
            'hazardous_zones': {},
            'cctv_ids': config_data.get('cctv_ids', []),
            'status': 'CONFIGURED',
            'updated_at': datetime.utcnow()
        }

        # Process hazardous zones
        for floor, zones in config_data['hazardousZones'].items():
            update_data['hazardous_zones'][floor] = [
                {
                    'topleft': {
                        'lat': float(zone['topLeft']['latitude']),
                        'lng': float(zone['topLeft']['longitude'])
                    },
                    'bottomright': {
                        'lat': float(zone['bottomRight']['latitude']),
                        'lng': float(zone['bottomRight']['longitude'])
                    }
                }
                for zone in zones
            ]

        return self.update_one({'_id': ObjectId(project_id)}, update_data)
    def get_project_details(self):
        """Get the first project's details (since we have only one project)"""
        return self.find_one({})

    def calculate_floor(self, elevation, ground_altitude, floor_height):
        """Calculate floor number based on elevation"""
        if elevation < ground_altitude:
            return 0
        relative_height = elevation - ground_altitude
        floor = int(relative_height / floor_height) + 1
        return str(floor)  # Convert to string to match floor numbers in hazardous_zones

    def is_point_in_zone(self, lat, lng, zone):
        """Check if a point is inside a rectangular zone"""
        zone_min_lat = min(zone['topleft']['lat'], zone['bottomright']['lat'])
        zone_max_lat = max(zone['topleft']['lat'], zone['bottomright']['lat'])
        zone_min_lng = min(zone['topleft']['lng'], zone['bottomright']['lng'])
        zone_max_lng = max(zone['topleft']['lng'], zone['bottomright']['lng'])
        
        return (zone_min_lat <= lat <= zone_max_lat and 
                zone_min_lng <= lng <= zone_max_lng)

    def check_hazardous_zone(self, floor, lat, lng):
        """Check if location is in any hazardous zone on the given floor"""
        project = self.get_project_details()
        if not project or 'hazardous_zones' not in project:
            return False
        
        floor_zones = project['hazardous_zones'].get(floor, [])
        for zone in floor_zones:
            if self.is_point_in_zone(lat, lng, zone):
                return True
        return False