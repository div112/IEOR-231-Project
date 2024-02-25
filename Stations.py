import numpy as np

class StationInterface:

    def __init__(self):
        self.logs = []

    def log(self, time):
        self.logs.append(self.get_queue_length())

    def get_logs(self):
        return self.logs

    # return station id
    def get_id(self):
        pass

    # return station name (maybe not necessary)
    def get_name(self):
        pass

    # return station location (latitude, longitude)
    def get_location(self):
        pass

    # return price to charge at time time
    def get_price(self, time):
        pass

    # return total number of chargers at this location
    def get_num_chargers(self):
        pass

    # return how many chargers are free to use
    def get_num_available(self, time):
        pass

    # return a list of all users currently charging
    def get_current_users(self, time):
        pass

    # return station power supply
    def get_power(self):
        pass

    # Add agent to the queue
    def enqueue_agent(self, agent, time):
        self.queue.append((agent, time))

    # Dequeue agent from the queue
    def dequeue_agent(self, agent):
        for i, (queued_agent, _) in enumerate(self.queue):
            if queued_agent.get_id() == agent.get_id():
                self.queue.pop(i)
                break

    # Get the number of agents in the queue
    def get_queue_length(self):
        return len(self.queue)

    # Get the waiting time for a particular agent
    def get_agent_waiting_time(self, agent):
        waiting_time = 0
        num_chargers = self.get_num_chargers()
        queue_copy = self.queue.copy()

        while queue_copy:
            current_agent, arrival_time = queue_copy.pop(0)
            if current_agent.get_id() == agent.get_id():
                break
            waiting_time += 1
            num_chargers -= 1
            if num_chargers == 0:
                num_chargers = self.get_num_chargers()

        return waiting_time

    # Update the charging status of agents
    def update_charging_agents(self, time):
        charging_agents = self.get_current_users(time)
        for agent in charging_agents:
            if agent.is_car_charged_to_80():
                self.dequeue_agent(agent)

class ChargingStation(StationInterface):
    def __init__(self, station_id, num_chargers, price, location=None):
        self.logs = []
        self.station_id = station_id
        self.num_chargers = num_chargers
        self.charging_agents = []
        self.queue = []
        self.charging_power = 50  # kW, assuming a fast-charging station
        self.price = price

        self.location = location

    def get_location(self):
        return self.location

    def get_price(self, time):
        return self.price[int(time/60)]

    def get_num_chargers(self):
        return self.num_chargers

    def get_num_available(self, time):
        return self.num_chargers - len(self.get_current_users(time))

    def get_current_users(self, time):
        return [agent for agent, start_time in self.charging_agents if start_time <= time]

    def enqueue_agent(self, agent, time):
        if self.get_num_available(time) > 0:
            self.charging_agents.append((agent, time))
            self.num_chargers -= 1
        else:
            self.queue.append((agent, time))

    def dequeue_agent(self, agent):
        for i, (queued_agent, _) in enumerate(self.queue):
            if queued_agent.get_id() == agent.get_id():
                self.queue.pop(i)
                break

    def get_queue_length(self):
        return len(self.queue)

    def get_agent_waiting_time(self, agent):
        waiting_time = 0
        num_chargers = self.get_num_chargers()
        queue_copy = self.queue.copy()

        while queue_copy:
            current_agent, arrival_time = queue_copy.pop(0)
            if current_agent.get_id() == agent.get_id():
                break
            waiting_time += 1
            num_chargers -= 1
            if num_chargers == 0:
                num_chargers = self.get_num_chargers()

        return waiting_time

    def update_charging_agents(self, time):
        new_charging_agents = []
        for agent, start_time in self.charging_agents:
            charging_duration = (time - start_time) * self.charging_power
            if agent.get_car().get_charge() + charging_duration >= agent.get_car().get_max_charge() * 0.8:
                self.num_chargers += 1
            else:
                new_charging_agents.append((agent, start_time))
        self.charging_agents = new_charging_agents

    # return station power supply
    def get_power(self):
        return self.charging_power
