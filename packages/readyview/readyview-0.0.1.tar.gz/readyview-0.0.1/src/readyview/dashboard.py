class Dashboard:
    def __init__(self, shipment_id, tracking_number):
        self.organization_id = shipment_id
        self.api_key = tracking_number

    def display_info(self):
        return (
            f"Org ID: {self.organization_id}\n"
            f"API Key: {self.api_key}\n"
        )
