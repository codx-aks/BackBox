from app.models.base_model import BaseModel
from datetime import datetime
import os

from app.routes.cctv_routes import get_all_cctvs


class CCTV(BaseModel):
    def __init__(self):
        super().__init__()
        self.video_index = 0
    def get_cctv_by_name(self, cctv_name):
        """
        Get CCTV details by CCTV name (e.g., "CCTV1", "CCTV2")
        """
        try:
            return self.find_one({'cctv_name': cctv_name})
        except Exception as e:
            return None
    def get_next_video(self):
        """
        Get videos sequentially from the videos folder
        """
        videos_folder = 'app/static/videos'
        try:
            video_files = sorted([f for f in os.listdir(videos_folder)
                                if f.endswith(('.mp4', '.avi'))])
            
            if not video_files:
                return None
            
            video = video_files[self.video_index]
            self.video_index = (self.video_index + 1) % len(video_files)  # Cycle back to 0 if reached end
            
            return os.path.join(videos_folder, video)
            
        except Exception as e:
            print(f"Error getting video: {str(e)}")
            return None

    def get_user_location_by_watchid(self, watchid):
        """
        Retrieve user location based on the watch ID.
        :param watchid: The ID of the user's watch.
        :return: A dictionary containing latitude and longitude, e.g., {"lat": 12.9716, "long": 77.5946}
        """
        user_location_data = self.database.find_one({"watchid": watchid})
        if user_location_data:
            return {
                "lat": user_location_data["latitude"],
                "long": user_location_data["longitude"]
            }
        return None

    def is_location_in_region(self, user_lat, user_long, cctv_region):
        """
        Check if the user's location is within the CCTV region.
        :param user_lat: Latitude of the user.
        :param user_long: Longitude of the user.
        :param cctv_region: A dictionary defining the CCTV region, e.g., a rectangular boundary.
        :return: True if the location is in the region, False otherwise.
        """
        if (cctv_region["min_lat"] <= user_lat <= cctv_region["max_lat"] and
                cctv_region["min_long"] <= user_long <= cctv_region["max_long"]):
            return True
        return False
    def create_cctvs(self, cctv_coverage):
        """
        Create CCTV entries from the cctvCoverage data
        """
        created_cctvs = []
        
        for floor, cctvs in cctv_coverage.items():
            for cctv_name, positions in cctvs.items():
                cctv = {
                    'cctv_id': int(cctv_name.replace('CCTV', '')),
                    'cctv_name': cctv_name,
                    'floor': floor,
                    'location': {
                        'topleft': {
                            'lat': float(positions['topLeft']['latitude']),
                            'lng': float(positions['topLeft']['longitude'])
                        },
                        'bottomright': {
                            'lat': float(positions['bottomRight']['latitude']),
                            'lng': float(positions['bottomRight']['longitude'])
                        }
                    },
                    'video_feed': self.get_next_video(),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                cctv_id = self.insert_one(cctv)
                created_cctvs.append(cctv_id)

        return created_cctvs

    def get_all_cctvs(self):
        return self.find_many({})

    def get_cctvs_by_floor(self, floor):
        return self.find_many({'floor': floor})

    def get_cctv_by_watchid(self, watchid):
        all_cctvs = self.get_all_cctvs()
        user_location = self.get_user_location_by_watchid(watchid)
        if not user_location:
            return {"error": "User location not found for the given watch ID"}, 404

        user_lat, user_long = user_location['lat'], user_location['long']

        for cctv in all_cctvs:
            cctv_region = cctv['region']
            if self.is_location_in_region(user_lat, user_long, cctv_region):
                return cctv['cc']

        return {"error": "No CCTV region found for the user's location"}, 404






