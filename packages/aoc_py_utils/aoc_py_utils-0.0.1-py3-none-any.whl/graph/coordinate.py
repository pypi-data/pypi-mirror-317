from .constants import Direction


class Coordinate:
    def __init__(self, row: int, col: int, value: str, direction: Direction = Direction.not_set):
        self.row = row
        self.col = col
        self.value = value
        self.direction = direction

    def next_nodes(self, r_limit: int, c_limit: int, grid: list[list[str]]) -> list["Coordinate"]:
        retval = []
        # north
        if self.row - 1 >= 0:
            retval.append(Coordinate(self.row - 1, self.col, grid[self.row - 1][self.col]))
        # south
        if self.row + 1 < r_limit:
            retval.append(Coordinate(self.row + 1, self.col, grid[self.row + 1][self.col]))
        # west
        if self.col - 1 >= 0:
            retval.append(Coordinate(self.row, self.col - 1, grid[self.row][self.col - 1]))
        # east
        if self.col + 1 < c_limit:
            retval.append(Coordinate(self.row, self.col + 1, grid[self.row][self.col + 1]))
        return retval

    def get_score_to_neighbor(self, neighbor: "Coordinate") -> tuple[int, Direction]:
        # direction from current coordinate to neighbor
        if neighbor.row == self.row + 1:
            self_to_neighbor = Direction.south
        elif neighbor.row == self.row - 1:
            self_to_neighbor = Direction.north
        elif neighbor.col == self.col - 1:
            self_to_neighbor = Direction.west
        else:
            self_to_neighbor = Direction.east
        difference = abs(self.direction.value - self_to_neighbor.value)
        if difference == 0:
            return 1, self_to_neighbor
        elif difference == 1 or difference == 2:
            return 1000 * difference + 1, self_to_neighbor
        elif difference == 3:
            return 1000 + 1, self_to_neighbor

    def __repr__(self) -> str:
        return f"(row:{self.row}, col:{self.col}, value:{self.value}, dir:{self.direction})"

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __eq__(self, value: "Coordinate"):
        if self.row == value.row and self.col == value.col:
            return True
        return False

    def __lt__(self, value: "Coordinate") -> bool:
        return (self.row, self.col) < (value.row, value.col)

    def __gt__(self, value: "Coordinate") -> bool:
        return (self.row, self.col) > (value.row, value.col)
