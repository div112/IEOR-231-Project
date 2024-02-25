import numpy as np

class AgentInterface:

    def __init__(self):
        self.logs = []
        self.charge_cost = {"naive": 0, "scheduled": 0, "None": 0}
        self.energy_charged = {"naive": 0, "scheduled": 0, "None": 0} 
        self.time_charged = {"naive": 0, "scheduled": 0, "None": 0}
        self.charging_method = "None"
        self.distance_driven = 0
        self.energy_used = 0
    
    #log the current state of the Agent
    def log(self, time):
        self.logs.append({"time": time,
                          "location": self.location,
                          "busy": self.busy,
                          "charge": self.get_car().get_charge(),
                          "charging_method": self.charging_method,
                          "naive_cost": self.charge_cost["naive"],
                          "scheduled_cost": self.charge_cost["scheduled"],
                          "naive_charged_energy": self.energy_charged["naive"], 
                          "scheduled_charged_energy": self.energy_charged["scheduled"], 
                          "naive_charged_time": self.time_charged["naive"], 
                          "scheduled_charged_time": self.time_charged["scheduled"], 
                          "distance_driven": self.distance_driven,
                          "energy_used": self.energy_used})
    
    #return the logs
    def get_logs(self):
        return self.logs

    #returns agent id
    def get_id(self):
        return self.driver_id

    #returns agent's nth car
    def get_car(self, n = 0):
        return self.cars[n]

    #return "drive", "charge", or None
    def get_action(self, time):
        pass

    #return desired location to drive if taking "drive" action
    def drive_location(self, time):
        pass

    def get_charge_method(self, time):
        pass

    #assumption: driving 60km/h
    def update_location(self):
        if self.driving == True:
            #BUG TO WATCH OUT FOR: self.location being an int??? there is currently a hacky fix
            self.location = self.location.astype(np.float64) + self.direction
            if np.linalg.norm(self.location-self.destination) <= 0.5 :
                self.location = self.destination
                self.driving = False
                self.busy = False

    def update_busy(self):
        self.busy_until -= 1
            
    #return boolean if the agent is currently doing another action (like driving or charging)
    def is_busy(self, time):   
        ## When is the agent busy?
        return self.busy_until > 0
    
    #return agent's current location
    def get_location(self):            
        return self.location

    #adjust location and car info
    def drive(self, destination, time):
        if not (destination - self.location).any():
            return
        self.driving = True
        self.busy = True
        self.destination = destination
        
        travel = destination-self.location
        distance = np.linalg.norm(travel)
        self.direction = travel/distance
        if self.direction[0] == np.nan:
            self.direction = np.array([0, 0])
        ## We could also update the state of charge in the same way that
        ## we update the location in order to see how the SOC changes 
        ## over time more exactly
        self.cars[0].drive(distance)

        self.busy_until = distance
        self.distance_driven += distance

    #decide how long to leave the car plugged in
    def plug_duration(self, time, station):
        if self.charging_method == "scheduled":
            # Implement logic for scheduling charge based on price drops over a 6 hour time period
            return 30 #temporary (should return 2 things, start time, then duration)
        elif self.charging_method == "naive":
            # Charge the car from the time of plug-in to 80%
            
            car = self.get_car()
            target = .8 * car.get_max_range()
            current = car.get_charge()
            assert target > current
            diff = target - current
            return diff / station.get_power()
            return min((0.8 - self.get_car().get_charge()) * self.get_car().get_max_range() / self.get_car().get_max_charge(), time)
        else:
            return 0
    
    def charge_location(self, stations):
        current_loc = self.get_location()
        min_dist = np.inf
        for station in stations:
            station_loc = station.location
            dist = np.linalg.norm(current_loc-station_loc)
            if dist < min_dist:
                min_dist = dist
                best_station = station
        return best_station

    # Check if the car is charged to 80%
    def is_car_charged_to_80(self):
        return self.get_car().get_charge() >= 0.8
    
    def charge(self, station, time):
        energy_required = self.car.get_energy_needed()
        if self.charging_method == "naive":
            cost = self.naive_charge(station, time, energy_required)  
        else:
            cost = self.scheduled_charge(station, time, energy_required)
        self.charge_cost[self.charging_method] += cost
        self.energy_charged[self.charging_method] += energy_required
        self.energy_used += energy_required
        self.car.charge_car(energy_required)
        self.busy_until = self.car.get_charging_time(energy_required)

    def naive_charge(self, station, time, energy_needed):
        cost = 0
        charging_time = self.car.get_charging_time(energy_needed)
        self.time_charged["naive"] += charging_time
        for _ in range(int(charging_time)):
            cost += energy_needed * station.get_price(time)
            time += 1
        return cost

    def find_optimal_charging_schedule(self, station, time, energy_needed):
        window_size = 8 * 60
        charging_time = self.cars[0].get_charging_time(energy_needed)
        min_cost = float('inf')
        optimal_schedule = []
    
        # Calculate the minimum charging time in the 7-hour window (50% of the time plugged in)
        min_charging_time = int(charging_time)#int(window_size * 0.5)
    
        # Iterate through all possible starting times within the 7-hour window
        for start_time in range(time, time + window_size - min_charging_time):
            schedule = []
            cost = 0
    
            # Calculate the total cost for charging at this starting time for the minimum charging time
            for t in range(start_time, start_time + min_charging_time):
                cost += station.get_price(t)
                schedule.append(t)
    
            # Update the minimum cost and optimal schedule if a better one is found
            if cost < min_cost:
                min_cost = cost
                optimal_schedule = schedule
    
        # Calculate the actual energy needed for the minimum charging time
        actual_energy_needed = min(energy_needed, min_charging_time * station.get_power())
    
        return min_cost * actual_energy_needed, optimal_schedule

    def scheduled_charge(self, station, time, energy_needed):
        cost, optimal_schedule = self.find_optimal_charging_schedule(station, time, energy_needed)
        if len(optimal_schedule) == 0:
            time_plugged_in = 0
        else: 
            time_plugged_in = optimal_schedule[-1]-time+1 
        self.time_charged["scheduled"] += time_plugged_in 
        return cost



        
## Driver Profile 1 
## A person that just goes to work and back

## UberDriver will choose Naive with probability 100% between 12pm and 12am whereas this 
## probability will drop to 60% between 12am and 11:59 am. 
## Similarly, the commuter will choose schedule pricing between 5pm to 7am with probability 90% 
## and this probability will drop down to 10% between 7 am and 5pm since 
##most likely they will not charge at all.
class Commuter(AgentInterface):
    def __init__(self, id, vehicle, home, work, min_charge, shift_start, shift_end):
        super().__init__() 
        self.driver_id = id
        self.cars = [vehicle]
        self.car = vehicle
        self.home = home
        self.work = work
        self.min_charge = min_charge
        self.location = home
        self.busy = False
        self.busy_until = 0
        self.driving = False  
        self.departure_time_morning = int(shift_start)
        self.departure_time_evening = int(shift_end)
        self.distance_to_work = np.linalg.norm(work - home)
  
    def get_action(self, time):
        if time % (24 * 60) == self.departure_time_morning or time % (24 * 60) == self.departure_time_evening:
                state_of_charge_after_drive = (self.cars[0].get_charge() - self.distance_to_work * self.cars[0].get_avg_cons()) / self.cars[0].get_max_charge()
                if state_of_charge_after_drive > 0.2:
                    return "drive"
                else:
                    if 9 * 60 <= time % (24 * 60) < 5 * 60:
                        self.charging_method = "naive" if np.random.rand() < 0.5 else "scheduled"
                    
                    else:
                        self.charging_method = "naive" if np.random.rand() < 0.5 else "scheduled"
                    return "charge"

    def drive_location(self, time):
        if  time % (24 * 60) < self.departure_time_morning:
            return self.work
        else: 
            return self.home


       
class UberDriver(AgentInterface):
    
    def __init__(self, 
                 driver_id, 
                 car,
                 home,
                 shift_start,
                 shift_end,
                 city_size = 100,
                 min_charge = 0.2,
                 pickup_distance = 50,
                  ):
        
        super().__init__()
        self.driver_id = driver_id
    
        if isinstance(car, list):
            self.cars = car
        else:
            self.cars = [car]

        self.car = car
            
        self.home = home
        self.location = home
        self.driving = False
        self.passenger = False
        self.destination = None
        self.direction = None
        self.busy = False
        self.busy_until = -1
        self.pickup_distance = pickup_distance
        self.city_size = city_size
        ## The minimum state of charge that the driver is comfortable with,
        ## initialized at 20% if none is passed
        self.min_charge = min_charge
        
        self.start_time_morning = shift_start
        self.stop_time_evening = shift_end

    def get_action(self, time):
        if self.start_time_morning <= time % (24 * 60) <= self.stop_time_evening:
            self.pickup = np.random.randint(low=0, high=self.city_size, size=2)
            self.dropoff = np.random.randint(low=0, high=self.city_size, size=2)
            distance = np.linalg.norm(self.pickup-self.location)+np.linalg.norm(self.dropoff-self.pickup)
            state_of_charge_after_drive = (self.cars[0].get_charge() - distance*self.cars[0].get_avg_cons())/self.cars[0].get_max_charge()
            
            if state_of_charge_after_drive >= 0.2:
                self.destination = self.pickup
                return "drive"
            else:
                if 10 * 60 <= time % (24 * 60) < 15 * 60:
                    self.charging_method = "naive"
                elif  15 * 60 < time % (24 * 60) <= 18 * 60:
                    self.charging_method = "scheduled"
                elif 18*60 < time % (24 * 60) <= 2 *60:
                    self.charging_method = "naive" if np.random.rand() < 0.5 else "scheduled"
                else:
                    self.charging_method = "scheduled" if np.random.rand() < 0.5 else "naive"
                return "charge"
        else:
            return None

    def drive_location(self, time):
        if self.start_time_morning <= time % (24 * 60) <= self.stop_time_evening:
            return self.pickup 
        else:
            return self.home
