class NotificationService:
    def send_notification(self, message: str):
        """
        Notifies about the scraping status. Can be extended to use email or other notification services.
        """
        print(message)
