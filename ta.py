#!/usr/bin/python3
from game import game
import graphics
import mcts
import minTotalAI
import minDifferenceAI
import mapFeatures
import pygame

def run_tournament(num, ai1, ai2):
    wins=[0,0,0]
    while(sum(wins)<num):
        players = [[0,ai1],[1,ai2]]
        g = game(players,mapFeatures)

        gBoard = copy.deepcopy(g.board)
        hands2 = copy.deepcopy(g.hands)
        winner1 = g.play_game()

        g2 = game([[0,ai2],[1,ai1]],mapFeatures,gBoard,hands2)
        winner2 =g2.play_game()
        if winner1 != winner2:
            print(winner1)
            wins[winner1]+=1
        else:
            print("draw")
            wins[2]+=1
    print(wins)

def run_graphics(ai1, ai2):
    players=[[0,ai1],[1,ai2]]
    g=game(players,mapFeatures)
    
    w = graphics.window(graphics.xres,graphics.yres,mapFeatures)
    grid=g.board

    running = True
    done = False
    draw = True

    # main loop
    while running:
        if draw:
            w.draw(g.board, g.hands)
            w.draw_turn(int((g.board.total_turns / len(players)) + 1),
                g.board.turn + 1, g.board.tracks_left)
            draw = False

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not done:
                    done=g.take_turn()
                    draw = True
                    if done:
                        print(g.board.value(g.hands))
                if event.key == pygame.K_q:
                    running = False

if __name__ == '__main__':
    run_graphics(mcts, minDifferenceAI)
    #run_graphics(minTotalAI, minDifferenceAI)
    #run_tournament(100, mcts, minDifferenceAI)
