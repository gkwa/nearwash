import ipaddress


def find_minimal_cidr_range(start_ip_str, target_ip_str):
    start_ip = ipaddress.ip_address(start_ip_str)
    target_ip = ipaddress.ip_address(target_ip_str)

    for prefix in range(32, 0, -1):
        network = ipaddress.ip_network(f"{start_ip}/{prefix}", strict=False)
        if target_ip in network:
            return network
    return None


def main(args, output_func):
    network = find_minimal_cidr_range(args.target_ip, args.gateway_ip)

    if network:
        output_func(
            f"The minimal CIDR range starting from {args.target_ip} that includes {args.gateway_ip} is {network}"
        )

    else:
        output_func(f"No CIDR range found that includes {args.gateway_ip}")


if __name__ == "__main__":
    main()
