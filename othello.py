
class Marker:
    def __init__(self, color=None):
        self.colors_dict = {'Black': chr(9675), 'White': chr(9679)}
        if color and color in self.colors_dict.keys():
            self.color = color
        else:
            print("color code error")

    def get_color(self):
        return self.color

    def turn_over(self):
        if self.color == 'Black':
            self.color = 'White'
        if self.color == 'White':
            self.color = 'Black'


class Player:
    def __init__(self, name, color):
        self.name = name
        self.brick_counter = 30
        self.color = color


class PlayField:
    def __init__(self, rows=8, columns=8):
        self.colors_dict = {'Black': chr(9675), 'White': chr(9679)}
        self.rows = rows
        self.columns = columns
        self.rowletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.columnnumbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.playfield = []
        self.create()

    def create(self):
        for row in range(self.rows):
            self.playfield.append([None] * self.columns)
        self.playfield[3][3] = Marker("White")
        self.playfield[3][4] = Marker("Black")
        self.playfield[4][3] = Marker("Black")
        self.playfield[4][4] = Marker("White")

    def draw(self):
        column_line = "  "
        for column in range(self.columns):
            column_line = column_line+str(self.columnnumbers[column])+" "
        print(column_line)
        for row in range(self.rows):
            current_row = self.rowletters[row]+"|"
            for column in range(self.columns):
                if self.playfield[row][column]:
                    current_row = current_row + self.colors_dict[self.playfield[row][column].color]
                else:
                    current_row = current_row + " "
                if column != self.columns:
                    current_row = current_row + "|"
            print(current_row)

    def get_adjacent_opponent_tiles(self, player, coord_list):
        r, c = coord_list
        r1 = [[r-1, c-1], [r-1, c], [r-1, c+1]]
        r2 = [[r, c-1], [r, c+1]]
        r3 = [[r+1, c-1], [r+1, c], [r+1, c+1]]
        adjacent_tiles = r1+r2+r3
        # remove eval_tiles outside of playfield
        valid_adjacent_tiles = []
        for tile in adjacent_tiles:
            if -1 not in tile and 8 not in tile:  # If tile is outside of playfield, don't use it.
                valid_adjacent_tiles.append(tile)
        opponent_tiles = []
        for eval_tile in valid_adjacent_tiles:
            if self.playfield[eval_tile[0]][eval_tile[1]]:  # There is a marker on the tile
                if self.playfield[eval_tile[0]][eval_tile[1]].color != player.color:  # its an opponent marker.
                    opponent_tiles.append(eval_tile)
        return opponent_tiles

    def valid_placement(self, player, coord_list):
        valid_tile = False
        row, column = coord_list
        if not self.playfield[row][column]:  # No marker on placement tile
            adjacent_tile_coords = self.get_adjacent_opponent_tiles(player, coord_list)
            if adjacent_tile_coords:
                valid_tile = True
            else:
                valid_tile = False
        return valid_tile

    def place_marker(self, player, coord_list):
        if coord_list[0] in self.rowletters and coord_list[1] in self.columnnumbers:
            row = int(self.rowletters.index(coord_list[0]))
            column = int(self.columnnumbers.index(coord_list[1]))
            if self.valid_placement(player, [row, column]):
                self.playfield[row][column] = Marker(player.color)
                player.brick_counter = player.brick_counter - 1
                return 1
            else:
                print("Invalid move!")
                return 0
        else:
            print("Invalid move!")
            return 0


class Othello:
    def __init__(self):
        self.playfield = PlayField(8, 8)
        self.players = []
        for playernum in range(2):
            self.players.append(self.create_player())
        self.turn = 0

    def create_player(self):
        name = input("Name:")
        color_num = input("Color (1 for Black & 2 for White):")
        return Player(name, ['Black', 'White'][int(color_num)-1])

    def change_turn(self):
        self.turn = 1 - self.turn


def main():
    game = Othello()
    game_over = False
    while 1:
        game.playfield.draw()
        move = input("{}'s move:".format(game.players[game.turn].name))
        valid_move = game.playfield.place_marker(game.players[game.turn], [str(move[0]), str(move[1])])
        if valid_move:
            game.change_turn()
        print("{}'s tiles left: {}. \n{}'s tiles left: {}.".format(game.players[game.turn].name,
                                                                   game.players[game.turn].brick_counter,
                                                                   game.players[1 - game.turn].name,
                                                                   game.players[1 - game.turn].brick_counter))
        if game_over:
            break
    print("Game Over")


if __name__ == "__main__":
    main()
