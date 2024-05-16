import pyroute2
import scapy.all


def get_default_route():
    ip = pyroute2.IPRoute()
    routes = ip.get_routes()

    default_route = None
    for route in routes:
        if (
            route.get_attr("RTA_DST") is None
            and route.get_attr("RTA_GATEWAY") is not None
        ):
            default_route = route
            break

    ip.close()
    return default_route


def perform_traceroute(target):
    result, unans = scapy.all.traceroute(target, maxttl=20, verbose=True)
    return result


def analyze_routes(output_func=print):
    output_func("Default Route:")
    default_route = get_default_route()
    if default_route:
        output_func(f"Destination: {default_route.get_attr('RTA_DST')}")
        output_func(f"Gateway: {default_route.get_attr('RTA_GATEWAY')}")
        output_func(f"Interface: {default_route.get_attr('RTA_OIF')}")
    else:
        output_func("No default route found.")

    output_func("\nTraceroute:")
    target = "www.example.com"
    traceroute_result = perform_traceroute(target)
    traceroute_result.show()
