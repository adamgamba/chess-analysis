import numpy as np

square_activity = np.zeros(64, dtype=int)
white_moves = []
black_moves = []
total_moves = 0
number_of_games = 0
# How many times each piece takes another piece
kills_by_piece = {"P": 0, "R":0, "N":0, "B":0, "Q":0, "K":0}
# Percent usage of each piece
usage_by_piece = {"P": 0, "R":0, "N":0, "B":0, "Q":0, "K":0}
# Combined black & white number of each piece
number_of_piece = {'P': 16,'N': 4, 'B': 4, 'R': 4, 'Q': 2, 'K': 2}
piece_list = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
white_win = 0
black_win = 0
draw = 0
result = ""

# Used in calculating the MVP (most valuable piece)
usage_by_piece_game = {"P": 0, "R":0, "N":0, "B":0, "Q":0}
kills_by_piece_game = {"P": 0, "R":0, "N":0, "B":0, "Q":0}
most_valuable_piece = {"P": 0, "R":0, "N":0, "B":0, "Q":0}

# Corresponding index of all 64 squares on the chess board
square_indices = {
    "a1" : 0, "b1" : 1, "c1" : 2, "d1" : 3, "e1" : 4, "f1" : 5, "g1" : 6, "h1" : 7,
    "a2" : 8, "b2" : 9, "c2" : 10, "d2" : 11, "e2" : 12, "f2" : 13, "g2" : 14, "h2" : 15,
    "a3" : 16, "b3" : 17, "c3" : 18, "d3" : 19, "e3" : 20, "f3" : 21, "g3" : 22, "h3" : 23,
    "a4" : 24, "b4" : 25, "c4" : 26, "d4" : 27, "e4" : 28, "f4" : 29, "g4" : 30, "h4" : 31,
    "a5" : 32, "b5" : 33, "c5" : 34, "d5" : 35, "e5" : 36, "f5" : 37, "g5" : 38, "h5" : 39,
    "a6" : 40, "b6" : 41, "c6" : 42, "d6" : 43, "e6" : 44, "f6" : 45, "g6" : 46, "h6" : 47,
    "a7" : 48, "b7" : 49, "c7" : 50, "d7" : 51, "e7" : 52, "f7" : 53, "g7" : 54, "h7" : 55,
    "a8" : 56, "b8" : 57, "c8" : 58, "d8" : 59, "e8" : 60, "f8" : 61, "g8" : 62, "h8" : 63
}
# Dictionary of the 20 possible white opening moves corresponding to [uses, successes]
white_openings = {
    "a3" : [0,0], "a4" : [0,0], "b3" : [0,0], "b4" : [0,0],
    "c3" : [0,0], "c4" : [0,0], "d3" : [0,0], "d4" : [0,0],
    "e3" : [0,0], "e4" : [0,0], "f3" : [0,0], "f4" : [0,0],
    "g3" : [0,0], "g4" : [0,0], "h3" : [0,0], "h4" : [0,0],
    "Na3" : [0,0], "Nc3" : [0,0], "Nf3" : [0,0], "Nh3" : [0,0]
}

# Dictionary of the 20 possible black opening moves corresponding to [uses, successes]
black_openings = {
    "a6" : [0,0], "a5" : [0,0], "b6" : [0,0], "b5" : [0,0],
    "c6" : [0,0], "c5" : [0,0], "d6" : [0,0], "d5" : [0,0],
    "e6" : [0,0], "e5" : [0,0], "f6" : [0,0], "f5" : [0,0],
    "g6" : [0,0], "g5" : [0,0], "h6" : [0,0], "h5" : [0,0],
    "Na6" : [0,0], "Nc6" : [0,0], "Nf6" : [0,0], "Nh6" : [0,0]
}

#---------------------------------------------------------------------------------#

def clean_gameplay(gameplay):
    gameplay_edited = gameplay
    global white_moves, black_moves
    white_moves = []
    black_moves = []

    # Remove periods after numbers
    for i in range(len(gameplay)):
        if gameplay[i] == ".":
            gameplay_edited = gameplay_edited[:i] + " " + gameplay_edited[i+1:]

    # Split gameplay into words
    split = gameplay_edited.split(' ')

    # Convert move numbers to ints
    for i in range(len(split)):
        if split[i].isdigit():
            split[i] = int(split[i])

    # The result is the final element of the list
    global result
    result = split[-1]
    split = split[:-1]

    # Append to white_moves and black_moves lists
    for i in range(len(split)):
        if i % 3 == 0:
            continue
        elif (i-1) % 3 == 0:
            white_moves.append(split[i])
        else:
            black_moves.append(split[i])

#---------------------------------------------------------------------------------#

def update_data(moves, color, result):
    # Update openings and results, this happens once per game
    # Make the variables global to be updated
    global white_win, black_win, draw, number_of_games, total_moves
    
    opening = moves[0]
    if color == "white":
        if opening in white_openings.keys():
            white_openings[opening][0] += 1
            if result == "1-0":
                white_openings[opening][1] += 1
                white_win += 1
            elif result == "1/2-1/2":
                draw += 1  
    else:
        if opening in black_openings.keys():
            black_openings[opening][0] += 1
            if result == "0-1":
                black_openings[opening][1] += 1
                black_win += 1
    
    number_of_games += 0.5
    total_moves += len(moves)
    
    # Reset these dicionaries each game to count the moves
    usage_by_piece_game = {"P": 0, "R":0, "N":0, "B":0, "Q":0}
    kills_by_piece_game = {"P": 0, "R":0, "N":0, "B":0, "Q":0}
    
    # For loop to look at every move in a game
    for move in moves:
        # Find which piece is moving
        piece = ""
        # There are a few games with a rare error this fixes
        try:
            if move[0].isupper():
                piece = move[0]
            else:
                piece = "P"
        except:
            break
        
        # Usage of each piece type
        if piece != "O":
            usage_by_piece[piece] += 1
            if piece != "K":
                usage_by_piece_game[piece] += 1
        
        # Update kills_by_piece
        if "x" in move:
            if move[0].isupper():
                kills_by_piece[move[0]] += 1
                if move[0] != "K":
                    kills_by_piece_game[move[0]] += 1
            else:
                kills_by_piece["P"] += 1
                kills_by_piece_game["P"] += 1
        
        # Update square_activity
        # Kingside Castle
        if move == "O-O":
            if color == "white":
                square_activity[5] += 1
                square_activity[6] += 1
            else:
                square_activity[61] += 1
                square_activity[62] += 1
        # Queenside Castle
        elif move == "O-O-O":
            if color == "white":
                square_activity[2] += 1
                square_activity[3] += 1
            else:
                square_activity[58] += 1
                square_activity[59] += 1
        else:
            if move[-1] == "+":
                move = move[:-1]
            move = move[-2:]
            square_activity[square_indices.get(move)] += 1
    
    # This runs at the end of each game, IF it was a winning game
    if (color == "white" and result == "1-0") or (color == "black" and result == "0-1"):
        # Calculates usage and kills by piece within the game
        for key in usage_by_piece_game.keys():
            usage_by_piece_game[key] /= number_of_piece[key] / 2
            kills_by_piece_game[key] /= number_of_piece[key] / 2
        
        # Finds the piece with the highest usage score for this game
        # Adds the winner(s) to the MVP list
        maximum = max(usage_by_piece_game.values())
        for key, value in usage_by_piece_game.items():
            if value == maximum:
                most_valuable_piece[key] += 1
        
        # Finds the piece with the highest kills score for this game
        # Adds the winner(s) to the MVP list
        maximum = max(kills_by_piece_game.values())
        for key, value in kills_by_piece_game.items():
            if value == maximum:
                most_valuable_piece[key] += 1

#---------------------------------------------------------------------------------#

import os, glob, time

time_start = time.time()
gameplay = ""
count_completed = 1
#path = "C:\\Users\\Adam\\KingBase2019-pgn\\" #Home
#path = 'C:\\Users\\agamba\\KingBase2019-pgn\\' #School
path = 'C:\\Users\\adamg\\OneDrive\\Documents\\Adam 12\\Computer Science\\Final Project\\KingBaseShort' #Short
os.chdir(path)

# Creates a list of all files with the .pgn extension
# Portable Game Notation, file type of the dataset
filenames = glob.glob("*.pgn")
#filenames = ["KingBaseShort.txt"]

for file in filenames:
    with open(path + file) as f:
        first = True
        for line in f:
            line = line.strip()
            # Ignores other junk in the file
            if len(line) <= 1 or line[0] == "[":
                continue
            # First move in the game
            elif line[:2] == "1.":
                if (not first):
                    # Call methods
                    count_completed += 1
                    if count_completed % 1000 == 0:
                        print(count_completed)
                    clean_gameplay(gameplay)
                    update_data(white_moves, "white", result)
                    update_data(black_moves, "black", result)  
                # Start new gameplay
                gameplay = line
                first = False
            # Appends further lines in the game to the string
            else:
                if gameplay.endswith("."):
                    gameplay += line
                elif gameplay.endswith(" "):
                    gameplay += line
                else:
                    gameplay += " " + line

        # Final iteration of loop 
        clean_gameplay(gameplay)
        update_data(white_moves, "white", result)
        update_data(black_moves, "black", result)

#---------------------------------------------------------------------------------#

# Print final results
print("Final Results:")
time_end = time.time() - time_start
print("{:.2f} seconds".format(time_end))
print()
print("Kills by Piece:")
print(kills_by_piece)
print("Usage by Piece:")
print(usage_by_piece)

print()
print("Square Activity:")
print(square_activity)

print()
# Remove openings which haven't been used
for key in list(white_openings):
    if white_openings[key][0] == 0:
        del(white_openings[key])
print("White Openings [uses, successes]:")
print(white_openings)

for key in list(black_openings):
    if black_openings[key][0] == 0:
        del(black_openings[key])
print("Black Openings [uses, successes]:")
print(black_openings)

print()
print("Number of Games:")
print(int(number_of_games))
print("Toal Moves:")
print(total_moves)
if number_of_games > 0:
    print("Average Moves per Game:")
    print("{:.2f}".format(total_moves / number_of_games))

    print("White Win Percentage")
    print("{:.2f}".format(white_win/number_of_games*100))

    print("Black Win Percentage")
    print("{:.2f}".format(black_win/number_of_games*100))

    print("Draw Percentage")
    print("{:.2f}".format(draw/number_of_games*100))

print()
print("Most Valuable Piece")
print(most_valuable_piece)

#---------------------------------------------------------------------------------#

# Convert values in dictionary to percentages by dividing by the sum
piece_ratings = most_valuable_piece
sum_MVP = sum(piece_ratings.values())
for key in piece_ratings.keys():
    piece_ratings[key] /= sum_MVP

for key in piece_ratings.keys():
    if key != "P":
        # Divide all non-pawn values by the pawn value to get relative scores
        piece_ratings[key] /= piece_ratings["P"]
        # Take the square root to shrink values to be more realistic
        piece_ratings[key] = piece_ratings[key] ** 0.5
piece_ratings["P"] = 1

print()
print("Final Piece Ratings")
print(piece_ratings)

#---------------------------------------------------------------------------------#
import matplotlib.pyplot as plt

# Create a new usage/kills dictionary that finds uses/kills per piece for each game, on average
# Divide by number_of_piece to look at a specific piece, not a whole piece type
# Update names of new dictionary to use name, not just first letter
new_usage = {}
for key, piece in zip(usage_by_piece.keys(), piece_list):
    new_usage[piece] = usage_by_piece[key]/number_of_piece[key]/number_of_games

new_kills = {}
for key, piece in zip(kills_by_piece.keys(), piece_list):
    new_kills[piece] = kills_by_piece[key]/number_of_piece[key]/number_of_games

# Plot a bar graph with 2 series
plt.bar(new_usage.keys(), new_usage.values(), color = 'g', label = "Moves")
plt.bar(new_kills.keys(), new_kills.values(), color = 'r', label = "Kills")
plt.title("Number of Moves and Kills per Piece per Game")
plt.xlabel("Piece")
plt.ylabel("Moves (Green) and Kills (Red)")
plt.legend()
plt.savefig("Moves_Kills_Graph.png", dpi=1000)
plt.show()

#---------------------------------------------------------------------------------#
# Calculate win percentages
white_win_percent = round(white_win/number_of_games*100, 2)
black_win_percent = round(black_win/number_of_games*100, 2)
draw_percent = round(draw/number_of_games*100,2)

# Plot a pie chart of white wins, black wins, and draws
plt.pie([white_win_percent, black_win_percent, draw_percent],
        labels = ["White: {}%".format(white_win_percent), "Black: {}%".format(black_win_percent), "Draw: {}%".format(draw_percent)],
        colors = ["w", "k", "lightblue"], startangle = 90,
        wedgeprops={"edgecolor" : "k", 'linewidth' : 3, 'antialiased' : True})
plt.title("Game Outcomes")
plt.savefig("Game_Outcomes_Pie.png", dpi=1000)
plt.show()

#---------------------------------------------------------------------------------#

# Take the uses of each of the 20 white openings and put them in a new list 
white_openings_uses = []
for arr in white_openings.values():
    white_openings_uses.append(arr[0])

# Do the same for the 20 black openings
black_openings_uses = []
for arr in black_openings.values():
    black_openings_uses.append(arr[0])

top_white_successes = {}
top_black_successes = {}

# Sort the list and shorten it to the 5 most common openings
white_openings_uses = sorted(white_openings_uses, reverse = True)[:5]
for value in white_openings_uses:
    for key in white_openings.keys():
        # Create a new dictionary with only the sorted top 5 
        if value == white_openings[key][0]:
            top_white_successes[key] = white_openings[key][1] / value

# Sort the list and shorten it to the 5 most common openings
black_openings_uses = sorted(black_openings_uses, reverse = True)[:5]
for value in black_openings_uses:
    for key in black_openings.keys():
        # Create a new dictionary with only the sorted top 5 
        if value == black_openings[key][0]:
            top_black_successes[key] = black_openings[key][1] / value

# Create a bar graph with the win rates of the 5 most common white openings
# Plot against the accepted win rate for white
plt.bar(top_white_successes.keys(), top_white_successes.values(), label = "White", color = "lightblue")
plt.bar(["White", ""], [white_win_percent/100, 0], label = "Overall White Win Rate", color = "g")

# Create a bar graph with the win rates of the 5 most common black openings
# Plot against the accepted win rate for black
plt.bar(top_black_successes.keys(), top_black_successes.values(), label = "Black", color = "k")
plt.bar("Black", black_win_percent/100, label = "Overall Black Win Rate", color = "g")

plt.title("Win Rates of 5 Most Common White and Black Openings")
plt.xlabel("Opening")
plt.ylabel("Win Rate")
plt.legend()
plt.ylim(0,0.5)
plt.savefig("Opening_Win_Rates.png", dpi = 1000)
plt.show()
