import pygame
import sys
import time
import csv
import os
import random

from interfaz import WHITE, BLACK, GRAY, DARKGRAY, BLUE, GREEN, RED, FONT, BIGFONT, Button
from ranking import leer_ranking, guardar_en_ranking

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60


#SONIDOS DEL JUEGO

pygame.mixer.init()

sonido_click = pygame.mixer.Sound("sonidos/click.wav")
sonido_error = pygame.mixer.Sound("sonidos/error.wav")
sonido_victoria = pygame.mixer.Sound("sonidos/victoria.wav")
sonido_gameover = pygame.mixer.Sound("sonidos/gameover.wav")



#CARGAR NONOGRAMAS CSV


def cargar_nonogramas(archivo):

    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, archivo)

    if not os.path.exists(path):
        default = """Corazon;5;5;0 1 1 1 0|1 1 1 1 1|1 1 1 1 1|0 1 1 1 0|0 0 1 0 0
CaraFeliz;5;5;0 1 0 1 0|0 1 0 1 0|0 0 0 0 0|1 0 0 0 1|0 1 1 1 0
Cruz;5;5;0 0 1 0 0|0 0 1 0 0|1 1 1 1 1|0 0 1 0 0|0 0 1 0 0
Diamante;5;5;0 0 1 0 0|0 1 1 1 0|1 1 1 1 1|0 1 1 1 0|0 0 1 0 0
Flecha;5;5;0 0 1 0 0|0 1 1 1 0|1 1 1 1 1|0 0 1 0 0|0 0 1 0 0
"""
        archivo_default = open(path, "w", encoding="utf-8", newline="")
        archivo_default.write(default)
        archivo_default.close()

    lista = []

    archivo_lectura = open(path, "r", encoding="utf-8")
    lector = csv.reader(archivo_lectura, delimiter=";")

    for linea in lector:
        if len(linea) < 4:
            continue

        nombre = linea[0].strip()
        filas = int(linea[1])
        columnas = int(linea[2])
        texto = linea[3].strip().split("|")

        matriz = []
        for fila in texto:
            if fila.strip() == "":
                continue
            nums = fila.strip().split(" ")
            fila_convertida = []
            for n in nums:
                if n != "":
                    fila_convertida.append(int(n))
            matriz.append(fila_convertida)

        if len(matriz) == filas and all(len(r) == columnas for r in matriz):
            lista.append([nombre, filas, columnas, matriz])

    archivo_lectura.close()
    return lista




#CALCULAR PISTAS


def calcular_pistas(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    pistas_filas = []
    pistas_columnas = []

    # Pistas filas
    for fila in matriz:
        pista = []
        cont = 0
        for celda in fila:
            if celda == 1:
                cont += 1
            else:
                if cont > 0:
                    pista.append(cont)
                    cont = 0
        if cont > 0:
            pista.append(cont)
        if pista == []:
            pista = [0]
        pistas_filas.append(pista)

    # Pistas columnas
    for c in range(columnas):
        pista = []
        cont = 0
        for f in range(filas):
            if matriz[f][c] == 1:
                cont += 1
            else:
                if cont > 0:
                    pista.append(cont)
                    cont = 0
        if cont > 0:
            pista.append(cont)
        if pista == []:
            pista = [0]
        pistas_columnas.append(pista)

    return pistas_filas, pistas_columnas




#MENÚ PRINCIPAL


def pantalla_menu():
    btn_play = Button((WIDTH//2 - 150, 220, 300, 60), "Iniciar juego")
    btn_rank = Button((WIDTH//2 - 150, 320, 300, 60), "Ranking", GREEN)
    btn_exit = Button((WIDTH//2 - 150, 420, 300, 60), "Salir", RED)

    while True:
        SCREEN.fill(DARKGRAY)

        title = BIGFONT.render("NONOGRAMA", True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:

                if btn_play.is_clicked(ev.pos):
                    sonido_click.play()
                    nombre = pantalla_registro()

                    lista = cargar_nonogramas("nonogramas.csv")

                    nombre_nono, filas, columnas, matriz = random.choice(lista)

                    tiempo, dibujo = pantalla_nonograma(matriz, nombre_nono)

                    if tiempo is not None:
                        guardar_en_ranking(nombre, tiempo, dibujo)

                if btn_rank.is_clicked(ev.pos):
                    sonido_click.play()
                    pantalla_ranking()

                if btn_exit.is_clicked(ev.pos):
                    sonido_click.play()
                    pygame.quit()
                    sys.exit()

        btn_play.draw(SCREEN)
        btn_rank.draw(SCREEN)
        btn_exit.draw(SCREEN)

        pygame.display.flip()
        CLOCK.tick(FPS)




#FUNCIONES MATRIZ Y TABLERO


def crear_matriz(filas, columnas, valor):
    return [[valor for c in range(columnas)] for f in range(filas)]


def calcular_posicion_celda(mx, my, offset_x, offset_y, cell):
    col = (mx - offset_x) // cell
    row = (my - offset_y) // cell
    return row, col


def dentro_del_tablero(row, col, grid):
    return 0 <= row < grid and 0 <= col < grid


def comparar_con_solucion(estado, sol):
    for r in range(len(sol)):
        for c in range(len(sol[0])):
            if estado[r][c] != sol[r][c]:
                return False
    return True



def dibujar_nonograma(estado, ox, oy, cell, screen):
    for r in range(len(estado)):
        for c in range(len(estado[0])):
            x = ox + c * cell
            y = oy + r * cell

            pygame.draw.rect(screen, WHITE, (x, y, cell, cell), 2)

            if estado[r][c] == 1:
                pygame.draw.rect(screen, BLACK, (x+3, y+3, cell-6, cell-6))
            elif estado[r][c] == 0:
                pygame.draw.line(screen, RED, (x+5, y+5), (x+cell-5, y+cell-5), 3)
                pygame.draw.line(screen, RED, (x+cell-5, y+5), (x+5, y+cell-5), 3)




#PANTALLA REGISTRO


def pantalla_registro():
    input_box = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 20, 400, 50)
    nombre = ""

    while True:
        SCREEN.fill(DARKGRAY)
        title = BIGFONT.render("Ingresá tu nombre", True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and nombre.strip():
                    sonido_click.play()
                    return nombre.strip()
                elif ev.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += ev.unicode

        pygame.draw.rect(SCREEN, WHITE, input_box, border_radius=5)
        texto = FONT.render(nombre, True, BLACK)
        SCREEN.blit(texto, (input_box.x + 10, input_box.y + 12))

        pygame.display.flip()
        CLOCK.tick(FPS)




#PANTALLA RANKING


def pantalla_ranking():
    ranking = leer_ranking()

    while True:
        SCREEN.fill((15, 15, 25))

        title = BIGFONT.render("Ranking Top 10", True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 30))

        if not ranking:
            txt = FONT.render("No hay jugadores todavía.", True, WHITE)
            SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))
        else:
            for i, r in enumerate(ranking, 1):
                linea = FONT.render(f"{i}. {r['nombre']} - {r['tiempo']}s - {r['dibujo']}", True, WHITE)
                SCREEN.blit(linea, (80, 120 + 30*(i-1)))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                sonido_click.play()
                return

        pygame.display.flip()
        CLOCK.tick(FPS)




#PANTALLA DEL NONOGRAMA


def pantalla_nonograma(SOLUCION, nombre_nono):

    GRID = len(SOLUCION)
    CELL = 60
    OFFSET_X = 150
    OFFSET_Y = 120

    estado = crear_matriz(GRID, GRID, -1)
    vidas = 3
    penalizado_hasta = 0
    tiempo_inicio = time.time()

    pistas_filas, pistas_columnas = calcular_pistas(SOLUCION)

    while True:
        SCREEN.fill((30,30,40))

        texto_vidas = FONT.render("Vidas: " + str(vidas), True, WHITE)
        SCREEN.blit(texto_vidas, (20, 20))

        if time.time() < penalizado_hasta:
            t = int(penalizado_hasta - time.time())
            texto_penal = FONT.render("Penalizado " + str(t) + "s", True, RED)
            SCREEN.blit(texto_penal, (20, 60))

        # EVENTOS 
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN and time.time() >= penalizado_hasta:
                sonido_click.play()

                mx, my = ev.pos
                row, col = calcular_posicion_celda(mx, my, OFFSET_X, OFFSET_Y, CELL)

                if dentro_del_tablero(row, col, GRID):

                    if ev.button == 1:  # pintar
                        estado[row][col] = 1
                        if SOLUCION[row][col] != 1:
                            vidas -= 1
                            sonido_error.play()
                            penalizado_hasta = time.time() + 3

                    elif ev.button == 3:  # cruz
                        estado[row][col] = 0
                        if SOLUCION[row][col] != 0:
                            vidas -= 1
                            sonido_error.play()
                            penalizado_hasta = time.time() + 3

        # 
        # DIBUJAR TABLERO
        dibujar_nonograma(estado, OFFSET_X, OFFSET_Y, CELL, SCREEN)

        # PISTAS FILAS
        for i, pista in enumerate(pistas_filas):
            texto = " ".join(str(n) for n in pista)
            t = FONT.render(texto, True, WHITE)
            SCREEN.blit(t, (OFFSET_X - 40, OFFSET_Y + i*CELL + 20))

        # PISTAS COLUMNAS
        for j, pista in enumerate(pistas_columnas):
            y = OFFSET_Y - 20
            for n in pista:
                t = FONT.render(str(n), True, WHITE)
                SCREEN.blit(t, (OFFSET_X + j*CELL + 20, y))
                y -= 18

        # GAME OVER 
        if vidas <= 0:
            sonido_gameover.play()
            msg = BIGFONT.render("GAME OVER", True, RED)
            SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 80))
            pygame.display.flip()
            time.sleep(2)
            return None, None

        # VICTORIA
        if comparar_con_solucion(estado, SOLUCION):
            sonido_victoria.play()
            msg = BIGFONT.render("¡COMPLETADO!", True, GREEN)
            SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 80))
            pygame.display.flip()
            time.sleep(2)

            tiempo_total = int(time.time() - tiempo_inicio)
            return tiempo_total, nombre_nono

        pygame.display.flip()
        CLOCK.tick(60)
