import ipaddress

import netifaces
import requests


def get_ip_addresses():
    ip_list = []
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip_list.append((addr["addr"], True))
        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                ip_list.append((addr["addr"].split("%")[0], True))
    return ip_list


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        data = response.json()
        return data["ip"], False
    except requests.exceptions.RequestException:
        return None, False


def analyze_ip(ip_info, output_func):
    ip, is_local_interface = ip_info
    if "%" in ip:
        ip, scope_id = ip.split("%")
    else:
        pass

    addr = ipaddress.ip_address(ip)

    output_func(
        f"IPAddress: {ip:<25} | "
        f"IPVersion: {'IPv4' if addr.version == 4 else 'IPv6':<4} | "
        f"IsPrivate: {str(addr.is_private):<5} | "
        f"IsGlobal: {str(addr.is_global):<5} | "
        f"IsMulticast: {str(addr.is_multicast):<5} | "
        f"IsReserved: {str(addr.is_reserved):<5} | "
        f"IsLoopback: {str(addr.is_loopback):<5} | "
        f"IsLink-local: {str(addr.is_link_local):<5} | "
        f"IsLocalInterface: {str(is_local_interface):<5}"
    )


def analyze_ips(output_func=print):
    ip_list = get_ip_addresses()
    for ip_info in ip_list:
        analyze_ip(ip_info, output_func)

    public_ip_info = get_public_ip()
    if public_ip_info[0]:
        analyze_ip(public_ip_info, output_func)
    else:
        output_func("Unable to retrieve the public IP address.")
