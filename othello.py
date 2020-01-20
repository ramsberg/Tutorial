

class Bricka:
    allowed_colors=['B','W']
    def __init__(self color=None):
        if color and color in allowed_colors:
            self.color = color
        else:
            raise

    def get_color(self):
        return self.color
    def turn_over(self):


def create_playfield(rows=8, columns=8):
    playfield = []
    for row in range(rows):
        playfield.append([0] * columns)
    return playfield

def print_playfield(playfield):
    for column in range(len(playfield[row])):

    for row in range(len(playfield)):
        current_row= ""
        for column in range(len(playfield[row])):
            if playfield[row][column]:
                current_row = current_row + playfield[row][colum].color
            else:
                current_row = current_row +"O"

        print(current_row)




def main():
    p=create_playfield()
    print_playfield(p)


if __name__ == "__main__":
    main()




