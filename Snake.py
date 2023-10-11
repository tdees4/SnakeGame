class SnakeNode:
    """
    Represents one "node" of a snake (Each node occupies one
    grid square)
    """

    def __init__(self, location, next=None):
        self.location = location
        if next:
            self.next = next
        else:
            self.next = None


class Snake:
    """
    Represents the combination of nodes that make up an
    entire snake
    """

    def __init__(self, location, direction):
        self.head = SnakeNode(location)
        self.direction = direction
        self.growing = False

    def size(self):
        """
        :return: The total size of the snake in grid squares
        """

        temp, counter = self.head, 0
        while temp is not None:
            counter += 1
            temp = temp.next
        return counter

    def get_location(self, index):
        """
        :param index: Gets the location of the indexed snake
        body node
        :return: The snake node that is indexed (if the index > the size
        of the snake it will return the tail node)
        """

        temp = self.head
        while temp is not None and index > 0:
            index -= 1
            temp = temp.next
        return temp.location

    def set_location(self, index, location):
        """
        Moves the snake body node to the specified location
        :param index: The index of the targeted snake node
        :param location: The new location of the snake node
        """

        temp = self.head
        while temp is not None and index > 0:
            index -= 1
            temp = temp.next
        temp.location = location

    def check_location(self, location):
        """
        :param location: Checks if the snake has a node at the given
        location
        :return: True if the snake has a node at the location, false
        otherwise
        """

        for i in range(self.size()):
            if self.get_location(i) == location:
                return True
        return False

    def grow(self):
        """
        The snake adds one node onto the end after its next movement
        """

        self.growing = True

    def move(self):
        """
        Moves the head of the snake by one grid spot into the direction that it is facing
        while all following nodes move in the direction of the next node
        """

        loc = (self.head.location[0] + self.direction[0], self.head.location[1] + self.direction[1])
        temp = self.head

        while temp.next is not None:
            temploc = temp.location
            temp.location = loc
            loc = temploc
            temp = temp.next

        if self.growing:
            self.growing = False
            tmploc = temp.location
            temp.location = loc
            temp.next = SnakeNode(tmploc)
        else:
            temp.location = loc

    def get_direction(self, index):
        """
        :param index: The index of the body node (0 is the head)
        :return: The direction of the indexed body node
        """

        if index == 0:
            return self.direction
        else:
            return (
                self.get_location(index - 1)[0] - self.get_location(index)[0],
                self.get_location(index - 1)[1] - self.get_location(index)[1]
            )

    def set_direction(self, direction):
        """
        :param direction: The direction that the head will
        move toward
        """

        self.direction = direction

    def draw(self, grid):
        """
        Draws the snake onto the given grid
        :param grid: The grid to draw the snake on
        """

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if self.check_location((col, row)):
                    grid[row][col] = 1
                elif grid[row][col] == 1:
                    grid[row][col] = 0
