import argparse

from . import ip_analyzer, route

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

    return parser.parse_args()


def report(args, output_func=print):
    ip_analyzer.analyze_ips(output_func)
    route.analyze_routes(output_func)


def main(output_func=print) -> int:
    args = parse_args()
    args.func(args, output_func)
    return 0
