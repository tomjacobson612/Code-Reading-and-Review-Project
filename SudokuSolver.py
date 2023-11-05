import pygame, Game, Window

WINDOW = Window.Window(1200, 1100, (251, 247, 245), 'Sudoku Solver')

def main():
    app = Game.Game(gridColor=(0, 0, 0), solutionColor=(136, 8, 8), backgroundColor=(255, 255, 255), gridOuterWidth=4, gridInnerWidth=1)
    app.drawBoard()

    while True:
        if app.buttons[0].buttonPress() and not app.boardSolved:
            app.solveBoard()
            app.populateSolution()
        if app.buttons[1].buttonPress():
            app = Game.Game(gridColor=(0, 0, 0), solutionColor=(136, 8, 8), backgroundColor=(255, 255, 255), gridOuterWidth=4, gridInnerWidth=1)
            app.drawBoard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()

if __name__ == "__main__" :
    main()