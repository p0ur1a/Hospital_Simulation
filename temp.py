import simpy
import numpy as np
from config import *
from visualization import plot_average_waiting_times
from messages import (arrival_message, arrived_at_desk_message,
                      failure_message, exit_hospital_message, success_message,
                      run_number_message, waiting_line_capacity_failure_message)

np.random.seed(10)

"""
STOP_TRIGGERS: Reasons for stopping the simulation.
"""
STOP_TRIGGERS = {
    'patient_waiting_time_failure': 1,
    'waiting_queue_failure': 2,
    'success': 3
}


class SimulationState:
    """
    Encapsulates the state variables of the simulation.
    """
    def __init__(self):
        self.number_of_desks = 1
        self.waiting_queue = []
        self.waiting_times = []
        self.average_waiting_times = []
        self.simulations_stop_causes = []
        self.success = False
        self.patient_number = 1
        self.env = simpy.Environment()
        self.stop_simulation = self.env.event()

    def reset(self):
        """
        Resets the simulation variables for a new run.
        """
        self.waiting_queue.clear()
        self.waiting_times.clear()
        self.env = simpy.Environment()
        self.stop_simulation = self.env.event()
        self.patient_number = 1


class Hospital:
    """
    Represents the hospital environment, including service desks and patient handling.
    """
    def __init__(self, env, num_desks):
        self.env = env
        self.num_desks = num_desks
        self.desks = simpy.PriorityResource(env, num_desks)

    def service(self, service_time):
        """
        Simulates the time taken to service a patient.
        """
        yield self.env.timeout(service_time)

    def add_desk(self, env):
        """
        Dynamically adds a new service desk.
        """
        self.num_desks += 1
        self.desks = simpy.PriorityResource(env, self.num_desks)


class Patient:
    """
    Represents a patient in the hospital simulation.
    """
    def __init__(self, name, priority, allowed_waiting_time, service_time):
        self.name = name
        self.priority = priority
        self.allowed_waiting_time = allowed_waiting_time
        self.service_time = service_time
        self.hospital_arrival_time = None
        self.desk_arrival_time = None
        self.exit_time = None
        self.waiting_time = None

    @staticmethod
    def create_patient(state):
        """
        Factory method to create a patient with randomized attributes.
        """
        name = state.patient_number
        state.patient_number += 1
        priority = np.random.randint(PRIORITY_LOWER_BOUND, PRIORITY_UPPER_BOUND + 1)
        allowed_waiting_time = (
            priority if priority <= EMERGENCY_THRESHOLD else NON_EMERGENCY_ALLOWED_WAITING_TIME
        )
        service_time = max(1, round(np.random.exponential(scale=SERVICE_TIME_LAMBDA_PARAM)))
        return Patient(name, priority, allowed_waiting_time, service_time)

    def hospital_arrival(self, env, waiting_queue, stop_simulation):
        """
        Handles the arrival of the patient at the hospital.
        """
        waiting_queue.append(self.name)
        check_simulation_conditions(
            waiting_queue=waiting_queue,
            queue_maximum_capacity=WAITING_LINE_CAPACITY,
            stop_simulation=stop_simulation,
        )
        self.hospital_arrival_time = env.now
        print(arrival_message(self.__dict__))

    def desk_arrival(self, env, waiting_queue, waiting_times, stop_simulation):
        """
        Handles the arrival of the patient at a service desk.
        """
        self.desk_arrival_time = env.now
        print(arrived_at_desk_message(self.__dict__))
        self.waiting_time = self.desk_arrival_time - self.hospital_arrival_time
        waiting_times.append(self.waiting_time)
        check_simulation_conditions(
            patient=self.__dict__,
            stop_simulation=stop_simulation,
        )
        waiting_queue.remove(self.name)

    def hospital_exit(self, env):
        """
        Handles the patient's exit from the hospital.
        """
        self.exit_time = env.now
        print(exit_hospital_message(self.__dict__))


def check_simulation_conditions(patient=None, waiting_queue=None, queue_maximum_capacity=None, env=None, stop_simulation=None):
    """
    Checks various failure or success conditions in the simulation.
    """
    if patient and patient['allowed_waiting_time'] < patient['waiting_time']:
        print(failure_message(patient))
        stop_simulation.succeed()  # Correctly trigger the SimPy event
        state.simulations_stop_causes.append(STOP_TRIGGERS['patient_waiting_time_failure'])
        return

    if waiting_queue is not None and len(waiting_queue) > queue_maximum_capacity:
        print(waiting_line_capacity_failure_message())
        stop_simulation.succeed()  # Correctly trigger the SimPy event
        state.simulations_stop_causes.append(STOP_TRIGGERS['waiting_queue_failure'])
        return

    if env and env.now > SIMULATION_TIME:
        stop_simulation.succeed()  # Correctly trigger the SimPy event
        # state.success = True
        state.simulations_stop_causes.append(STOP_TRIGGERS['success'])


def patient_process(env, hospital, state):
    """
    Simulates the lifecycle of a patient in the hospital.
    """
    patient = Patient.create_patient(state)
    patient.hospital_arrival(env, state.waiting_queue, state.stop_simulation)

    with hospital.desks.request(priority=patient.priority) as request:
        yield request
        patient.desk_arrival(env, state.waiting_queue, state.waiting_times, state.stop_simulation)
        yield env.process(hospital.service(patient.service_time))
        patient.hospital_exit(env)


def setup(env, hospital, state):
    """
    Sets up the hospital simulation.
    """
    while True:
        env.process(patient_process(env, hospital, state))
        interarrival_rate = max(1, round(np.random.exponential(scale=INTERARRIVAL_RATE_LAMBDA_PARAM)))
        check_simulation_conditions(env=env, stop_simulation=state.stop_simulation)
        yield env.timeout(interarrival_rate)


def main():
    """
    Main function to run the hospital simulation.
    """
    state = SimulationState()
    hospital = Hospital(state.env, state.number_of_desks)

    while not state.success:
        state.reset()
        state.env.process(setup(state.env, hospital, state))
        state.env.run(until=state.stop_simulation)

        if len(state.waiting_times) > 0:
            avg_wait = round(sum(state.waiting_times) / len(state.waiting_times), 2)
            state.average_waiting_times.append(avg_wait)
        else:
            state.average_waiting_times.append(0)

        hospital.add_desk(state.env)

    print(success_message(hospital.num_desks - 1))
    plot_average_waiting_times(state.average_waiting_times, state.simulations_stop_causes)


if __name__ == "__main__":
    main()
