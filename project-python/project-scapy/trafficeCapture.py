from scapy.all import sniff

# Define a callback to process each packet
def packet_callback(packet):
    print(packet.summary())

# Sniff packets on interface (e.g., eth0 or wlan0)
# count=0 -> infinite capture, use count=N for limited packets
# store=0 -> do not store in memory (for performance)
sniff(iface="en7", prn=packet_callback, count=0, store=0)
