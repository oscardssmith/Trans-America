""" util.py contains various utility routines for Trans America """
import sys
import pygame

def wait_for_key():
    """ Wait either for 'w' (proceed) or 'q' (quit) """
    while True:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return True
                if event.key == pygame.K_q:
                    return False

def wait_for_click():
    """ Wait for a mouse click """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return event.pos
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit(0)
