from scapy.all import ARP, Ether, conf, get_if_hwaddr, srp, show_interfaces


def _format_ip_range(ip_range):
    """
    Formats the IP range to ensure it is in the correct format for scanning.
    :param ip_range: The IP range to format (e.g., '192.168.27.0/24')
    returns the formatted IP range
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
    
    base_ip = formatted_ip_range.split('/')[0]

    try:
        interface, local_ip, gateway = conf.route.route(base_ip)
        print(f"Found best matching route through interface IP {local_ip} with MAC address {get_if_hwaddr(interface)}")
        return interface, local_ip, gateway
    except Exception as e:
        print(f"Error: Could not resolve a route to {base_ip}. Details: {e}")
        raise

