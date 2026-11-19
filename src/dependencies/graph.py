
ROOT_DEPTH = 0
DEPTH_INCREMENT = 1


def build_dependency_graph(root_package, dependency_provider, max_depth):
    """Строит граф зависимостей рекурсивным обходом DFS."""
    graph = {}
    visited_depth = {}
    active_path = []
    cycles = []

    def dfs(package, depth):
        """Рекурсивно обходит зависимости текущего пакета."""
        if package in active_path:
            cycle_start = active_path.index(package)
            cycle = active_path[cycle_start:] + [package]

            if cycle not in cycles:
                cycles.append(cycle)

            return

        previous_depth = visited_depth.get(package)

        if previous_depth is not None and previous_depth <= depth:
            return

        visited_depth[package] = depth
        graph.setdefault(package, [])

        if depth >= max_depth:
            return

        active_path.append(package)
        dependencies = dependency_provider(package)
        graph[package] = dependencies

        for dependency in dependencies:
            dfs(dependency, depth + DEPTH_INCREMENT)

        active_path.pop()

    dfs(root_package, ROOT_DEPTH)

    return graph, cycles
