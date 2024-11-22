"""
These are the constants of the simulation which will be discussed

PRIORITY_LOWER_BOUND, PRIORITY_UPPER_BOUND: These two variables are the lower and the upper
bound of priority. priority of each patient is assigned to them once they arrive in the
hospital and is a random number between these two variables (1 and 10)

EMERGENCY_THRESHOLD: Indicates whether the patient is in an emergency situation or not. If a
patient's priority is less or equal to this value, it is considered an emergency patient.

NON_EMERGENCY_ALLOWED_WAITING_TIME: The waiting time of every non-emergency patient is equal
to this value

WAITING_LINE_CAPACITY: The maximum capacity of the hospital's waiting queue. We can have 
situations where we don't set a limit on it (float('inf')). But it's normally it's equal
to 10.

SIMULATION_TIME: Indicated the length of the simulation. once we reach this time unit, the
simulation is terminated automatically. It's important to note that this variable is a time
unit and can be interpreted as we like. We have considered it as minute in this simulation.
But it can also be second, hour, day, etc. 

INTERARRIVAL_RATE_LAMBDA_PARAM, SERVICE_TIME_LAMBDA_PARAM: The service time and interarrival
time of patients are each assigned to them using an exponential distribution. This statistical 
distribution requires a lambda parameter which is assigned to it using these variables.
"""

PRIORITY_LOWER_BOUND = 1
PRIORITY_UPPER_BOUND = 10
EMERGENCY_THRESHOLD = 5
NON_EMERGENCY_ALLOWED_WAITING_TIME = 60
WAITING_LINE_CAPACITY = 10
SIMULATION_TIME = 2000
INTERARRIVAL_RATE_LAMBDA_PARAM = 0.76
SERVICE_TIME_LAMBDA_PARAM = 15
