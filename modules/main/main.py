from NetworkUser import NetworkUser
from wifi_scanner import scan as wifi_scan
from bluetooth_scanner import scan as bluetooth_scan
from database import Database


# dict of mac_address: NetworkUser key value pairs
active_users = {}

# init db
db = Database()


def main_loop():
    # Get scan results from wifi and bluetooth scans
    devices = wifi_scan() + bluetooth_scan()
    device_macs = [x[0] for x in devices]

    # Add/Update devices
    for mac, signal_strength in devices:
        # If already being tracked update with new signal strength
        if mac in active_users:
            active_users[mac].update(signal_strength)
        else:
            active_users[mac] = NetworkUser(mac, signal_strength)

    # Check for devices not present anymore and remove them from the active_users list
    # and add them to the database
    for mac in active_users.keys():
        if mac not in device_macs:
            # Send data from that device to the database
            db.send_data(active_users[mac])

            # Delete device from active_users
            del active_users[mac]
