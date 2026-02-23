def build_causal_graph(timeline: dict):
    graph = {}
    ordered_services = list(timeline.keys())

    for i, service in enumerate(ordered_services[:-1]):
        graph[service] = ordered_services[i + 1:]

    return graph