#!/usr/bin/env python3
from functools import lru_cache
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


@lru_cache(1024000)
def play_memo(active_player, other_player, limit):
    result = Counter()
    for roll, universes in ROLLS.items():
        updated_player = active_player.move(roll)
        if updated_player.score >= limit:
            result[updated_player.id] += universes
        else:
            result += {k: v * universes for k, v in play_memo(other_player, updated_player, limit).items()}
    return result


def main():
    total_wins = play_memo(Player(id=1, position=1), Player(id=2, position=6), limit=21)
    for wins, player in sorted((v, i) for i, v in total_wins.items()):
        print(f"player {player}: {wins}")


if __name__ == "__main__":
    main()
