import hid

dict_devices = {}

def list_hid_devices():
    devices = hid.enumerate()
    for device in devices:
        # print(f"Device: {device}")
        dict_devices[(device["vendor_id"], device["product_id"])] = device

def read_hid_device(vendor_id, product_id):
    try:
        # device = hid.Device(vendor_id, product_id)
        
        device_info = dict_devices[(vendor_id, product_id)]
        
        print(f"Device manufacturer: {device_info["manufacturer_string"]}")
        print(f"Product: {device_info["product_string"]}")
        print(f"Serial Number: {device_info["serial_number"]}")


        device = hid.device()
        device.open(vendor_id, product_id)       
        while True:
            data = device.read(64)  # Reading 64 bytes

            if data:
                print(f"Data read from device: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Listing all HID devices:")
    list_hid_devices()
    
    # Example vendor ID and product ID, replace with your device's IDs
    VENDOR_ID = 1155
    PRODUCT_ID = 22352
    
    print("Reading from specific HID device:")
    read_hid_device(VENDOR_ID, PRODUCT_ID)
