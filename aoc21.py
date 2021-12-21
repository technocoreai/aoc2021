#!/usr/bin/env python3
from collections import Counter
import itertools
from typing import NamedTuple


class Player(NamedTuple):
    id: int
    position: int
    score: int = 0

    def move(self, roll):
        new_position = (self.position + roll - 1) % 10 + 1
        return Player(id=self.id, position=new_position, score=self.score + new_position)


ROLLS = Counter(sum(v) for v in itertools.product([1, 2, 3], repeat=3))


def play(active_player, other_player, limit, current_universes=1):
    for roll, universes in ROLLS.items():
        updated_player = active_player.move(roll)
        if updated_player.score >= limit:
            yield (updated_player.id, current_universes * universes)
        else:
            yield from play(
                other_player,
                updated_player,
                limit,
                current_universes=current_universes * universes,
            )


def main():
    total_wins = Counter()
    iterations = 0
    for player, wins in play(Player(id=1, position=1), Player(id=2, position=6), limit=21):
        total_wins[player] += wins
        iterations += 1
        if iterations % 100000 == 0:
            print(iterations, total_wins)
    print()
    for wins, player in sorted((v, i) for i, v in total_wins.items()):
        print(f"player {player}: {wins}")


if __name__ == "__main__":
    main()
