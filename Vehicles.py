import numpy as np

class CarInterface:

    def __init__(self):
        self.logs = []

    #log the current state of the car
    def log(self):
        self.logs.append(self.get_range())

    #return logs
    def get_logs(self):
        return self.logs

    #returns make/model of the car
    def get_model(self):
        pass

    #returns range of car with full charge
    def get_max_range(self):
        pass

    #returns current range on the car (miles)
    def get_range(self):
        pass

    #returns current charge percent of car
    def get_charge(self):
        pass

    #returns max charge watts for car
    def get_max_charge(self):
        pass

    #simulate driving miles, adjusting range/charge
    def drive(self, miles):
        pass

class Vehicle(CarInterface):
    def __init__(self, model, charge = None):
        super().__init__()
        #all charging rates are in kW pe hour and assume level 2 charging
        if model =='ModelS':
            self.model = model
            self.max_charge = 95
            self.max_range = 570
            self.avg_cons = .152
            self.charging_rate = 11.5 #kW per hour
            

        elif model =='Mustang':
            self.model = model
            self.max_charge = 91
            self.max_range = 455
            self.avg_cons = .152
            self.charging_rate = 23 #temporary number need to figure out real one

        elif model =='Ioniq':
            self.model = model
            self.max_charge = 74
            self.max_range = 390
            self.avg_cons = .127
            self.charging_rate = 11
            
        elif model =='Kia':
            self.model = model
            self.max_charge = 64.8
            self.max_range = 380
            self.avg_cons = .140
            self.charging_rate = 7.4
            
        else:
            raise IndexError("Illegal car model")
            
        if charge == None:
            self.charge = np.random.uniform(0.2*self.max_charge, 0.8*self.max_charge)
        else: 
            self.charge = charge
        self.charge_percent = self.charge / self.max_charge
            
    def get_model(self):
        return self.model

    def get_max_range(self):
        return self.max_range

    def get_range(self):
        return self.charge / self.max_charge * self.max_range 

    def get_charge(self):
        return self.charge

    def get_max_charge(self):
        return self.max_charge
    
    def get_avg_cons(self):
        return self.avg_cons

    def drive(self, distance):
        self.charge -= distance*self.avg_cons

    def get_energy_needed(self, target=0.8):
        energy_needed = self.max_range * self.avg_cons * (target - self.charge_percent)
        return energy_needed
    
    def get_charging_time(self, energy_needed):
        return energy_needed / self.charging_rate
    
    def charge_car(self, energy):
        percent = energy / self.max_charge
        self.charge += percent
        self.charge_percent += percent
