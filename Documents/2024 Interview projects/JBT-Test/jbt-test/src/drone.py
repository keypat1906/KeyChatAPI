
# Class of Drone 


class Drone():

    def __init__(self, range):
        self.address = ''
        self.total_distance = 0
        self.drone_range = range

    def set_address(self, address):
        self.address = address
    
    def set_distance(self, distance):
        self.total_distance += distance
        
    def get_remaining_range(self):
        return self.drone_range - self.total_distance
    


drone = Drone(25)

