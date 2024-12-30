import requests
import json

class Sender:
    def __init__(self, token):
        self.TOKEN = token

    def _send_request(self, url, payload, files=None):
        """Helper method to send requests and handle responses."""
        try:
            response = requests.post(url, data=payload, files=files).json()
            if response.get("ok"):
                print(f"Message successfully sent.")
                return True
            else:
                print(f"Message failed to send: {response.get('description')}", flush=True)
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}", flush=True)
            return False

    def send_text(self, chat_id=None, message=None, buttons=None):
        """Send a text message."""
        if not message:
            print("Error: A message must be provided.")
            return False
        
        reply_markup = self._prepare_buttons(buttons)
        
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "reply_markup": reply_markup
        }
        
        return self._send_request(url, payload)

    def send_image(self, chat_id=None, base64_image_data=None, message=None, buttons=None):
        """Send an image with an optional caption."""
        if not base64_image_data:
            print("Error: Base64 image data must be provided.")
            return False
        
        reply_markup = self._prepare_buttons(buttons)
        
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendPhoto"
        files = {"photo": base64_image_data}
        payload = {
            "chat_id": chat_id,
            "caption": message or "",
            "reply_markup": json.dumps(reply_markup)
        }

        return self._send_request(url, payload, files)

    def _prepare_buttons(self, buttons):
        """Prepare the buttons for inline keyboard if provided."""
        if buttons:
            return {
                "inline_keyboard": [[{"text": button["text"], "url": button["url"]}] for button in buttons]
            }
        return None
