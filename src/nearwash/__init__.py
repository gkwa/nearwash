from . import ip_analyzer, route

__project_name__ = "nearwash"


def main(output_func=print) -> int:
    ip_analyzer.analyze_ips(output_func)
    route.analyze_routes(output_func)
    return 0
