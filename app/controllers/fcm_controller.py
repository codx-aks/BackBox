from firebase_admin import messaging
from flask import jsonify

class FCMController:
    @staticmethod
    def send_topic_notification(data):
        """
        Send notification to all devices subscribed to a topic
        
        Args:
            data (dict): Contains topic, title, and body for the notification
        
        Returns:
            tuple: (response_dict, status_code)
        """
        try:
            # Validate required fields
            topic = data.get('topic')
            title = data.get('title')
            body = data.get('body')

            if not all([topic, title, body]):
                return {
                    "success": False,
                    "error": "Missing required fields (topic, title, or body)"
                }, 400

            # Create the message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                topic=topic
            )

            # Send the message
            response = messaging.send(message)
            
            return {
                "success": True,
                "response": response,
                "message": f"Successfully sent message to topic: {topic}"
            }, 200

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }, 500

    @staticmethod
    def subscribe_to_topic(data):
        """
        Subscribe a device or multiple devices to a topic
        
        Args:
            data (dict): Contains registration_tokens and topic
        
        Returns:
            tuple: (response_dict, status_code)
        """
        try:
            registration_tokens = data.get('registration_tokens')
            topic = data.get('topic')

            if not registration_tokens or not topic:
                return {
                    "success": False,
                    "error": "Missing required fields (registration_tokens or topic)"
                }, 400

            if not isinstance(registration_tokens, list):
                registration_tokens = [registration_tokens]

            # Subscribe devices to the topic
            response = messaging.subscribe_to_topic(registration_tokens, topic)
            
            return {
                "success": True,
                "response": response,
                "message": f"Successfully subscribed {len(registration_tokens)} devices to topic: {topic}"
            }, 200

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }, 500

    @staticmethod
    def unsubscribe_from_topic(data):
        """
        Unsubscribe a device or multiple devices from a topic
        
        Args:
            data (dict): Contains registration_tokens and topic
        
        Returns:
            tuple: (response_dict, status_code)
        """
        try:
            registration_tokens = data.get('registration_tokens')
            topic = data.get('topic')

            if not registration_tokens or not topic:
                return {
                    "success": False,
                    "error": "Missing required fields (registration_tokens or topic)"
                }, 400

            if not isinstance(registration_tokens, list):
                registration_tokens = [registration_tokens]

            # Unsubscribe devices from the topic
            response = messaging.unsubscribe_from_topic(registration_tokens, topic)
            
            return {
                "success": True,
                "response": response,
                "message": f"Successfully unsubscribed {len(registration_tokens)} devices from topic: {topic}"
            }, 200

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }, 500
