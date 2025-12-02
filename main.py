import pygame
from ranking import crear_archivo_si_no_existe
from screen import pantalla_menu

def main():
    pygame.init()
    crear_archivo_si_no_existe()
    pantalla_menu()

if __name__ == "__main__":
    main()
