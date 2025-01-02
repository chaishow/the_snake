class Vector2:
    """New type to present a mathematic
    Vector in 2 dimensions.
    """

    def __init__(self, *args):

        # Case for collections
        if len(args) == 1:
            arg = args[0]

            # Case for make copy of Vector2
            if isinstance(arg, Vector2):
                self.x, self.y = arg.x, arg.y

            # Case for tuples and lists
            elif (
                isinstance(arg, (tuple, list))
                and len(arg) == 2
                and all(isinstance(i, int) for i in arg)
            ):
                self.x, self.y = arg

            else:
                raise ValueError(f'Invalid arguments for Vector2: {args}')

        # Case for two different args
        elif len(args) == 2 and all(isinstance(i, int) for i in args):
            self.x, self.y = args

        else:
            raise ValueError(f'Invalid arguments for Vector2: {args}')

    def __add__(self, other):
        """Method to Adding
        of two vectors.
        """
        if not isinstance(other, Vector2):
            raise TypeError('Can only add Vector2 with a Vector2')
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        """Multiply vector
        by number.
        """
        if not isinstance(other, int):
            raise TypeError('Can only multiply Vector2 by a number')
        return Vector2(self.x * other, self.y * other)

    def __sub__(self, other):
        """Substraction of two
        vetors.
        """
        if not isinstance(other, Vector2):
            raise TypeError('Can only substract Vector2 with a Vector 2')
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
        """Return a human-readable
        string representation of
        vector.
        """
        return f'{(self.x, self.y)}'

    def __mod__(self, other):
        """If other is int returns mods of every coordinate,
        if other is Vector 2 divides the corresponding
        coordinates into each other.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x % other.x, self.y % other.y)
        elif isinstance(other, int):
            return Vector2(self.x % other, self.y % other)
        else:
            raise TypeError('Can only % with types Vector2, int')

    def __hash__(self):
        """Redifinded to can
        return Vector2 to tupple.
        """
        return hash((self.x, self.y))
