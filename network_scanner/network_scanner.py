from scapy.all import ARP, Ether, conf, get_if_hwaddr, srp, show_interfaces
from bidict import bidict

def _format_ip_range(ip_range):
    """
    Formats the IP range to ensure it is in the correct format for scanning.
    :param ip_range: The IP range to format (e.g., '192.168.27.0/24')
    :returns: The formatted IP range
    """
    
    ip = ip_range.strip().split('/')  # Remove any whitespace and subnet mask

    if len(ip) != 2:
        raise ValueError("Invalid IP range format. Please provide a valid IP range (e.g., '192.168.27.0/`24').")

    subnet_range, subnet_mask = ip[0], ip[1]
    subnet_range_parts = subnet_range.split('.')

    # Ensure ip part is of x.x.x.x format and each part is between 0 and 255
    if len(subnet_range_parts) != 4 or \
        not all(
            ip_part.isdigit() and \
                0 <= int(ip_part) <= 255 \
                    for ip_part in subnet_range_parts
                ):
        raise ValueError("Invalid IP range format. Please provide a valid IP range (e.g., '192.168.27.0/`24').")
    
    if not (subnet_mask.isdigit() and 0 <= int(subnet_mask) <= 32):
        raise ValueError("Invalid subnet mask. Please provide a valid subnet mask (e.g., '24').")
    
    return f"{subnet_range}/{subnet_mask}"



def _get_interface(formatted_ip_range):
    """
    Determines the best network interface to use for scanning based on the provided IP range.
    :param formatted_ip_range: The formatted IP range to scan (e.g., '192.168.27.0/24')
    :returns: The interface's name, local IP address, and gateway for the best matching route
    """
    base_ip = formatted_ip_range.split('/')[0]

    try:
        interface, local_ip, gateway = conf.route.route(base_ip, verbose=False)
        return interface, local_ip, gateway
    except Exception as e:
        print(f"Error: Could not resolve a route to {base_ip}. Details: {e}")
        raise


def _get_active_hosts(answered_list):
    """
    Formats the list of answered ARP requests to extract active hosts and their MAC addresses.
    :param answered_list: The list of answered ARP requests
    :returns: A bidirectional dictionary containing active IPs and their corresponding MAC addresses
    """
    host_dict = bidict() # bidirectional dictionary to store IP-MAC pairs

    for sent, received in answered_list:
        host_dict.update({received.psrc: received.hwsrc})

    return host_dict


def active_scan(ip_range):
    """
    Scans the specified IP range for active hosts using ARP requests.
    :param ip_range: The IP range to scan (e.g., '192.168.27.0/24')
    :returns: A list of active IPs and their MAC addresses in the specified IP range
    """
    formatted_ip_range = _format_ip_range(ip_range)
    interface, local_ip, _ = _get_interface(formatted_ip_range)
    adapter_mac = get_if_hwaddr(interface)

    arp = ARP(pdst=formatted_ip_range, psrc=local_ip, hwsrc=adapter_mac)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = ether / arp
    answered_list, unanswered_list = srp(arp_request_broadcast, iface=interface, timeout=1, verbose=False)

    return _get_active_hosts(answered_list)
    

if __name__ == '__main__':
    active_scan('192.168.227.0/24')