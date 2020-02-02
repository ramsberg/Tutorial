

class Bricka:
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
    def __init__(self,rows=8, columns=8):
        self.colors_dict = {'Black': chr(9675), 'White': chr(9679)}
        self.rows = rows
        self.columns = columns
        self.rowletters = ['a','b','c','d','e','f','g','h']
        self.columnnumbers = ['1','2','3','4','5','6','7','8']
        self.create()
        self.setup()

    def setup(self):
        self.playfield[3][3] = Bricka("White")
        self.playfield[3][4] = Bricka("Black")
        self.playfield[4][3] = Bricka("Black")
        self.playfield[4][4] = Bricka("White")

    def create(self):
        self.playfield = []
        for row in range(self.rows):
            self.playfield.append([None] * self.columns)

    def draw(self):
        self.column_line = "  "
        self.cover_line = "  "
        for column in range(self.columns):
            self.column_line = self.column_line+str(self.columnnumbers[column])+" "
#        for column in range(self.columns):
#            self.cover_line = self.cover_line+"--"
        print(self.column_line)
#        print(self.cover_line)
        for row in range(self.rows):
            current_row= self.rowletters[row]+"|"
            for column in range(self.columns):
                if self.playfield[row][column]:
                    current_row = current_row + self.colors_dict[self.playfield[row][column].color]
                else:
                    current_row = current_row +" "
                if column != self.columns:
                    current_row = current_row + "|"
            print(current_row)
#        print(self.cover_line)

    def place_marker(self, player, coord_list):
        player.brick_counter = player.brick_counter - 1
        row = self.rowletters.index(coord_list[0])
        column = self.columnnumbers.index(coord_list[1])
        if not self.playfield[row][column]:
            self.playfield[row][column] = Bricka(player.color)
            return(1)
        else:
            print("Invalid move!")
            return(0)


class Othello:
    def __init__(self):
        self.playfield = PlayField(8, 8)
        self.players = []
        for playernum in range(2):
            self.players.append( self.create_player() )
        self.turn = 0

    def create_player(self):
        name = input("Name:")
        color_num = input("Color (1 for Black & 2 for White):")
        return Player(name,['Black','White'][int(color_num)-1])

    def change_turn(self):
        self.turn = 1 - self.turn


def main():
    game = Othello()
    while 1:
        game.playfield.draw()
        move = input("{}'s move:".format(game.players[game.turn].name))
        valid_move = game.playfield.place_marker( game.players[game.turn], [str(move[0]),str(move[1])] )
        if valid_move:
            game.change_turn()


if __name__ == "__main__":
    main()




