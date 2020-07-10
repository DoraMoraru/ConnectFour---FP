class Valid :
    def __init__(self):
        pass

    def check_valid_input(self,col):
    #this function check if the input is valid and if not, raises a Value Error
        if col < 0 or col > 6 :
            raise ValueError("not valid input! it must be between 0 and 6 ")