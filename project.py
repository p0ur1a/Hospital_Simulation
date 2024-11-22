"""
This file contains the simulation and its methods and variables. The functionality of methods and
variables have been explained on top of them. 
"""

import simpy
import numpy as np
from config import *
from visualization import plot_average_waiting_times
from messages import (arrival_message, arrived_at_desk_message,
                      failure_message, exit_hospital_message, success_message,
                      run_number_message, waiting_line_capacity_failure_message)



np.random.seed(10)


"""
STOP_TRIGGERS: There are essentially three reasons why a simulation is terminated:

    1. patient_waiting_time_failure: This means a patient has waited more than we are allowed 
    to keep them waiting. When this happens, it means we need at least one more service desk in
    our hospital.
    
    2. waiting_queue_failure: It means we have more people in line than we could handle. The
    simulation is then terminated to add another desk to process the patients faster so that
    they don't stack up.
    
    3. success: we have reached SIMULATION_TIME without having the discussed failures
"""

STOP_TRIGGERS = {
    'patient_waiting_time_failure' : 1,
    'waiting_queue_failure' : 2,
    'success' : 3
}


"""
These are the variables of this simulation and will be expanded

number_of_desks: A hospital needs at least one desk to operate. so the initial value of this 
variable is 1. Every time we have a failure, we add one more desk and start the simulation again.

waiting_queue: It's the hospital's waiting queue. We store the patients that have arrived and are yet 
to be serviced in this list. only the names are stored in this list. once the patient gets to a desk,
they will be removed from this list.

waiting_times: The waiting times of patients are stored in this list. This list is used to get the 
average waiting time of each run, which is one of the main goals of this project.

average_waiting_times: The average waiting time of each run is calculated using the waiting_times
and is stored in this list.

simulations_stop_causes: It is important to know why we cannot operate with X number of service desks.
So we store the causes of failure in this list to use it for visualization and analyzing the results.

env: a simPy environment object that handles the simulation events, processes, resources, etc. It's 
practically our hospital in this project

success: It's a trigger that once equals to true, we know that the whole simulation must be stopped and
the problem of finding the optimum amount of service desks is solved
"""

number_of_desks = 1
waiting_queue = []
waiting_times = []
average_waiting_times = []
simulations_stop_causes = []
env = simpy.Environment()
success = False


"""
Hospital is our environment and everything happens in it. Its main function is to service the 
patients. It's done by service desks which are our resources. Resources are the things that are 
shared between the users (patients in this case) and are limited. Since this project focuses on
priority-based servicing, we have used a special type of resource (PriorityResource) that does 
the job for us.
"""

class Hospital:
    def __init__(self, env, num_desks):
        self.env = env
        self.desks = simpy.PriorityResource(env, num_desks)

    def service(self, service_time):
        yield self.env.timeout(service_time)


"""
There are three reasons for stopping the simulation. Three methods have been written to check whether
we have encountered any of them:

    1. check_patient_waiting_time_failure(patient): 
    allowed waiting time of the patient is assigned to them once they arrive in the hospital, and is 
    based on their priority. Their actual waiting time is calculated once they get to a service desk. 
    If a patient is kept waiting more than we are allowed to, it means we have failed and we need at  
    least one more desk; hence, the simulation is stopped.
    
    2. check_hospital_waiting_queue_failure(waiting_queue, queue_maximum_capacity):
    In some cases, the capacity of a hospital waiting line is limited. So every time a patient arrives,
    we should check to see if we have reached the capacity. If so, it means the number of hospital's 
    service desks was not sufficient to visit the patients.
    
   3. check_success(env):
   If we have reached the end of our simulation time unit and have not had any failures, the current number
   of desks are enough and we practically have solved the problem. 
"""
    
def check_simulation_conditions(patient=None, waiting_queue=None, queue_maximum_capacity=None, env=None):
    """
    Checks various failure or success conditions in the simulation.

    Parameters:
    - patient (dict): Dictionary with 'allowed_waiting_time' and 'waiting_time' keys.
    - waiting_queue (list): List representing the hospital's waiting queue.
    - queue_maximum_capacity (int): Maximum capacity of the waiting queue.
    - env (SimPy Environment): Simulation environment to check the current time.
    """
    global success

    if patient and patient['allowed_waiting_time'] < patient['waiting_time']:
        print(failure_message(patient))
        stop_simulation.succeed()
        simulations_stop_causes.append(STOP_TRIGGERS['patient_waiting_time_failure'])
        return

    if waiting_queue is not None and len(waiting_queue) > queue_maximum_capacity:
        print(waiting_line_capacity_failure_message())
        stop_simulation.succeed()
        simulations_stop_causes.append(STOP_TRIGGERS['waiting_queue_failure'])
        return

    if env and env.now > SIMULATION_TIME:
        stop_simulation.succeed()
        success = True
        simulations_stop_causes.append(STOP_TRIGGERS['success'])


        
        
"""
The arrival of patients in a simulation means creating them and assigning them the necessary  values. The 
initial values of a patient are as follows:

    1. patient_name: For better comprehension, we have assigned a number to each patient as their name. This
    could prove useful in debugging and checking the flow of the simulation to see which state each patient 
    is in.
    
    2. priority: Priority of a patient is a number between 1 (highest priority) and 10 (lowest priority). Since
    this project focuses on priority-based service queues, this value is the basis of future functionalities of 
    the simulation. You can imagine a patient who is having a stroke as a priority 1 patient, and someone who 
    is at the hospital for their annual check-up as a priority 10 patient.
   
    3. allowed_waiting_time: determines how long a patient can be kept waiting. If the priority of a patient
    is high (between 1 and 5) its value is equal to the patient's priority. If it's not, we are allowed to keep
    them waiting for the NON_EMERGENCY_ALLOWED_WAITING_TIME time unit. 
    
    4. service_time: Each patient requires a certain amount of time for their treatment. This number is calculated
    based on an exponential distribution with a lambda parameter of SERVICE_TIME_LAMBDA_PARAM. Because in real
    scenarios we cannot have a 0 service time, the value of this variable should be greater or equal to 1. 
    
"""
    
def create_patient():
    
    global patient_number
    patient_name = patient_number
    patient_number += 1
    
    priority = np.random.randint(PRIORITY_LOWER_BOUND, PRIORITY_UPPER_BOUND + 1)
    allowed_waiting_time = priority if priority <= EMERGENCY_THRESHOLD else NON_EMERGENCY_ALLOWED_WAITING_TIME
    service_time = max(1, round(np.random.exponential(scale=SERVICE_TIME_LAMBDA_PARAM)))
    
    
    patient = {'name': patient_name,
               'priority': priority,
               'allowed_waiting_time': allowed_waiting_time,
               'service_time': service_time}
    
    return patient


"""
There are three stages of a patient overall state in the hospital. Once they arrive in the hospital and are waiting to
be serviced, once they get to a desk and are visited, and once they leave the hospital. each state has a separate
method which is as follows:

    1. patient_hospital_arrival(env):
    The patient is created and is assigned the initial values that we have discussed. Their name then enters the 
    waiting queue. We have to immediately check for the waiting queue failure after that to see whether we have 
    exceeded the hospital waiting line capacity. Finally, a new attribute is assigned to the patient (hospital_arrival_time) 
    
    2. patient_desk_arrival(env, patient):
    The patient is going to be visited at this point; hence, we can assign two new attributes to them. desk_arrival_time
    which is self-explanatory. Then we can calculate the most important attribute of the patient which is their waiting 
    time. It is equal to the time difference between when they entered the hospital and the time that they were examined
    by a doctor. This important value is stored in the waiting_times list to be analyzed later. Now that we have the 
    patient's waiting time, we can check whether they have been kept waiting longer than we are allowed to. If we don't
    have a failure, we continue with the simulation and remove the patient from the waiting queue.
    
    3. patient_hospital_exit(env, patient): 
    Patient has been visited and leaves the hospital. A new attribute (exit_time) is used to store the patient's exit
    time from the hospital
"""

def patient_hospital_arrival(env):
    patient = create_patient()
    waiting_queue.append(patient['name'])
    check_simulation_conditions(waiting_queue=waiting_queue, queue_maximum_capacity=WAITING_LINE_CAPACITY)
    patient['hospital_arrival_time'] = env.now
    print(arrival_message(patient))
    return patient

def patient_desk_arrival(env, patient):
    patient['desk_arrival_time'] = env.now
    print(arrived_at_desk_message(patient))
    patient['waiting_time'] = patient['desk_arrival_time'] - patient['hospital_arrival_time']
    waiting_times.append(patient['waiting_time'])
    check_simulation_conditions(patient=patient)
    waiting_queue.remove(patient['name'])

    
def patient_hospital_exit(env, patient):
    
    patient['exit_time'] = env.now
    print(exit_hospital_message(patient))
    

"""
The three explained states of a patient in the hospital are implemented in this method. Hospital as the environment
of the whole simulation is an argument of this method, and it is here that we model the patient in the hospital.
First, the patient arrives and requests a service desk from the hospital. It is done by sending a special type of 
simPy request which is based on priority. The patient now has to wait until the system dedicates a resource (desk) 
to them. After they get to a service desk, we let the system pass the simulation time by the patient's service
time. Finally, the patient leaves the hospital.
"""

def patient_process(env, hospital):
    
    patient = patient_hospital_arrival(env)
    
    with hospital.desks.request(priority=patient['priority']) as request:
        
        yield request
        
        patient_desk_arrival(env, patient)
        
        yield env.process(hospital.service(patient['service_time']))
        
        patient_hospital_exit(env, patient)


"""
An object of hospital class is created with the desired number of desks. The patient_process method is constantly
executed until the simulation is successful. There must be a time between the arrival of patients; this time is 
calculated using the exponential distribution with the lambda parameter of INTERARRIVAL_RATE_LAMBDA_PARAM. 
"""
    
def setup(env, num_desks):
    hospital = Hospital(env, num_desks)
    while True:
        env.process(patient_process(env, hospital))
        interarrival_rate = max(1, round(np.random.exponential(scale=INTERARRIVAL_RATE_LAMBDA_PARAM)))
        check_simulation_conditions(env=env)
        yield env.timeout(interarrival_rate)  
        
    
"""
Each run starts with resetting the variables and emptying the necessary lists. a simPy event (stop_simulation) is created
which can be triggered by other methods throughout the simulation. After each run is over, the average waiting time of
the patients is stored and a new desk is added. This will continue until we have a successful run. Finally, the average
waiting times of the simulation are plotted. 
"""    
    
    
def reset_simulation_variables(waiting_queue, waiting_times):
    
    global patient_number, env
    
    patient_number = 1
    waiting_times.clear()
    waiting_queue.clear()
    env = simpy.Environment()
    
    print(run_number_message(number_of_desks))


while success == False:
        
    reset_simulation_variables(waiting_queue, waiting_times)
    stop_simulation = env.event()
    env.process(setup(env, num_desks=number_of_desks))
    env.run(until=stop_simulation)

    average_waiting_times.append(round(sum(waiting_times)/len(waiting_times), 2))
    
    number_of_desks += 1
 
print(success_message(number_of_desks - 1))

plot_average_waiting_times(average_waiting_times, simulations_stop_causes)