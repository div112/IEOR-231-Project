from Agents import *
from Vehicles import *
from Stations import *
import numpy as np
from chargingCosts import ChargingCosts

#np.random.seed(0)

POPULATION = 1000
NUM_OFFICES = 200
NUM_STATIONS = 30
CITY_SIZE = 100
VEHICLES = ["ModelS", "Mustang", "Ioniq", "Kia"]
VEHICLEp = [.4, .1, .25, .25]
agents = []

for i in range(POPULATION):
    if np.random.random() < .1:
        #Uber driver agent
        id = i
        car = Vehicle(np.random.choice(VEHICLES, p = VEHICLEp))
        home = np.random.normal(50, 30, 2) % CITY_SIZE
        min_charge = np.random.normal(.2, .005)
        agents.append(UberDriver(id, car, home, min_charge))
    else:
        #commuter agent
        id = i
        car = Vehicle(np.random.choice(VEHICLES, p = VEHICLEp))
        home = np.random.normal(50, 30, 2) % CITY_SIZE
        work = np.random.normal(50, 12, 2) % CITY_SIZE
        min_charge = np.random.normal(.2, .005)
        agents.append(Commuter(id, car, home, work, min_charge))

stations = []

prices = ChargingCosts()

for i in range(NUM_STATIONS):
    id = i
    num_chargers = np.random.randint(5, 30)
    location = np.random.uniform(0, CITY_SIZE, 2)
    price = prices.simulate(1)[0]
    stations.append(ChargingStation(station_id = i, 
                                    num_chargers = num_chargers, 
                                    location = location, 
                                    price = price))

print("Starting simulation")

for time in range(24 * 60):
    for agent in agents:
        agent.update_location()
        agent.update_busy()
        agent.log(time)
        if agent.is_busy(time):
            continue
        agent_action = agent.get_action(time)
        if agent_action == "drive":
            destination = agent.drive_location(time)
            agent.drive(destination, time)
        if agent_action == "charge":
            station = agent.charge_location(stations)
            agent.drive(station.location, time)
            station.enqueue_agent(agent, time)

            # Check if the station is available
            station_available = station.get_num_available(time) > 0
            if station_available:
                station.enqueue_agent(agent, time)
                agent.charge(station, time)
            else:
                # Find the next closest station if the current station is not available
                closest_station = None
                min_distance = float("inf")
                for s in stations:
                    if s ==  station:
                        continue
                    if s.get_num_available(time) > 0:
                        dist = np.linalg.norm(agent.get_location() - s.get_location())
                        if dist < min_distance:
                            min_distance = dist
                            closest_station = s

                if closest_station is not None:
                    agent.drive(closest_station.get_location(), time)
                    closest_station.enqueue_agent(agent, time)
                    agent.charge(station, time)
    # Update charging agents at each station
    for station in stations:
        station.update_charging_agents(time)
        station.log(time)

print("Finished simulation")

total_naive_cost = 0
total_scheduled_cost = 0
total_distance = 0
total_energy = 0
for agent in agents:
    logs = agent.get_logs()
    last_log = logs[-1]
    total_naive_cost += last_log["naive_cost"]
    total_scheduled_cost += last_log["scheduled_cost"]
    total_distance += last_log["distance_driven"]
    total_energy += last_log["energy_used"]

print("Total naive cost:", total_naive_cost)
print("Total scheduled cost:", total_scheduled_cost)
print("Cost differential:", total_naive_cost - total_scheduled_cost)
print()
print("Total distance driven:", total_distance)
print("Total energy used:", total_energy)


import matplotlib.pyplot as plt

def plot_charging_methods(agents):
    naive_count = 0
    scheduled_count = 0

    for agent in agents:
        for log in agent.get_logs():
            if log["charging_method"] == "naive":
                naive_count += 1
            elif log["charging_method"] == "scheduled":
                scheduled_count += 1

    labels = ["Naive", "Scheduled"]
    sizes = [naive_count, scheduled_count]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    plt.title("Charging Methods Distribution")
    plt.show()


def plot_prices_and_costs(stations, agents):
    hours = list(range(24))
    avg_prices = [sum([station.get_price(i * 60) for station in stations]) / len(stations) for i in hours]

    naive_costs = [0] * 24
    scheduled_costs = [0] * 24
    naive_counts = [0] * 24
    scheduled_counts = [0] * 24

    for agent in agents:
        for log in agent.get_logs():
            hour = log["time"] // 60
            if log["charging_method"] == "naive":
                naive_costs[hour] += log["naive_cost"]
                naive_counts[hour] += 1
            elif log["charging_method"] == "scheduled":
                scheduled_costs[hour] += log["scheduled_cost"]
                scheduled_counts[hour] += 1

    naive_avg_costs = [naive_costs[i] / naive_counts[i] if naive_counts[i] > 0 else 0 for i in hours]
    scheduled_avg_costs = [scheduled_costs[i] / scheduled_counts[i] if scheduled_counts[i] > 0 else 0 for i in hours]

    fig, ax = plt.subplots()
    ax.plot(hours, avg_prices, label="Average Price", color="black")
    ax.plot(hours, naive_avg_costs, label="Naive Avg. Cost", linestyle="--", color="blue")
    ax.plot(hours, scheduled_avg_costs, label="Scheduled Avg. Cost", linestyle="--", color="red")
    ax.legend()
    plt.title("Pricing and Costs")
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("Price/Cost")
    plt.show()

def plot_distance_driven(agents):
    hours = list(range(24))
    distances = np.zeros(24)
    for agent in agents:
        for log in agent.get_logs():
            hour = log["time"] // 60
            distances[hour] += log["distance_driven"]
    plt.plot(hours, distances)
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("Total Miles Driven by the Population")
    plt.title("Distances Traveled by All Agents Over Time")
    plt.show()

def plot_energy_used(agents):
    hours = list(range(24))
    distances = np.zeros(24)
    for agent in agents:
        for log in agent.get_logs():
            hour = log["time"] // 60
            distances[hour] += log["energy_used"]
    plt.plot(hours, distances)
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("Total Energy Used by the Population")
    plt.title("Energy Used by All Agents Over Time")
    plt.show()

plot_energy_used(agents)
plot_distance_driven(agents)
plot_charging_methods(agents)
plot_prices_and_costs(stations, agents)

