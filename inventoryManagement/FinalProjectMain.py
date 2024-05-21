import csv
from FinalProjectDevice import Device
from FinalProjectInventory import Inventory

# Price threshold to find similar products
PRICE_RANGE = 250

# Create inventory object to hold devices                    
inventory = Inventory()
manufacturers = set()
device_types = set()

# Read in list of devices in ManufactuerList csv file
with open('ManufacturerList.csv', 'r') as csvfile:
    ManufacturerList_reader = csv.reader(csvfile, delimiter=',')

    # Create a new device object for each row in file
    for row in ManufacturerList_reader:
        device = Device()
        device.item_ID = row[0]
        device.manufacturer_name = row[1]
        device.device_type = row[2]
        device.damaged = row[3]

        # Add new device to inventory
        inventory.add(device)

        # Add manufacturers and device types to sets
        manufacturers.add(row[1].strip())
        device_types.add(row[2].strip())

csvfile.close()

# Read in list of device prices in PriceList csv file
with open('PriceList.csv', 'r') as csvfile:
    PriceList_reader = csv.reader(csvfile, delimiter=',')
    # Read in device price data and modify the corresponding device's price
    for row in PriceList_reader:
        device = inventory.get(row[0])
        device.price = row[1]
csvfile.close()

# Read in Service Dates of devices from ServiceDatesList csv file
with open('ServiceDatesList.csv', 'r') as csvfile:
    ServiceDatesList_reader = csv.reader(csvfile, delimiter=',')

    # Read in device service dates and modify the corresponding device's service date
    for row in ServiceDatesList_reader:
        device = inventory.get(row[0])
        device.service_date = row[1]
csvfile.close()

# Calling inventory functions to create csv reports
inventory.createFullInventory()
inventory.createTypeInventory()
inventory.createPastServiceDateInventory()
inventory.createDamagedInventory()

# Keep asking user for queries unless they enter 'q'
while True:
    user_query = input("Please enter item manufacturer and item type:\n")
    if user_query == 'q':
        break

    # Grab correct item from inventory ()
    query_keywords = user_query.strip().split(' ')

    query_manufacturer = ''
    query_device_type = ''

    incorrect_query = False

    for keyword in query_keywords:
        # Find manufacturer and device type in user query
        if keyword in manufacturers:
            if query_manufacturer == '':
                query_manufacturer = keyword
            else:
                incorrect_query = True
                break

        if keyword in device_types:
            if query_device_type == '':
                query_device_type = keyword
            else:
                incorrect_query = True
                break

    if query_manufacturer == '' or query_device_type == '':
        incorrect_query = True

    if incorrect_query:
        print("No such item in inventory")
    else:
        # Query and find device in inventory
        query_device = inventory.find(query_manufacturer, query_device_type)
        if query_device:
            # Print out found device information in inventory
            print("Your item is:", query_device.item_ID, query_device.manufacturer_name, query_device.device_type,
                  query_device.price)
            query_similar_device = inventory.findSimilarDevice(query_manufacturer, query_device_type,
                                                               float(query_device.price) - PRICE_RANGE,
                                                               float(query_device.price) + PRICE_RANGE)
            if query_similar_device:
                # Print out similar product information in inventory
                print("You may, also, consider:", query_similar_device.item_ID, query_similar_device.manufacturer_name,
                      query_similar_device.device_type, query_similar_device.price)
        else:
            print("No such item in inventory")