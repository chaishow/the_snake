class Vector2:
    """New type to present a mathematic
    Vector in 2 dimensions.
    """

    def __init__(self, *args):
        self.x = 0
        self.y = 0
        if len(args) == 1:
            if type(args[0]) is Vector2:
                self.x = args[0].x
                self.y = args[0].y
                return
            if type(args[0]) is tuple or type(args[0]) is list:
                if all([type(i) is int for i in args[0]]):
                    self.x = args[0][0]
                    self.y = args[0][1]
                    return None
                else:
                    return None
            else:
                return None
        elif len(args) == 2:
            if all([type(i) is int for i in args]):
                self.x = args[0]
                self.y = args[1]
                return None
            else:
                return None
        else:
            return None

    def __add__(self, other):
        """Method to Adding
        of two vectors.
        """
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector2(new_x, new_y)

    def __mul__(self, other):
        """Multiply vector
        by number.
        """
        return Vector2(self.x * other, self.y * other)

    def __sub__(self, other):
        """Substraction of two
        vetors.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """Returns negative
        vetor.
        """
        return Vector2(-self.x, -self.y)

    def __eq__(self, other):
        """Check equallity between
        two vectors.
        """
        if not type(other) is Vector2:
            return False
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        """Defind to make unpacking by
        two coordinates.
        """
        return iter((self.x, self.y))

    def __str__(self):
        """Return string with
        string introdaction of
        vector.
        """
        return f'{(self.x, self.y)}'

    def __hash__(self):
        return hash((self.x, self.y))
