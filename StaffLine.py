class StaffLine:

    def __init__(self, y, array):
        self.y = y
        self.array = array
        self.start_x = self.__get_start_x()
        self.end_x = self.__get_end_x()
        self.count = sum(array)

    def __get_start_x(self):
        x = 0
        for i in range(len(self.array)):
            if self.array[i] != 0:
                x = i
                return x
        return x

    def __get_end_x(self):
        x = len(self.array)-1
        for i in range(len(self.array)-1, 0, -1):
            if self.array[i] != 0:
                x = i
                return x
        return x
