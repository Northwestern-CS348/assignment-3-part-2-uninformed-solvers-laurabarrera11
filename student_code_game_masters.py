from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        peg1 = []
        peg2 = []
        peg3 = []
        input_parsed = parse_input("fact: (inst ?peg peg)")
        all_pegs = self.kb.kb_ask(input_parsed)
        for every_peg in all_pegs:
            if not Fact(instantiate(Statement(("empty", "?peg")), every_peg)) in self.kb.facts:
                all_disks = self.kb.kb_ask(Fact(instantiate(Statement(("on", "?disk", "?peg")), every_peg)))
                all_disks_int = []
                for every_disk in all_disks:
                    disk_int = int(every_disk.bindings_dict["?disk"][4])
                    all_disks_int.append(disk_int)
                peg_int = int(every_peg.bindings_dict["?peg"][3])
                if peg_int == 1:
                    if all_disks_int:
                        while all_disks_int:
                            min_disk = min(all_disks_int)
                            peg1.append(min_disk)
                            all_disks_int.remove(min_disk)
                elif peg_int == 2:
                    if all_disks_int:
                        while all_disks_int:
                            min_disk = min(all_disks_int)
                            peg2.append(min_disk)
                            all_disks_int.remove(min_disk)
                else:
                    if all_disks_int:
                        while all_disks_int:
                            min_disk = min(all_disks_int)
                            peg3.append(min_disk)
                            all_disks_int.remove(min_disk)
        return (tuple(peg1), tuple(peg2), tuple(peg3))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        ### Student code goes here

        all_terms = movable_statement.terms
        start = all_terms[1]
        end = all_terms[2]
        disk = all_terms[0]

        new_top_disk = self.kb.kb_ask(Fact(Statement(("onTop", disk, "?obj"))))[0]
        old_top_end = self.kb.kb_ask(Fact(Statement(("top", "?obj", end))))[0]

        new_top_fact = Fact(instantiate(Statement(("onTop", disk, "?obj")), new_top_disk))
        old_top_fact = Fact(instantiate(Statement(("top", "?obj", end)), old_top_end))

        new_start_top_fact = Fact(instantiate(Statement(("top", "?obj", start)), new_top_disk))
        new_old_top_fact = Fact(instantiate(Statement(("onTop", disk, "?obj")), old_top_end))

        self.kb.kb_retract(Fact(Statement(("on", disk, start))))
        self.kb.kb_retract(Fact(Statement(("top", disk, start))))
        self.kb.kb_retract(new_top_fact)
        self.kb.kb_retract(old_top_fact)
        self.kb.kb_assert(Fact(Statement(("on", disk, end))))
        self.kb.kb_assert(Fact(Statement(("top", disk, end))))
        self.kb.kb_assert(new_start_top_fact)
        self.kb.kb_assert(new_old_top_fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        current = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        rows = {"pos1": ("pos1", "pos2", "pos3"),
                "pos2": ("pos1", "pos2", "pos3"),
                "pos3": ("pos1", "pos2", "pos3")}

        for y_cord in rows:
            y = int(y_cord[3]) - 1
            for x_cord in rows[y_cord]:
                x = int(x_cord[3]) - 1
                ask = self.kb.kb_ask(Fact(Statement(["coordinate", "?tile", x_cord, y_cord])))[0]
                tile = ask.bindings_dict["?tile"][4]
                tile_val = 0
                if tile == 'y':
                    tile_val = -1
                else:
                    tile_val = int(tile)
                current[y][x] = tile_val

        return tuple([tuple(current[0]), tuple(current[1]), tuple(current[2])])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        ### Student code goes here

        all_terms = movable_statement.terms
        current_tile = all_terms[0]
        start_x = all_terms[1]
        end_x = all_terms[3]
        start_y = all_terms[2]
        end_y = all_terms[4]

        self.kb.kb_retract(Fact(Statement(("coordinate", "empty", end_x, end_y))))
        self.kb.kb_retract(Fact(Statement(("coordinate", current_tile, start_x, start_y))))

        self.kb.kb_assert(Fact(Statement(("coordinate", "empty", start_x, start_y))))
        self.kb.kb_assert(Fact(Statement(("coordinate", current_tile, end_x, end_y))))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))