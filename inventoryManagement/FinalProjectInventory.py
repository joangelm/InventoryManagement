import datetime
import csv


# Class to manage devices and reports
class Inventory:
    def __init__(self):
        self.inventory_list = {}

    def add(self, device):
        self.inventory_list[device.item_ID] = device

    def get(self, device_ID):
        return self.inventory_list[device_ID]

    def find(self, manufacturer, device_type):
        today = datetime.datetime.today()
        found_device = False

        for device in self.devices():
            # Convert device service date from string to datetime object
            service_date = datetime.datetime.strptime(device.service_date, "%m/%d/%Y")

            # Check if device is not damaged and not past its service date
            if (not device.damaged) and (service_date >= today):
                # Found matching device in inventory
                if (device.manufacturer_name.strip() == manufacturer) and (device.device_type == device_type):
                    # Found duplicate devices
                    if found_device:
                        # Compare duplicate prices and get most expensive
                        if device.price > found_device.price:
                            found_device = device
                    else:
                        found_device = device

        return found_device

    def findSimilarDevice(self, manufacturer, device_type, price_min, price_max):
        # Get program run date
        today = datetime.datetime.today()

        for device in self.devices():
            # Convert device service date from string to datetime object
            service_date = datetime.datetime.strptime(device.service_date, "%m/%d/%Y")
            # Check if device is not damaged and not past its service date
            if (not device.damaged) and (service_date >= today):
                # Found matching device in inventory
                if (device.manufacturer_name.strip() != manufacturer) and (device.device_type == device_type):
                    # Check if price is similar in price
                    if price_min <= float(device.price) <= price_max:
                        return device

        return False

    # Method to retrieve the inventory's devices
    def devices(self):
        return self.inventory_list.values()

    # Method to create a full inventory report sorted by device manufacturer name in alphabetical order
    def createFullInventory(self):
        with open('FullInventory.csv', 'w', newline='') as csvfile:
            FullInventory_writer = csv.writer(csvfile)

            sorted_list = []

            # Loop through devices in inventory
            for device in self.devices():
                found_position = False

                # Loop through list of devices in sorted list
                for index in range(len(sorted_list)):
                    # Compare manufacturer names alphabetically
                    if device.manufacturer_name < sorted_list[index].manufacturer_name:
                        sorted_list.insert(index, device)
                        found_position = True
                        break
                    # Check if manufacturer names are the same
                    elif device.manufacturer_name == sorted_list[index].manufacturer_name:
                        if device.device_type < sorted_list[index].device_type:
                            sorted_list.insert(index, device)
                        else:
                            sorted_list.insert(index + 1, device)
                        found_position = True
                        break

                # Did not find position to insert device in sorted list (Also when list is empty)
                if not found_position:
                    sorted_list.append(device)

            # Loop through devices in sorted list and create rows in csv file
            for device in sorted_list:
                FullInventory_writer.writerow(
                    [device.item_ID, device.manufacturer_name, device.device_type, device.price, device.service_date,
                     device.damaged])

        csvfile.close()

    def createTypeInventory(self):
        # Create dictionary of device type as Key and a device list as Value
        types = {}

        # Loop through devices in inventory
        for device in self.devices():
            # Check if device type already exists in dictionary
            if device.device_type in types:
                # Sort device list while creating it
                found = False

                # Loop through dictionary
                for index in range(len(types[device.device_type])):
                    # Compare device IDs (Ascending order)
                    if device.item_ID < types[device.device_type][index].item_ID:
                        types[device.device_type].insert(index, device)
                        found = True
                        break
                # Did not find position to insert device in dictionary (Also when list is empty)
                if not found:
                    types[device.device_type].append(device)
            # No type found in dictionary, so create one
            else:
                types[device.device_type] = [device]

        # Create inventory file for device types
        for type, list in types.items():
            file_name = f'{type.title()}Inventory.csv'
            with open(file_name, 'w', newline='') as csvfile:
                TypeInventory_writer = csv.writer(csvfile)
                for device in list:
                    TypeInventory_writer.writerow(
                        [device.item_ID, device.manufacturer_name, device.price, device.service_date, device.damaged])

            csvfile.close()

    def createPastServiceDateInventory(self):
        with open('PastServiceDateInventory.csv', 'w', newline='') as csvfile:
            ServiceDate_writer = csv.writer(csvfile)
            # Get date of program runtime
            today = datetime.datetime.today()
            sorted_list = []

            # Loop through devices in inventory
            for device in self.devices():
                # Convert device service date from string to datetime object
                service_date = datetime.datetime.strptime(device.service_date, "%m/%d/%Y")
                # Check if device service date is in the past
                if service_date < today:
                    found_position = False
                    # Loop through list of devices in sorted list
                    for index in range(len(sorted_list)):
                        # Convert service date from string to datetime object
                        sorted_service_date = datetime.datetime.strptime(sorted_list[index].service_date, "%m/%d/%Y")
                        # Compare device service dates (Oldest to most recent)
                        if service_date < sorted_service_date:
                            sorted_list.insert(index, device)
                            found_position = True
                            break

                    # Did not find position to insert device in sorted list (Also when list is empty)
                    if not found_position:
                        sorted_list.append(device)

            # Write rows for past service date inventory csv file
            for device in sorted_list:
                row_list = [device.item_ID, device.manufacturer_name, device.device_type, device.price,
                            device.service_date]
                if device.damaged == 'damaged':
                    row_list.append(device.damaged)

                ServiceDate_writer.writerow(row_list)

        csvfile.close()

    def createDamagedInventory(self):
        with open('DamagedInventory.csv', 'w', newline='') as csvfile:
            DamagedInventory_writer = csv.writer(csvfile)
            sorted_list = []

            # Loop through devices in inventory
            for device in self.devices():
                # Check if device is damaged
                if device.damaged == 'damaged':
                    found_position = False
                    # Loop through devices in sorted list
                    for index in range(len(sorted_list)):
                        # Compare device prices (Most expensive to least expensive)
                        if device.price > sorted_list[index].price:
                            sorted_list.insert(index, device)
                            found_position = True
                            break

                    # Did not find position to insert device in sorted list (Also when list is empty)
                    if not found_position:
                        sorted_list.append(device)

            # Write rows for damaged inventory csv file
            for device in sorted_list:
                DamagedInventory_writer.writerow(
                    [device.item_ID, device.manufacturer_name, device.device_type, device.price, device.service_date])

        csvfile.close()
