import math, random


def main():
    dim = int(input("Width: "))
    if dim == 1:
        return None
    completed_tiles = [n for n in range(dim * dim)]    
    tiles = shuffle_tiles(completed_tiles)
    print(State(tiles, ""))
    dist = get_manhattan_distance(tiles)
    while dist > 0:
        try_move = input("Move [H|J|K|L] | [S]olve | [Q]uit: ")
        if try_move == "S":
            print("Solution:", solve_puzzle(tiles).path)
        elif try_move == "Q":
            return None
        elif is_valid_move(tiles, try_move):
            tiles = move_tile(tiles, try_move)
            print(State(tiles, ""))
        else:
            print("Invalid Move")
        dist = get_manhattan_distance(tiles)
    print("Puzzle Complete!")


class State:
    
    def __init__(self, tiles, path):
        self.tiles = tiles
        self.path = path
        self.distance = get_manhattan_distance(self.tiles)
        self.cost = len(self.path) + self.distance
    
    def __eq__(self, other):
        return self.tiles == other.tiles and len(self.path) == len(other.path)
    
    def __repr__(self):
        dim = len(self.tiles) ** (1 / 2)
        if dim == 0:
            return "\n"
        stringy = "\n"
        for n in range(len(self.tiles)):
            if self.tiles[n] == 0:
                stringy += "    "
            else:
                stringy += "[{:2d}]".format(self.tiles[n]) 
            if (n + 1) % dim == 0 and n != len(self.tiles) - 1:
               stringy += "\n"
        return stringy + "\n" 


def is_opposing_move(prev_move, next_move):
    opposing = [["J", "K"], ["H", "L"]]
    if prev_move != next_move:
        for n in range(len(opposing)):
            if prev_move in opposing[n] and next_move in opposing[n]:
                return True
    return False


def create_new_states(state):
    frontier = []
    pre_move = state.path[-1] if len(state.path) > 0 else ""
    if len(state.tiles) == 0:
        return [State([], "")]
    elif len(state.tiles) == 1:
        return [state]
    else:
        for move in ["J", "K", "H", "L"]:
            if not is_opposing_move(pre_move, move):
                if is_valid_move(state.tiles, move):
                    tilesy = move_tile(state.tiles, move)
                    frontier.append(State(tilesy, str(state.path + move)))
        return frontier


def solve_puzzle(tiles):
    open_list = []
    closed_list = []
    current_state = State(tiles, "")
    while current_state.distance > 0:
        new_states = (create_new_states(current_state))
        for state in new_states:
            if state not in closed_list:
                open_list.append(state)
        costs = [state.cost for state in open_list]
        min_cost = min(costs)
        for open in open_list:
            if open.cost == min_cost:
                min_state = open
        closed_list.append(min_state)
        open_list.remove(min_state)
        current_state = closed_list[-1]
        #for state in open_list:
            #if state.cost == min_cost:
            #    closed_list.append(state)
            #    open_list.remove(state)
            #    current_state = state
    return current_state
    
 
def find_position(tiles, val):
    pos = 0
    dim = int(math.sqrt(len(tiles)))
    while tiles[pos] != val:
        pos += 1
    return pos 


def set_special_case(tiles):
    dim = int(math.sqrt(len(tiles)))
    open_pos = find_position(tiles, 0)
    open_row = get_row(tiles, open_pos)
    open_col = get_col(tiles, open_pos)
    special_case = []
    if open_row == 0:
        special_case.append("TOP CASE") 
    elif open_row == dim - 1:
        special_case.append("BOTTOM CASE")
    if open_col == 0:
        special_case.append("LEFT CASE")
    elif open_col == dim - 1:
        special_case.append("RIGHT CASE")
    return special_case


def is_valid_move(tiles, move):
    special_case = set_special_case(tiles)
    all_valid_moves = ["H", "J", "K", "L"]
    if "LEFT CASE" in special_case:
        all_valid_moves.remove("L")
    elif "RIGHT CASE" in special_case:
        all_valid_moves.remove("H")
    if "TOP CASE" in special_case:
        all_valid_moves.remove("J")
    elif "BOTTOM CASE" in special_case:
        all_valid_moves.remove("K")
    return move in all_valid_moves


def copy_tiles(tiles):
    return [tiles[pos] for pos in range(len(tiles))]


def find_tile_position(tiles, move):
    dim = int(math.sqrt(len(tiles)))
    open_pos = find_position(tiles, 0)
    open_row = get_row(tiles, open_pos)
    open_col = get_col(tiles, open_pos)
    if move in "HL":
        tile_row = open_row
        if move == "H":
            tile_col = open_col + 1
        else:
            tile_col = open_col - 1
    if move in "KJ":
        tile_col = open_col
        if move == "K":
            tile_row = open_row + 1
        else:
            tile_row = open_row - 1
    return (dim * tile_row) + tile_col


def move_tile(tiles, move):   
    open_pos = find_position(tiles, 0) 
    copy = copy_tiles(tiles)
    tile_pos = find_tile_position(tiles, move)
    copy[tile_pos] = 0
    copy[open_pos] = tiles[tile_pos] 
    return copy 


def get_row(tiles, pos):
    dim = int(math.sqrt(len(tiles)))
    row = pos // dim
    return row


def get_col(tiles, pos):
    dim = int(math.sqrt(len(tiles)))
    col = pos % dim
    return col


def get_manhattan_distance(tiles):
    completed = [n for n in range(len(tiles))]       
    dist = 0
    for n in range(1, len(tiles)):
        n_curr_pos = find_position(tiles, n)            
        n_curr_row = get_row(tiles, n_curr_pos)
        n_curr_col = get_col(tiles, n_curr_pos)
        n_fin_row = get_row(completed, n)
        n_fin_col = get_col(completed, n)
        row_diff = abs(n_curr_row - n_fin_row) 
        col_diff = abs(n_curr_col - n_fin_col)
        dist = dist + row_diff + col_diff
    return dist


def shuffle_tiles(tiles):
    while get_manhattan_distance(tiles) < len(tiles):   
        rand_move = random.choice("HJKL")
        if is_valid_move(tiles, rand_move):
            tiles = move_tile(tiles, rand_move)
    return tiles


if __name__ == "__main__":
    main()

