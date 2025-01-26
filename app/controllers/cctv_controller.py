from app.models.cctv_model import CCTV
from app.utils.video_stream import generate_video_stream
from flask import Response
import os
import mimetypes

class CCTVController:
    def __init__(self):
        self.cctv_model = CCTV()
    
    def get_livefeed(self, cctv_name):
        try:
            cctv = self.cctv_model.get_cctv_by_name(cctv_name)
            
            if not cctv:
                return {
                    "status": "error",
                    "message": f"No CCTV found with name {cctv_name}"
                }
            
            video_path = cctv.get('video_feed')
            
            if not video_path or not os.path.exists(video_path):
                return {
                    "status": "error",
                    "message": "Video feed not found"
                }
            
            mimetype = mimetypes.guess_type(video_path)[0]
            return Response(
                generate_video_stream(video_path),
                mimetype=mimetype,
                headers={
                    'Content-Disposition': 'inline',
                    'Accept-Ranges': 'bytes'
                }
            )
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_all_cctvs(self):
        try:
            cctvs = self.cctv_model.get_all_cctvs()
            return {
                "status": "success",
                "cctvs": cctvs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_cctvs_by_floor(self, floor):
        try:
            cctvs = self.cctv_model.get_cctvs_by_floor(floor)
            return {
                "status": "success",
                "cctvs": cctvs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    def get_cctv_by_watchid(self, watchid):
        try:
            cctvs = self.cctv_model.get_cctv_by_watchid(watchid)
            return {
                "status": "success",
                "cctvs": cctvs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }