import argparse

from . import ip_analyzer, route
from . import search as searchmod

__project_name__ = "nearwash"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Nearwash network analysis tool", add_help=False
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser(
        "report", help="Generate network analysis report"
    )
    report_parser.set_defaults(func=report)

    search_parser = subparsers.add_parser(
        "search", help="Search for specific gateway and target IP addresses"
    )
    search_parser.add_argument(
        "--gateway-ip", required=True, help="Gateway IP address to search for"
    )
    search_parser.add_argument(
        "--target-ip", required=True, help="Target IP address to search for"
    )
    search_parser.set_defaults(func=search)

    return parser.parse_args()


def report(args, output_func=print):
    ip_analyzer.analyze_ips(output_func)
    route.analyze_routes(output_func)


def search(args, output_func=print):
    searchmod.main(args, output_func)
    output_func(f"Searching for gateway IP: {args.gateway_ip}")
    output_func(f"Searching for target IP: {args.target_ip}")


def main(output_func=print) -> int:
    args = parse_args()
    args.func(args, output_func)
    return 0
