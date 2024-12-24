from heapq import heapify, heappop, heappush

from .constants import Direction
from .coordinate import Coordinate


class Graph:
    def __init__(self):
        self.graph : dict[Coordinate, dict[Coordinate, int]] = {}
        self.start_coordinate: Coordinate
        self.end_coordinate: Coordinate
        self.best_tiles: set = set()

    def add_edge(self, n1: Coordinate, n2: Coordinate, weight: int = 1):
        if self.graph.get(n1) is None:
            self.graph[n1] = {}
        self.graph[n1][n2] = weight

    def from_aoc_input(self, grid: list[list[str]]) -> None:
        row_limit = len(grid)
        col_limit = len(grid[0])
        for row_num, row in enumerate(grid):
            for col_num, col in enumerate(row):
                n1 = Coordinate(row_num, col_num, col)
                if col == "#":
                    continue
                elif col == "S":
                    self.start_coordinate = n1
                    self.start_coordinate.direction = Direction.east
                elif col == "E":
                    self.end_coordinate = n1
                surrounding_nodes = n1.next_nodes(row_limit, col_limit, grid)
                for i in surrounding_nodes:
                    if i.value != "#":
                        self.add_edge(n1, i)
        return self

    def shortest_path(self) -> dict[Coordinate, int]:
        if not self.graph:
            raise ValueError("graph has not been initialized!")
        visited_nodes: set = set()
        distances = {node: float("inf") for node in self.graph}
        distances[self.start_coordinate] = 0
        priority_queue = [(0, self.start_coordinate)]
        heapify(priority_queue)

        while priority_queue:
            current_distance, node = heappop(priority_queue)
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            for neighbor_node, _ in self.graph[node].items():
                distance, neighbor_direction = node.get_score_to_neighbor(neighbor=neighbor_node)
                neighbor_node.direction = neighbor_direction
                tentative_distance = current_distance + distance
                if neighbor_node.value == "E":
                    print(f" [o] Reached E, current tentative dist: {tentative_distance}")
                if tentative_distance <= distances[neighbor_node]:
                    self.best_tiles.add(node)
                    distances[neighbor_node] = tentative_distance
                    heappush(priority_queue, (tentative_distance, neighbor_node))
        return distances
