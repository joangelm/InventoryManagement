# Class to handle device data
class Device:
    def __init__(self, item_ID='', manufacturer_name='', device_type='', price='', service_date='', damaged=''):
        self.item_ID = item_ID
        self.manufacturer_name = manufacturer_name
        self.device_type = device_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged
