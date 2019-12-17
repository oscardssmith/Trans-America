#!/usr/bin/python3
""" util.py contains various utility routines for Trans America """
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
