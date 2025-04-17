import LCD1602

class View:
    def __init__(self):
        pass
    
    @staticmethod
    def display_message(message):
        LCD1602.clear()
        LCD1602.write(0, 0, message)
    
    @staticmethod
    def display_two_lines(line1, line2):
        LCD1602.clear()
        LCD1602.write(0, 0, line1)
        LCD1602.write(0, 1, line2)