"""
Maze Editor + BFS Solver (Tkinter)

Funcionalidades:
- Modo Edição com ferramentas: Parede (#), Caminho ( ), Início (S), Fim (E)
- Clique e arraste para desenhar
- Modo Simulação: busca BFS animada com .after()
- Reconstrução do caminho encontrado
- Resetar busca (limpa somente resultados da busca)
- Limpar labirinto (volta ao estado vazio)
"""

import tkinter as tk
from tkinter import messagebox
from collections import deque

class MazeEditorGUI:
    def __init__(self,
                 cols=30, rows=20,
                 cell_size=25,
                 tempo_ms=30):
        # Configurações do grid
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.tempo_ms = tempo_ms  # intervalo entre passos em ms

        # Cores sugeridas
        self.COLOR_WALL = "#1E3A5F"      # Parede (#)
        self.COLOR_PATH = "#FFFFFF"      # Caminho ( )
        self.COLOR_START = "#4CAF50"     # Início (S)
        self.COLOR_END = "#F44336"       # Fim (E)
        self.COLOR_FRONTIER = "#AED6F1"  # Fronteira (na fila)
        self.COLOR_VISITED = "#D6EAF8"   # Visitado
        self.COLOR_FINAL = "#FFD700"     # Caminho final (dourado)

        # Estado do labirinto: ' ' caminho, '#' parede, 'S' start, 'E' end
        self.labirinto = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        # IDs dos retângulos no canvas para cada célula
        self.grid_cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Posições de start e end (tuplas) ou None
        self.inicio_pos = None
        self.fim_pos = None

        # Para BFS
        self.fila = None
        self.visitados = set()
        self.predecessores = {}
        self.in_queue = set()

        # agendamento
        self.job_after = None

        # GUI init
        self.root = tk.Tk()
        self.root.title("Maze Editor & BFS Solver")

        self._build_ui()
        self._draw_grid_initial()

    # -------------------
    # UI BUILD
    # -------------------
    def _build_ui(self):
        # Frames
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=6, pady=4)

        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=6, pady=6)

        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, padx=6, pady=6, fill=tk.Y)

        # Canvas
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas = tk.Canvas(left_frame, width=canvas_width, height=canvas_height, bg="lightgray")
        self.canvas.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

        # Tools (Radiobuttons)
        tk.Label(right_frame, text="Modo Edição (Ferramenta):").pack(anchor="w")
        self.tool_var = tk.StringVar(value="wall")
        tools = [
            ("Parede (#)", "wall"),
            ("Caminho ( )", "path"),
            ("Início (S)", "start"),
            ("Fim (E)", "end")
        ]
        for txt, val in tools:
            rb = tk.Radiobutton(right_frame, text=txt, variable=self.tool_var, value=val)
            rb.pack(anchor="w")

        # Buttons
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=8, fill=tk.X)

        self.btn_start = tk.Button(btn_frame, text="Iniciar Busca (BFS)", command=self.iniciar_busca)
        self.btn_start.pack(fill=tk.X, pady=2)

        self.btn_reset = tk.Button(btn_frame, text="Resetar Busca", command=self.resetar_busca)
        self.btn_reset.pack(fill=tk.X, pady=2)

        self.btn_clear = tk.Button(btn_frame, text="Limpar Labirinto", command=self.limpar_labirinto)
        self.btn_clear.pack(fill=tk.X, pady=2)

        # Status label
        self.status_var = tk.StringVar(value="Modo Edição: desenhe paredes, início e fim.")
        self.status_label = tk.Label(top_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(fill=tk.X)

        # Small legend
        legend = tk.Label(right_frame, text="\nLegenda:\nS = Início (verde)\nE = Fim (vermelho)\n# = Parede (azul escuro)")
        legend.pack(anchor="w", pady=6)

    # -------------------
    # GRID DRAW
    # -------------------
    def _draw_grid_initial(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.COLOR_PATH, outline="#cccccc")
                self.grid_cells[r][c] = rect_id

    # -------------------
    # MOUSE HELPERS
    # -------------------
    def _coords_to_cell(self, event_x, event_y):
        c = int(event_x // self.cell_size)
        r = int(event_y // self.cell_size)
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return (r, c)
        return None

    def on_canvas_click(self, event):
        cell = self._coords_to_cell(event.x, event.y)
        if cell:
            self.editar_celula(cell[0], cell[1])

    def on_canvas_drag(self, event):
        cell = self._coords_to_cell(event.x, event.y)
        if cell:
            self.editar_celula(cell[0], cell[1])

    # -------------------
    # EDIT CELL (MODE EDIT)
    # -------------------
    def editar_celula(self, r, c):
        tool = self.tool_var.get()
        current = self.labirinto[r][c]

        # If editing disabled because simulation running, ignore
        if not self._edicao_permitida():
            return

        if tool == "wall":
            # set wall
            if current != '#':
                # if it was start or end, update positions
                if current == 'S':
                    self.inicio_pos = None
                if current == 'E':
                    self.fim_pos = None
                self.labirinto[r][c] = '#'
                self._pintar_celula(r, c, self.COLOR_WALL)
        elif tool == "path":
            # set path (erase)
            if current != ' ':
                if current == 'S':
                    self.inicio_pos = None
                if current == 'E':
                    self.fim_pos = None
                self.labirinto[r][c] = ' '
                self._pintar_celula(r, c, self.COLOR_PATH)
        elif tool == "start":
            # place start; only one allowed
            if current == 'S':
                return
            # remove old start
            if self.inicio_pos:
                old_r, old_c = self.inicio_pos
                self.labirinto[old_r][old_c] = ' '
                self._pintar_celula(old_r, old_c, self.COLOR_PATH)
            # if new pos was end, clear end
            if self.labirinto[r][c] == 'E':
                self.fim_pos = None
            self.labirinto[r][c] = 'S'
            self.inicio_pos = (r, c)
            self._pintar_celula(r, c, self.COLOR_START)
        elif tool == "end":
            # place end; only one allowed
            if current == 'E':
                return
            # remove old end
            if self.fim_pos:
                old_r, old_c = self.fim_pos
                self.labirinto[old_r][old_c] = ' '
                self._pintar_celula(old_r, old_c, self.COLOR_PATH)
            # if new pos was start, clear start
            if self.labirinto[r][c] == 'S':
                self.inicio_pos = None
            self.labirinto[r][c] = 'E'
            self.fim_pos = (r, c)
            self._pintar_celula(r, c, self.COLOR_END)

    def _pintar_celula(self, r, c, color):
        rect_id = self.grid_cells[r][c]
        self.canvas.itemconfigure(rect_id, fill=color)

    # -------------------
    # CONTROLES DE EDIÇÃO / SIMULAÇÃO
    # -------------------
    def _edicao_permitida(self):
        # Edição permitida quando não há job em execução
        return self.job_after is None

    def _set_edicao_enabled(self, enabled: bool):
        # If disabled, gray out the radiobuttons and prevent editing via flag
        state = tk.NORMAL if enabled else tk.DISABLED
        # iterate widgets on the right frame (radiobuttons are children)
        for widget in self.root.winfo_children():
            pass
        # Simpler: enable/disable the buttons related to editing
        for child in self.root.winfo_children():
            # We won't be exhaustive — just disable the Start/Reset/Clear appropriately
            pass
        # Instead of fiddly toggles, we enable/disable the main control buttons to avoid editing during sim
        if enabled:
            self.btn_clear.config(state=tk.NORMAL)
            self.btn_reset.config(state=tk.NORMAL)
            self.btn_start.config(state=tk.NORMAL)
        else:
            # When simulation running, don't allow start/clear
            self.btn_clear.config(state=tk.DISABLED)
            self.btn_reset.config(state=tk.DISABLED)
            self.btn_start.config(state=tk.DISABLED)

    # -------------------
    # BFS LOGIC (SIMULATION)
    # -------------------
    def iniciar_busca(self):
        # Validate S and E
        if self.inicio_pos is None or self.fim_pos is None:
            messagebox.showwarning("Atenção", "Defina posição de Início (S) e Fim (E) antes de iniciar a busca.")
            return
        # Reset previous search (colors) but keep labirinto
        self.resetar_busca()

        # initialize BFS structures
        self.fila = deque()
        self.visitados = set()
        self.predecessores = {}
        self.in_queue = set()

        start = self.inicio_pos
        self.fila.append(start)
        self.in_queue.add(start)
        # mark start as frontier (or keep green)
        self._pintar_celula(start[0], start[1], self.COLOR_START)

        # disable editing controls while sim
        self._set_edicao_enabled(False)
        self.status_var.set("Busca em andamento...")

        # schedule first BFS step
        self.job_after = self.root.after(self.tempo_ms, self.processar_passo_bfs)

    def processar_passo_bfs(self):
        if not self.fila:
            # fila vazia e nada achado
            self.status_var.set("Busca finalizada: Caminho não encontrado.")
            self.job_after = None
            # re-enable editing controls
            self._set_edicao_enabled(True)
            return

        atual = self.fila.popleft()
        # remove from in_queue (já foi processado)
        if atual in self.in_queue:
            self.in_queue.remove(atual)

        # if atual is end -> reconstruct path
        if atual == self.fim_pos:
            self.status_var.set("Destino encontrado! Reconstruindo caminho...")
            self._reconstruir_caminho(atual)
            self.job_after = None
            # re-enable editing
            self._set_edicao_enabled(True)
            return

        # mark current visited (unless it's start which remains green)
        if atual != self.inicio_pos:
            ar, ac = atual
            self._pintar_celula(ar, ac, self.COLOR_VISITED)
        self.visitados.add(atual)

        # Explore neighbors: up, down, left, right
        r, c = atual
        vizinhos = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for vr, vc in vizinhos:
            if 0 <= vr < self.rows and 0 <= vc < self.cols:
                if (vr, vc) in self.visitados:
                    continue
                if (vr, vc) in self.in_queue:
                    continue
                cell_value = self.labirinto[vr][vc]
                # can step if not wall '#'
                if cell_value != '#':
                    # record predecessor
                    self.predecessores[(vr, vc)] = atual
                    # add to queue
                    self.fila.append((vr, vc))
                    self.in_queue.add((vr, vc))
                    # color frontier (but keep start/end special)
                    if (vr, vc) == self.fim_pos:
                        # show as end (red)
                        self._pintar_celula(vr, vc, self.COLOR_END)
                    elif (vr, vc) == self.inicio_pos:
                        self._pintar_celula(vr, vc, self.COLOR_START)
                    else:
                        self._pintar_celula(vr, vc, self.COLOR_FRONTIER)

        # schedule next step
        self.job_after = self.root.after(self.tempo_ms, self.processar_passo_bfs)

    def _reconstruir_caminho(self, destino):
        # Reconstrói o caminho de destino até start usando self.predecessores
        caminho = []
        atual = destino
        while atual != self.inicio_pos:
            caminho.append(atual)
            if atual in self.predecessores:
                atual = self.predecessores[atual]
            else:
                # Não há predecessor -> não foi possível reconstruir
                break
        # pintar caminho (exclui S e E cores especiais)
        for pos in caminho:
            if pos == self.fim_pos or pos == self.inicio_pos:
                continue
            r, c = pos
            self._pintar_celula(r, c, self.COLOR_FINAL)
        self.status_var.set("Caminho reconstruído com sucesso.")

    # -------------------
    # RESET / CLEAR
    # -------------------
    def resetar_busca(self):
        # Cancel after job if running
        if self.job_after:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None

        # Clear BFS-specific states/paintings but keep '#', 'S', 'E'
        for r in range(self.rows):
            for c in range(self.cols):
                v = self.labirinto[r][c]
                if v == '#':
                    self._pintar_celula(r, c, self.COLOR_WALL)
                elif v == 'S':
                    self._pintar_celula(r, c, self.COLOR_START)
                elif v == 'E':
                    self._pintar_celula(r, c, self.COLOR_END)
                else:
                    # default path
                    self._pintar_celula(r, c, self.COLOR_PATH)

        # reset BFS structures
        self.fila = None
        self.visitados = set()
        self.predecessores = {}
        self.in_queue = set()
        self.status_var.set("Busca resetada. Modo Edição.")
        # re-enable editing
        self._set_edicao_enabled(True)

    def limpar_labirinto(self):
        # Cancel any running job
        if self.job_after:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None

        # Reset model and canvas to empty
        self.labirinto = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.inicio_pos = None
        self.fim_pos = None
        for r in range(self.rows):
            for c in range(self.cols):
                self._pintar_celula(r, c, self.COLOR_PATH)
        self.fila = None
        self.visitados = set()
        self.predecessores = {}
        self.in_queue = set()
        self.status_var.set("Labirinto limpo. Modo Edição.")
        self._set_edicao_enabled(True)

    # -------------------
    # RUN GUI
    # -------------------
    def run(self):
        self.root.mainloop()


# -------------------
# Rodar app
# -------------------
if __name__ == "__main__":
    app = MazeEditorGUI(cols=30, rows=20, cell_size=28, tempo_ms=25)
    app.run()
