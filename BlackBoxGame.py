# Author: Devin Barger
# Date: 08/07/2020
# Description: Program representing a fully functioning version of the Black Box Game.
from pprint import pprint

class Board:
    """
    Represents the playing board for BlackBoxGame.
    Inherited by BlackBoxGame when BlackBoxGame is initialized
    """

    def __init__(self):
        """
        Initialize a 10x10 board where 'o' represents
        ray entry points for the player to shoot
        """
        self._board = []

        for i in range(10):
            row = []
            for j in range(10):
                if i == 0 and (j == 0 or j == 9):
                    row.append('')
                elif i == 9 and (j == 0 or j == 9):
                    row.append('')
                elif (i == 0 or i == 9) or (j == 0 or j == 9):
                    row.append('o')
                else:
                    row.append(' ')
            self._board.append(row)
        return

    def print_board(self):
        """
        Print the board to console
        """
        pprint(self._board)
        return


class BlackBoxGame(Board):
    """
    Represents the game itself.
    Inherits Board which is a 10x10 grid with a blank slate.
    Defines methods that track player score, their moves and results of the moves
    """

    def __init__(self, atoms):
        """
        Initialize the game with the placement of the atoms on the board
        """
        super().__init__()

        self._atom_locations = []

        for atom in atoms:
            self._board[atom[0]][atom[1]] = 'X'
            self._atom_locations.append(atom)

        self._score = 25
        self._atoms_count = len(atoms)
        self._entry_locations = []
        self._exit_locations = []
        self._atom_guesses = []

    def get_score(self):
        """
        Returns the current score of the player

        :return: Integer, value of self._score
        """
        return self._score

    def set_score(self, value):
        """
        Update the players score

        :return:
        """
        self._score += value
        return

    def atoms_left(self):
        """
        Returns the number of atoms that haven't been guessed yet

        :return: Integer, number of atoms that have not yet been guessed by the player
        """
        return self._atoms_count

    def set_atoms_remaining(self, value):
        """
        Update the atoms_remaining count

        :param value: Integer value dictating how many atoms are remaining
        :return: Integer, length of the self._atoms_count list
        """
        self._atoms_count += value
        return self._atoms_count

    def get_atom_locations(self):
        """
        Return the locations of the atoms on the board

        :return: List, stores the tuple pairs of row, column where the atoms are located on the board
        """
        return self._atom_locations

    def get_atom_guesses(self):
        """
        Return the previous guesses of atom locations

        :return: List of tuples representing the atom location guesses
        """
        return self._atom_guesses

    def set_atom_guesses(self, row, column):
        """
        """
        self._atom_guesses.append((row, column))

    def guess_atom(self, row, column):
        """
        Takes in the row and column as parameters.
        If there is an atom at that location, return True. Else, False.
        Adjusts the player score appropriatley.

        :param row: Integer, the row on the board where the atom is thought to be
        :param column: Integer, the column on the board where the atom is thought to be
        :return: True if row,column guessed contains an atom. False otherwise.
        """
        atoms = self.get_atom_locations()

        for atom in atoms:
            if (row, column) == atom:
                # Correct guess, one less atom remaining
                self.set_atoms_remaining(-1)
                self.set_atom_guesses(row, column)
                return True
        # Incorrect Guess
        if (row, column) in self.get_atom_guesses():  # Already guessed, no point deduction
            return False
        else:
            self.set_atom_guesses(row, column)
            self.set_score(-5)
            return False

    def get_entry_locations(self):
        """
        Return the entry locations already used by the player

        :return: List, consists of row, column tuples representing entry locations when ray is shot
        """
        return self._entry_locations

    def set_entry_location(self, row, column):
        """
        Add the entry location of the ray to self._entry_locations

        :param row: Integer, the row specified by the user when shooting ray
        :param column: Integer, the column specified by the user shooting ray
        :return:
        """
        self._entry_locations.append((row, column))
        return

    def get_exit_locations(self):
        """
        Return the exit locations already used by the player

        :return: List, consists of row, column tuples representing exit locations after ray is shot
        """
        return self._exit_locations

    def set_exit_location(self, row, column):
        """
        Add the exit location of the ray to self._exit_locations

        :param row: Integer, the row where the ray exits the board after being shot
        :param column: Integer, the column where the ray exits the board after being shot
        :return:
        """
        self._exit_locations.append((row, column))
        return

    def south_ray(self, row, column):
        """
        If the shoot_ray row is == 0, then the ray will travel south across the board

        Recursively starts from row 0 and iterates to row 9, checking for hits and detours along the way.
        If detour is encountered, call function defining the new direction of the ray based on the deflection.

        :param row: Integer, represents the current row of the ray as it traverses the board
        :param column: Integer, represents the current column of the ray as it traverses the board

        :return: If encountering an atom directly, return 'HIT'.
                 If reaching the end of the board, return the tuple pair of current row, column
                 If atom is located in the next row, one column to the right, call self.west_ray(row, column)
                 If atom is located in the next row, one column to the left, call self.east_ray(row, column)
                 Else, recursively call itself and move to the next row
        """
        ray_position = [row, column]
        atom_locations = self.get_atom_locations()
        exit_locations = self.get_exit_locations()

        if tuple(ray_position) in atom_locations:
            exit_square = 'HIT'
            return exit_square

        elif row == 9:  # Ray traversed the entire board without hitting.
            exit_square = (row, column)
            if exit_square not in exit_locations:
                self.set_score(-1)
            return exit_square

        elif tuple([row + 1,
                    column + 1]) in atom_locations:  # Atom located in the next row down, one column to the right. Detour.
            return self.west_ray(row, column)

        elif tuple([row + 1,
                    column - 1]) in atom_locations:  # Atom located in the next row down, one column to the left. Detour.
            return self.east_ray(row, column)

        else:
            return self.south_ray(row + 1, column)  # Advance to the next row

    def north_ray(self, row, column):
        """
        If the shoot_ray row is == 9, then the ray will travel south across the board

        Recursively starts from row 9 and iterates to row 0, checking for hits and detours along the way.
        If detour is encountered, call function defining the new direction of the ray based on the deflection.

        :param row: Integer, represents the current row of the ray as it traverses the board
        :param column: Integer, represents the current column of the ray as it traverses the board

        :return: If encountering an atom directly, return 'HIT'.
                 If reaching the end of the board, return the tuple pair of current row, column
                 If atom is located in the next row, one column to the right, call self.west_ray(row, column)
                 If atom is located in the next row, one column to the left, call self.east_ray(row, column)
                 Else, recursively call itself and move to the next row
        """
        ray_position = [row, column]
        atom_locations = self.get_atom_locations()
        exit_locations = self.get_exit_locations()

        if tuple(ray_position) in atom_locations:
            exit_square = 'HIT'
            return exit_square

        elif row == 0:  # Ray traversed the entire board without hitting.
            exit_square = (row, column)
            if exit_square not in exit_locations:
                self.set_score(-1)
            return exit_square

        elif tuple([row - 1,
                    column + 1]) in atom_locations:  # Atom located in the next row up, one column to the right. Detour.
            return self.west_ray(row, column)

        elif tuple([row - 1,
                    column - 1]) in atom_locations:  # Atom located in the next row up, one column to the left. Detour.
            return self.east_ray(row, column)

        else:
            return self.north_ray(row - 1, column)  # Advance to the next row

    def east_ray(self, row, column):
        """
        If the shoot_ray column == 0, then the ray will travel east across the board

        Recursively starts from column 0 and iterates to column 9, checking for hits and detours along the way.
        If detour is encountered, call function defining the new direction of the ray based on the deflection.

        :param row: Integer, represents the current row of the ray as it traverses the board
        :param column: Integer, represents the current column of the ray as it traverses the board

        :return: If encountering an atom directly, return 'HIT'.
                 If reaching the end of the board, return the tuple pair of current row, column
                 If atom is located in the next column, one row above, call self.south_ray(row, column)
                 If atom is located in the next column, one row below, call self.north_ray(row, column)
                 Else, recursively call itself and move to the next column
        """
        ray_position = [row, column]
        atom_locations = self.get_atom_locations()
        exit_locations = self.get_exit_locations()

        if tuple(ray_position) in atom_locations:
            exit_square = 'HIT'
            return exit_square

        elif column == 9:  # Ray traversed the entire board without hitting
            exit_square = (row, column)
            if exit_square not in exit_locations:
                self.set_score(-1)
            return exit_square

        elif tuple([row - 1,
                    column + 1]) in atom_locations:  # Atom located in the row above, one column to the right. Detour.
            return self.south_ray(row, column)

        elif tuple([row + 1,
                    column + 1]) in atom_locations:  # Atom located in the row below, one column to the right. Detour.
            return self.north_ray(row, column)

        else:
            return self.east_ray(row, column + 1)

    def west_ray(self, row, column):
        """
        If the shoot_ray column == 9, then the ray will travel west across the board

        Recursively starts from column 9 and iterates to column 0, checking for hits and detours along the way.
        If detour is encountered, call function defining the new direction of the ray based on the deflection.

        :param row: Integer, represents the current row of the ray as it traverses the board
        :param column: Integer, represents the current column of the ray as it traverses the board

        :return: If encountering an atom directly, return 'HIT'.
                 If reaching the end of the board, return the tuple pair of current row, column
                 If atom is located in the next column, one row above, call self.south_ray(row, column)
                 If atom is located in the next column, one row below, call self.north_ray(row, column)
                 Else, recursively call itself and move to the next column
        """
        ray_position = [row, column]
        atom_locations = self.get_atom_locations()
        exit_locations = self.get_exit_locations()

        if tuple(ray_position) in atom_locations:
            exit_square = 'HIT'
            return exit_square

        elif column == 0:  # Ray traversed the entire board without hitting
            exit_square = (row, column)
            if exit_square not in exit_locations:
                self.set_score(-1)
            return exit_square

        elif tuple([row - 1,
                    column - 1]) in atom_locations:  # Atom located in the row above, one column to the left. Detour.
            return self.south_ray(row, column)

        elif tuple([row + 1,
                    column - 1]) in atom_locations:  # Atom located in the row below, one column to the left. Detour.
            return self.north_ray(row, column)

        else:
            return self.west_ray(row, column - 1)

    def valid_square(self, row, column):
        """
        Check if the row and column provided is a boarder square or corner square. If so, return False.

        :param row: Integer, represents the row from shoot_ray() to check if the row is valid boarder square
        :param column: Integer, represents the column from shoot_ray() to check if the column is valid boarder square

        :return: False if the entry location for shoot_ray() is corner square or boarder squre
        """
        if (row == 0 or row == 9) and (column == 0 or column == 9):  # Corner square, False
            return False
        elif (row != 0 and row != 9) and (column != 0 and column != 9):  # Non-boarder square, False
            return False
        else:
            return True

    def shoot_ray(self, row, column):
        """
        Player shoots a ray from the row, column specified. The row, column must be a boarder square.
        If the row is 0, then the ray will start out traveling south. Call self.south_ray(row, column)
        If the row is 9, then the ray will start out traveling north. Call self.north_ray(row, column)
        If the column is 0, then the ray will start out traveling east. Call self.east_ray(row, column)
        If the column is 9, then the ray will start out traveling west. Call self.west_ray(row, column)

        Each shot will check the existing entry/exit locations of previous shots to determine if a point needs
        to be deducted. Previous entry/exit locations do not count against the player.

        :param row: Integer, reperesents the row from which the user wants to shoot the ray
        :param column: Integer, represents the column from which the user wants to shoot the ray

        :return: If the row is a corner square or not a boarder square, return False
                 If the shot results in an atom hit, deduct 1 from atoms remaining and return None
                 Else, deduct additional point if the exit location has not been seen prior and return the exit location
        """
        entry_locations = self.get_entry_locations()
        exit_locations = self.get_exit_locations()

        if self.valid_square(row, column) is False:
            return False

        if (row, column) not in entry_locations and (row, column) not in exit_locations:
            self.set_score(-1)
            self.set_entry_location(row, column)

        if row == 0 and (1 <= column <= 8):  # Shoot ray south
            ray = self.south_ray(row, column)

        if row == 9 and (1 <= column <= 8):  # Shoot ray north
            ray = self.north_ray(row, column)

        if column == 0 and (1 <= row <= 8):  # Shoot ray east
            ray = self.east_ray(row, column)

        if column == 9 and (1 <= row <= 8):  # Shoot ray west
            ray = self.west_ray(row, column)

        if ray == 'HIT':
            return None
        else:
            self.set_exit_location(ray[0], ray[1])
            return ray

