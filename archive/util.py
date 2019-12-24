""" util.py contains various utility routines for Trans America """
import pygame
import board as b

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

def eval_move(player, move, board, distances_left):
    """
    Computes a move's effect on all total distances without actually making the move. Note that this does modify distances_left.
    This logic is the same as the update logic for make_move,  but doesn't actually modify the board.
    The actual algorithm is similar to Floyd-Warshall,  but on just the cities and hubs.
    """
    #This for loop simply finds the node that the player isn't already connected to in the move.
    for track in move:
        if track not in board.player_nodes_in_reach[player][0]:
            #Use cost matrix to update player to player costs if this track is closer than any previous track.
            for i in range(0, len(board.hubs)):
                if i == player:
                    continue
                hub = board.hubs[i]
                if distances_left[player][hub] > 0:
                    for compare_track in board.player_nodes_in_reach[i][0]:
                        if b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]] < distances_left[player][hub]:
                            distances_left[player][hub] = b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
                        if b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]] < distances_left[i][board.hubs[player]]:
                            distances_left[i][board.hubs[player]] = b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
            #Update any cities that this track brings me closer to
            for city in board.cities.values():
                for location in city.values():
                    if b.costs[track[0]][track[1]][location[0]][location[1]] < distances_left[player][location]:
                        distances_left[player][location] = b.costs[track[0]][track[1]][location[0]][location[1]]
            #Update any cities/hubs that are faster to reacher via another player
            for i in range(0, len(board.hubs)):
                for j in range(0, len(board.hubs)):
                    if distances_left[j][board.hubs[player]]+distances_left[player][board.hubs[i]] < distances_left[j][board.hubs[i]]:
                        distances_left[j][board.hubs[i]] = distances_left[j][board.hubs[player]]+distances_left[player][board.hubs[i]]
                    if distances_left[i][board.hubs[player]]+distances_left[player][board.hubs[j]] < distances_left[i][board.hubs[j]]:
                        distances_left[i][board.hubs[i]] = distances_left[i][board.hubs[player]]+distances_left[player][board.hubs[j]]
                for city in board.cities.values():
                    for location in city.values():
                        if distances_left[player][location] > distances_left[i][location]+distances_left[player][board.hubs[i]]:
                            distances_left[player][location] = distances_left[i][location]+distances_left[player][board.hubs[i]]
                        if distances_left[i][location] > distances_left[player][location]+distances_left[i][board.hubs[player]]:
                            distances_left[i][location] = distances_left[player][location]+distances_left[i][board.hubs[player]]
    return distances_left
