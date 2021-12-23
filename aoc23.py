#!/usr/bin/env python3
import sortedcontainers
import math
import itertools
from collections import defaultdict
from enum import Enum, auto
import utils
from typing import Tuple, Optional, NamedTuple


class Species(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()


MOVE_COSTS = {
    Species.A: 1,
    Species.B: 10,
    Species.C: 100,
    Species.D: 1000,
}


class CellKind(Enum):
    Hallway = auto()
    RoomExit = auto()
    Room = auto()


class Pod(NamedTuple):
    id: int
    species: Species

    def move_cost(self):
        return MOVE_COSTS[self.species]

    def render(self):
        return self.species.name


class Cell(NamedTuple):
    id: int
    kind: CellKind
    neighbours: Tuple[int]
    render_x: int
    render_y: int
    room_species: Optional[Species] = None
    room_continuation: Tuple[int] = tuple()


PODS = [
    Pod(id=id, species=species) for id, species in enumerate(res for s in Species for res in itertools.repeat(s, 4))
]

MAP = [
    Cell(0, CellKind.Hallway, (1,), 1, 1),
    Cell(1, CellKind.Hallway, (0, 2), 2, 1),
    Cell(2, CellKind.RoomExit, (1, 3, 11), 3, 1),
    Cell(3, CellKind.Hallway, (2, 4), 4, 1),
    Cell(4, CellKind.RoomExit, (3, 5, 15), 5, 1),
    Cell(5, CellKind.Hallway, (4, 6), 6, 1),
    Cell(6, CellKind.RoomExit, (5, 7, 19), 7, 1),
    Cell(7, CellKind.Hallway, (6, 8), 8, 1),
    Cell(8, CellKind.RoomExit, (7, 9, 23), 9, 1),
    Cell(9, CellKind.Hallway, (8, 10), 10, 1),
    Cell(10, CellKind.Hallway, (9,), 11, 1),
    Cell(11, CellKind.Room, (2, 12), 3, 2, room_species=Species.A, room_continuation=(12, 13, 14)),
    Cell(12, CellKind.Room, (11, 13), 3, 3, room_species=Species.A, room_continuation=(13, 14)),
    Cell(13, CellKind.Room, (12, 14), 3, 4, room_species=Species.A, room_continuation=(14,)),
    Cell(14, CellKind.Room, (13,), 3, 5, room_species=Species.A),
    Cell(15, CellKind.Room, (4, 16), 5, 2, room_species=Species.B, room_continuation=(16, 17, 18)),
    Cell(16, CellKind.Room, (15, 17), 5, 3, room_species=Species.B, room_continuation=(17, 18)),
    Cell(17, CellKind.Room, (16, 18), 5, 4, room_species=Species.B, room_continuation=(18,)),
    Cell(18, CellKind.Room, (17,), 5, 5, room_species=Species.B),
    Cell(19, CellKind.Room, (6, 20), 7, 2, room_species=Species.C, room_continuation=(20, 21, 22)),
    Cell(20, CellKind.Room, (19, 21), 7, 3, room_species=Species.C, room_continuation=(21, 22)),
    Cell(21, CellKind.Room, (20, 22), 7, 4, room_species=Species.C, room_continuation=(22,)),
    Cell(22, CellKind.Room, (21,), 7, 5, room_species=Species.C),
    Cell(23, CellKind.Room, (8, 24), 9, 2, room_species=Species.D, room_continuation=(24, 25, 26)),
    Cell(24, CellKind.Room, (23, 25), 9, 3, room_species=Species.D, room_continuation=(25, 26)),
    Cell(25, CellKind.Room, (24, 26), 9, 4, room_species=Species.D, room_continuation=(26,)),
    Cell(26, CellKind.Room, (25,), 9, 5, room_species=Species.D),
]


def room_filled_fully(blocked_cells, current_cell, pod):
    for cell in current_cell.room_continuation:
        occupant_id = blocked_cells.get(cell)
        if occupant_id is None:
            return False
        if PODS[occupant_id].species != pod.species:
            return False
    return True


def room_has_other_species(blocked_cells, current_cell, pod):
    for cell in current_cell.room_continuation:
        occupant_id = blocked_cells.get(cell)
        if occupant_id is not None and PODS[occupant_id].species != pod.species:
            return True
    return False


class GameState(NamedTuple):
    positions: Tuple[int]

    def render(self):
        result = [["#"] * 13 for i in range(7)]
        busy_cells = {cell_id: PODS[pod] for pod, cell_id in enumerate(self.positions)}
        for cell_id, cell in enumerate(MAP):
            pod = busy_cells.get(cell_id)
            result[cell.render_y][cell.render_x] = "." if pod is None else pod.species.name
        for x in range(2):
            for y in range(4):
                result[y + 3][x] = " "
                result[y + 3][-x - 1] = " "
        return "\n".join("".join(line) for line in result) + "\n"

    @staticmethod
    def parse(src):
        available_pods = defaultdict(set)
        for pod in PODS:
            available_pods[pod.species.name].add(pod)
        positions = [-1 for pod in PODS]
        for cell_id, cell in enumerate(MAP):
            char = src[cell.render_y][cell.render_x]
            if char in ("A", "B", "C", "D"):
                pod = available_pods[char].pop()
                positions[pod.id] = cell_id
        if any(p == -1 for p in positions):
            raise ValueError(f"invalid positions: {positions}")
        return GameState(tuple(positions))

    def move(self, pod, cell_id):
        return GameState(positions=self.positions[: pod.id] + (cell_id,) + self.positions[pod.id + 1 :])

    def pod_transitions(self, pod, blocked_cells, start, current, prev, cost):
        if current.room_species == pod.species:
            if room_filled_fully(blocked_cells, current, pod):
                # same species occupies the rest of the room, if any
                return

        next_cost = cost + pod.move_cost()
        for neighbour_id in current.neighbours:
            neighbour = MAP[neighbour_id]

            if prev and neighbour_id == prev.id:
                # came from there
                continue

            if neighbour_id in blocked_cells:
                # can't move, occupied
                continue

            next_state = self.move(pod, neighbour_id)
            can_stop = True

            if neighbour.kind == CellKind.RoomExit:
                can_stop = False
            elif neighbour.kind == CellKind.Room and neighbour.room_species != pod.species:
                if start.room_species == neighbour.room_species:
                    # we can leave wrong rooms
                    can_stop = False
                else:
                    # we won't go into wrong rooms
                    return
            elif neighbour.kind == CellKind.Room:
                if start.room_species != pod.species and room_has_other_species(blocked_cells, neighbour, pod):
                    # don't enter rooms occupied by strangers
                    continue

                if neighbour.room_continuation:
                    next_occupant = blocked_cells.get(neighbour.room_continuation[0])
                    if next_occupant is None or next_occupant == pod.id:
                        can_stop = False
            elif start.kind == CellKind.Hallway and neighbour.kind != CellKind.Room:
                can_stop = False

            if can_stop:
                yield pod, next_cost, next_state

            yield from next_state.pod_transitions(
                pod,
                blocked_cells=blocked_cells,
                start=start,
                current=neighbour,
                prev=current,
                cost=next_cost,
            )

    def transitions(self):
        blocked_cells = {cell_id: pod_id for pod_id, cell_id in enumerate(self.positions)}

        for pod in PODS:
            current_position = self.positions[pod.id]
            yield from self.pod_transitions(
                pod,
                blocked_cells,
                start=MAP[current_position],
                current=MAP[current_position],
                prev=None,
                cost=0,
            )

    def solved(self):
        for pod in PODS:
            pod_cell = MAP[self.positions[pod.id]]
            if pod_cell.room_species != pod.species:
                return False
        return True


class PendingState(NamedTuple):
    cost: int
    state: GameState


def solve(state):
    costs = {state: 0}
    iterations = 0

    pending = sortedcontainers.SortedSet()
    pending.add(PendingState(cost=0, state=state))

    while pending:
        elem = pending.pop(0)
        current_state = elem.state
        current_cost = costs[current_state]
        iterations += 1
        if iterations % 10000 == 0:
            print(f"considering state with cost {current_cost} ({iterations} examined, {len(pending)} pending)")
            print(current_state.render())
        if current_state.solved():
            print(f"solution with cost {current_cost}")
            return

        for pod, move_cost, next_state in current_state.transitions():
            next_cost = current_cost + move_cost
            existing_cost = costs.get(next_state, math.inf)
            if next_cost < existing_cost:
                try:
                    pending.remove(PendingState(cost=existing_cost, state=next_state))
                except KeyError:
                    pass
                costs[next_state] = next_cost
                pending.add(PendingState(cost=next_cost, state=next_state))


def debug_transitions(state):
    print(state.render())
    for pod, cost, next_state in state.transitions():
        print(f"pod {pod}, cost {cost}")
        print(next_state.render())


def main():
    state = GameState.parse(utils.test_input().read().split("\n"))
    # debug_transitions(state)
    solve(state)


if __name__ == "__main__":
    main()
