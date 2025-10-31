import random
from colorama import init, Fore

# ============================
# CONFIGURACIÓN DEL TABLERO
# ============================
N = 5  # tamaño del tablero
gato = (0, 0)
raton = (4, 4)
movs = [(-1,0),(1,0),(0,-1),(0,1)]  # movimientos posibles (4 direcciones)

def vecinos(pos):
    x, y = pos
    return [(x+dx, y+dy) for dx, dy in movs if 0 <= x+dx < N and 0 <= y+dy < N]

# ============================
# FUNCIÓN DE EVALUACIÓN
# ============================
def evaluar(gato, raton):
    # Distancia Manhattan: entre más grande, mejor para el ratón
    return abs(gato[0]-raton[0]) + abs(gato[1]-raton[1])

# ============================
# ALGORITMO MINIMAX
# ============================
def minimax(gato, raton, depth, turno):
    if gato == raton:  # gato atrapó al ratón
        return -999 if turno=="raton" else 999
    if depth == 0:  # límite de profundidad
        return evaluar(gato, raton)

    if turno == "raton":
        mejor = -9999
        for mov in vecinos(raton):
            mejor = max(mejor, minimax(gato, mov, depth-1, "gato"))
        return mejor
    else:  # turno del gato
        peor = 9999
        for mov in vecinos(gato):
            peor = min(peor, minimax(mov, raton, depth-1, "raton"))
        return peor

# ============================
# MOVIMIENTOS
# ============================
def mover_raton_aleatorio(raton):
    # ratón se mueve random
    return random.choice(vecinos(raton))

def mover_raton(gato, raton):
    # ratón usa minimax
    mejor_valor, mejor_mov = -9999, raton
    for mov in vecinos(raton):
        val = minimax(gato, mov, 3, "gato")
        if val > mejor_valor:
            mejor_valor, mejor_mov = val, mov
    return mejor_mov

def mover_gato(gato, raton):
    # gato usa minimax
    peor_valor, peor_mov = 9999, gato
    for mov in vecinos(gato):
        val = minimax(mov, raton, 3, "raton")
        if val < peor_valor:
            peor_valor, peor_mov = val, mov
    return peor_mov

# ============================
# TABLERO VISUAL
# ============================
def mostrar_tablero(gato, raton):
    for i in range(N):
        fila = ""
        for j in range(N):
            if (i,j) == gato:
                fila += "🐱 "
            elif (i,j) == raton:
                fila += "🐭 "
            else:
                fila += "🟫 "
        print(fila)
    print("\n")

# ============================
# SIMULACIÓN DEL JUEGO
# ============================
turnos = 10

print(f"\n{Fore.CYAN}¡Bienvenido al Juego del Gato & el Ratón!...")

for t in range(turnos):
    print(f"Turno {t}:")
    mostrar_tablero(gato, raton)

    if gato == raton:
        print("¡El gato atrapó al ratón! 😼")
        break

    # los primeros 3 turnos el ratón se mueve random
    if t < 3:
        raton = mover_raton_aleatorio(raton)
        print("🐭 El ratón se mueve al azar...")
    else:
        raton = mover_raton(gato, raton)
        print("🐭 El ratón planea su escape con astucia...")

    if gato == raton:
        mostrar_tablero(gato, raton)
        print("¡El gato atrapó al ratón! 😼")
        break

    gato = mover_gato(gato, raton)
    print("🐱 El gato calcula su jugada...")

else:
    mostrar_tablero(gato, raton)
    print("¡El ratón sobrevivió! 🐭🧀")