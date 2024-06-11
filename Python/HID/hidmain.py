import os
import sys
import hid
from pynput.keyboard import Controller
import msvcrt

# File lock path
LOCK_FILE = 'hid_script.lock'

# Dictionary to store HID devices
dict_devices = {}

def list_hid_devices():
    """
    Lists all HID devices and stores their information in a dictionary.
    """
    devices = hid.enumerate()
    for device in devices:
        dict_devices[(device["vendor_id"], device["product_id"])] = device

def read_hid_device(vendor_id, product_id):
    """
    Reads data from the specified HID device and simulates key presses.
    
    Parameters:
        vendor_id (int): The vendor ID of the HID device.
        product_id (int): The product ID of the HID device.
    """
    try:
        # Retrieve device info from the dictionary
        device_info = dict_devices[(vendor_id, product_id)]
        
        print(f"Device manufacturer: {device_info['manufacturer_string']}")
        print(f"Product: {device_info['product_string']}")
        print(f"Serial Number: {device_info['serial_number']}")
        
        # Open the HID device
        device = hid.Device(vendor_id, product_id)
        
        # Initialize the keyboard controller
        keyboard = Controller()
        
        print("Reading data from device (press Ctrl+C to stop):")
        while True:
            try:
                # Read 64 bytes of data from the device
                data = device.read(64)
                if data:
                    print(f"Data read from device: {data}")
                    # Simulate pressing 'a' key when data is read
                    keyboard.press('a')
                    keyboard.release('a')
            except KeyboardInterrupt:
                print("Stopping reading from device.")
                break
            except Exception as read_error:
                print(f"Error reading from device: {read_error}")
                break
    except KeyError:
        print(f"No device found with vendor_id {vendor_id} and product_id {product_id}.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            device.close()
        except:
            pass

def acquire_lock(lock_file):
    """
    Acquires a file lock to prevent multiple script instances.
    
    Parameters:
        lock_file (str): Path to the lock file.
    
    Returns:
        file: The file handle to the lock file.
    """
    lock_fd = open(lock_file, 'w')
    try:
        msvcrt.locking(lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
        return lock_fd
    except IOError:
        print("Another instance of this script is already running.")
        sys.exit(1)

if __name__ == "__main__":
    # Acquire the file lock
    lock_fd = acquire_lock(LOCK_FILE)

    print("Listing all HID devices:")
    list_hid_devices()
    
    # Example vendor ID and product ID, replace with your device's IDs
    VENDOR_ID = 1155
    PRODUCT_ID = 22352
    
    print("Reading from specific HID device:")
    read_hid_device(VENDOR_ID, PRODUCT_ID)
    
    # Release the lock (automatically done when the script exits)
    msvcrt.locking(lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
    lock_fd.close()
