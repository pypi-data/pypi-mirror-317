class Pattern:
    def print_triangle(self, rows):
        """Prints a triangle pattern."""
        for i in range(1, rows + 1):
            print("*" * i)

    def print_reverse_triangle(self, rows):
        """Prints a reverse triangle pattern."""
        for i in range(rows, 0, -1):
            print("*" * i)

    def print_pyramid(self, rows):
        """Prints a pyramid pattern."""
        for i in range(1, rows + 1):
            print(" " * (rows - i) + "*" * (2 * i - 1))

    def print_diamond(self, rows):
        """Prints a diamond pattern."""
        for i in range(1, rows + 1):
            print(" " * (rows - i) + "*" * (2 * i - 1))
        for i in range(rows - 1, 0, -1):
            print(" " * (rows - i) + "*" * (2 * i - 1))

    def print_square(self, size):
        """Prints a square pattern."""
        for i in range(size):
            print("*" * size)

    def print_hollow_square(self, size):
        """Prints a hollow square pattern."""
        for i in range(size):
            if i == 0 or i == size - 1:
                print("*" * size)
            else:
                print("*" + " " * (size - 2) + "*")

    def print_right_triangle(self, rows):
        """Prints a right-aligned triangle pattern."""
        for i in range(1, rows + 1):
            print(" " * (rows - i) + "*" * i)

    def print_hollow_triangle(self, rows):
        """Prints a hollow triangle pattern."""
        for i in range(1, rows + 1):
            if i == 1 or i == rows:
                print("*" * i)
            else:
                print("*" + " " * (i - 2) + "*")

    def print_zigzag(self, rows, cols):
        """Prints a zigzag pattern."""
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

    def print_checkerboard(self, rows, cols):
        """Prints a checkerboard pattern."""
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
