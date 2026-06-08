"""
8 Puzzle Solver - Algoritmo A* com Heurística Manhattan Distance
Autores: Maria Alice Giuliari e Mariele Vieira da Silva
"""

import heapq
import time
from typing import List, Tuple, Optional

# ── Estado do tabuleiro ───────────────────────────────────────────────────────

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)   # 0 representa o espaço vazio
GOAL_POS = {v: (i // 3, i % 3) for i, v in enumerate(GOAL)}

def manhattan(state: tuple) -> int:
    """Heurística: soma das distâncias Manhattan de cada peça."""
    dist = 0
    for i, tile in enumerate(state):
        if tile != 0:
            r, c = i // 3, i % 3
            gr, gc = GOAL_POS[tile]
            dist += abs(r - gr) + abs(c - gc)
    return dist

def neighbors(state: tuple) -> List[Tuple[tuple, str]]:
    """Retorna estados vizinhos e o movimento realizado."""
    zero = state.index(0)
    r, c = zero // 3, zero % 3
    moves = []
    directions = [(-1, 0, "↓"), (1, 0, "↑"), (0, -1, "→"), (0, 1, "←")]
    # Direção do vazio → peça que se move é o oposto
    for dr, dc, label in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            ni = nr * 3 + nc
            lst = list(state)
            lst[zero], lst[ni] = lst[ni], lst[zero]
            moves.append((tuple(lst), label))
    return moves

# ── A* ────────────────────────────────────────────────────────────────────────

def astar(start: tuple) -> Optional[List[tuple]]:
    """Retorna lista de estados do início ao goal, ou None se sem solução."""
    h = manhattan(start)
    # heap: (f, g, state, path)
    heap = [(h, 0, start, [start])]
    visited = set()

    while heap:
        f, g, state, path = heapq.heappop(heap)
        if state == GOAL:
            return path
        if state in visited:
            continue
        visited.add(state)
        for nxt, _ in neighbors(state):
            if nxt not in visited:
                ng = g + 1
                nf = ng + manhattan(nxt)
                heapq.heappush(heap, (nf, ng, nxt, path + [nxt]))
    return None

# ── Solucionabilidade ─────────────────────────────────────────────────────────

def is_solvable(state: tuple) -> bool:
    """Conta inversões; puzzle é solucionável se número de inversões é par."""
    tiles = [t for t in state if t != 0]
    inv = sum(tiles[i] > tiles[j]
                for i in range(len(tiles))
                for j in range(i + 1, len(tiles)))
    return inv % 2 == 0

# ── Representação textual ─────────────────────────────────────────────────────

def print_board(state: tuple):
    for i in range(3):
        row = state[i*3:(i+1)*3]
        print("+---+---+---+")
        print("| " + " | ".join(str(x) if x else " " for x in row) + " |")
    print("+---+---+---+")

def move_label(a: tuple, b: tuple) -> str:
    """Qual peça se moveu e em que direção."""
    zi = a.index(0)
    pi = b.index(0)   # posição anterior do vazio = posição atual da peça
    tile = a[pi]
    dr = (zi // 3) - (pi // 3)
    dc = (zi % 3) - (pi % 3)
    arrows = {(-1,0):"↑",(1,0):"↓",(0,-1):"←",(0,1):"→"}
    return f"Peça {tile} move {arrows.get((dr,dc),'?')}"

# ── Demo CLI ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random, sys

    # Estado inicial de exemplo
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)

    if "--random" in sys.argv:
        while True:
            s = list(range(9))
            random.shuffle(s)
            start = tuple(s)
            if is_solvable(start):
                break

    print("\n🧩  8 PUZZLE SOLVER  –  Algoritmo A*\n")
    print("Estado inicial:")
    print_board(start)

    if not is_solvable(start):
        print("❌ Este estado não tem solução!")
        sys.exit(1)

    t0 = time.time()
    path = astar(start)
    elapsed = time.time() - t0

    if not path:
        print("Sem solução encontrada.")
        sys.exit(1)

    print(f"\n✅ Solução encontrada em {len(path)-1} movimentos  ({elapsed:.3f}s)\n")
    for step, (a, b) in enumerate(zip(path, path[1:]), 1):
        print(f"Passo {step:02d}: {move_label(a, b)}")
        print_board(b)
