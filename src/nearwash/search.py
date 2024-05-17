import ipaddress

from .ip_analyzer import get_ip_addresses
from .route import get_default_route


def find_minimal_cidr_range(start_ip_str, target_ip_str):
    start_ip = ipaddress.ip_address(start_ip_str.split("%")[0])
    target_ip = ipaddress.ip_address(target_ip_str)

    for prefix in range(32, 0, -1):
        network = ipaddress.ip_network(f"{start_ip}/{prefix}", strict=False)
        if target_ip in network:
            return network
    return None


def main(args, output_func):
    default_route = get_default_route()
    if not default_route:
        output_func("No default gateway found.")
        return

    gateway_ip = default_route.get_attr("RTA_GATEWAY")
    if args.verbose:
        output_func(f"Default Gateway IP: {gateway_ip}")

    ip_list = get_ip_addresses()
    results = []
    for ip_info in ip_list:
        target_ip, _ = ip_info
        network = find_minimal_cidr_range(target_ip, gateway_ip)
        if network:
            results.append((target_ip, network))

    results.sort(key=lambda x: x[1].prefixlen, reverse=True)

    if args.verbose:
        for target_ip, network in results:
            output_func(f"Target IP: {target_ip}, Minimal CIDR range: {network}")
    else:
        if results:
            target_ip, network = results[0]
            output_func(f"{target_ip}")
        else:
            output_func(f"No CIDR range found that includes {gateway_ip}")


if __name__ == "__main__":
    main(print)
