<h1 align="center">8 Puzzle Solver</h1>

<p align="center">
  <strong>Algoritmos Avançados — Católica SC</strong><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.16-blue?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/HTML-Visualizacao-yellowgreen?logo=pygame" alt="Pygame"/>
  <img src="https://img.shields.io/badge/Algoritmo-A*-orange" alt="A* Search"/>
</p>

 <h3 align="center">Relatório de como IA ajudou a construir a solução</h3>

---
 
### O Problema

O **8 Puzzle** é um quebra-cabeça clássico de Inteligência Artificial: um tabuleiro 3×3 com 8 peças numeradas e um espaço vazio. O objetivo é deslizar as peças até atingir o estado final `1 2 3 / 4 5 6 / 7 8 ☐`.

É um problema de **busca em espaço de estados**: cada configuração do tabuleiro é um estado, e cada movimento de peça é uma transição.

---

### A Abordagem — Algoritmo A*

A IA escolheu o algoritmo **A\*** (A-estrela) por ser:

- **Ótimo** — garante o menor número de movimentos possível
- **Completo** — sempre encontra a solução (quando ela existe)
- **Eficiente** — muito mais rápido que BFS/DFS puro

#### A Fórmula Central

```
f(n) = g(n) + h(n)
```

| Componente | Significado |
|---|---|
| `f(n)` | Custo total estimado do nó `n` |
| `g(n)` | Custo real do caminho percorrido até `n` (número de movimentos já feitos) |
| `h(n)` | Heurística: estimativa do custo até o objetivo |

#### A Heurística — Distância de Manhattan

Para cada peça fora do lugar, calcula-se quantas casas ela precisa andar (horizontal + vertical) para chegar à posição correta — **sem contar diagonais**, pois o puzzle só permite movimentos ortogonais.

```python
def manhattan(state):
    dist = 0
    for i, tile in enumerate(state):
        if tile != 0:
            r, c = i // 3, i % 3
            gr, gc = GOAL_POS[tile]
            dist += abs(r - gr) + abs(c - gc)
    return dist
```

Exemplo: se a peça `5` está na posição `(0,0)` e deveria estar em `(1,1)`:
- Distância = |0−1| + |0−1| = **2**

A heurística Manhattan é **admissível** (nunca superestima o custo real), o que garante que o A* encontrará a solução ótima.

---

### Verificação de Solucionabilidade

Nem toda configuração do 8 Puzzle tem solução! A IA implementou a verificação por **contagem de inversões**:

```python
def is_solvable(state):
    tiles = [t for t in state if t != 0]
    inversions = sum(
        tiles[i] > tiles[j]
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )
    return inversions % 2 == 0
```

Uma **inversão** ocorre quando um número maior aparece antes de um número menor (ignorando o espaço vazio). Se o total de inversões for **par** → tem solução. Se for **ímpar** → sem solução.

---

### Como a IA Estruturou o Código

#### 1. Representação do Estado
O tabuleiro é representado como uma **tupla de 9 inteiros** (imutável, para poder ser usada como chave de dicionário/set):
```python
estado = (1, 2, 3, 4, 0, 6, 7, 5, 8)
#         posições 0 a 8; 0 = espaço vazio
```

#### 2. Geração de Vizinhos
Para cada estado, a IA encontra os movimentos possíveis trocando o espaço vazio com peças adjacentes:
```python
def neighbors(state):
    zero = state.index(0)
    r, c = zero // 3, zero % 3
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    # para cada direção válida, gera o novo estado
```

#### 3. A Fila de Prioridade (Heap)
O A* usa uma **heap mínima** para sempre expandir o nó com menor `f(n)` primeiro:
```python
heap = [(f, g, state, path)]
heapq.heappush(heap, (f_novo, g_novo, novo_estado, caminho))
estado_atual = heapq.heappop(heap)
```

#### 4. Conjunto de Visitados
Para evitar revisitar estados já explorados (o espaço de estados tem 9!/2 = 181.440 estados possíveis):
```python
visited = set()
visited.add(state)  # tuplas são hashable!
```

---

### A Interface Visual

A IA construiu uma interface web completa com:

| Feature | Detalhes |
|---|---|
| **Editor interativo** | Campos para definir qualquer estado inicial |
| **Randomização** | Gera puzzle aleatório sempre solucionável |
| **Playback** | Navegar passo a passo com slider e play/pause |
| **Velocidade ajustável** | 50ms a 1000ms por passo |
| **Log de movimentos** | Lista clicável com todas as peças e direções |
| **Métricas em tempo real** | Movimentos, nós visitados, tempo de execução |
| **Validação** | Detecta estados inválidos e insolucionáveis |

---

### Exemplo de Execução

**Entrada:**
```
4 5 8
6 3 2
7 _ 1
```

**Saída do algoritmo:**
-  Solução em **25 movimentos**
-  Tempo: **~15ms**
-  Nós visitados: depende da complexidade

---

### Lições Aprendidas com a IA

1. **A heurística é tudo** — uma heurística mais precisa reduz drasticamente os nós explorados. Manhattan é muito melhor que "peças fora do lugar".

2. **Imutabilidade importa** — usar tuplas (imutáveis) em vez de listas permite usá-las como chaves em sets, essencial para rastrear visitados eficientemente.

3. **Solucionabilidade antes de buscar** — verificar inversões evita loops infinitos em estados sem solução.

4. **A* ≠ BFS** — no BFS, exploraríamos todos os estados de distância `k` antes dos de distância `k+1`. O A* "pula" para estados promissores usando a heurística, economizando memória e tempo.

---

### Arquivos Entregues

| Arquivo | Descrição |
|---|---|
| `8puzzle_app.html` | Interface visual completa, abre em qualquer navegador |
| `8puzzle_solver.py` | Algoritmo puro em Python, executa no terminal |

**Para rodar o Python:**
```bash
python 8puzzle_solver.py          # estado de exemplo
python 8puzzle_solver.py --random # estado aleatório
```

**Para a interface:** abra `8puzzle_app.html` em qualquer navegador moderno — sem dependências, sem instalação.
