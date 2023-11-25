"""
This file includes the messages that will appear on the terminal during the simulation. To enhance understanding,
the messages have different colors and fonts when the simulation begins and ends (is terminated).
"""

def arrival_message(patient):
    
    message = (f"Patient {patient['name']} arrives at {patient['hospital_arrival_time']}, priority: {patient['priority']}, "
        f"service time: {patient['service_time']}, "
        f"allowed waiting time: {patient['allowed_waiting_time']}")
    
    return message

def arrived_at_desk_message(patient):
    
    message = (f"Patient {patient['name']} gets to the desk at {patient['desk_arrival_time']}")
    return message

def failure_message(patient):
    
    message = (f"\033[1m\033[31mSIMULATION FAILED!!! Patient {patient['name']} waiting time exceeded its limit\033[0m")
    return message


def waiting_line_capacity_failure_message():

    message = (f"\033[1m\033[95mSIMULATION FAILED!!! Hospital waiting queue has reached its maximum capacity \033[0m")

    return message

def exit_hospital_message(patient):
    
    message = (f"Patient {patient['name']} exited at {patient['exit_time']}, "
          f"waiting time: {patient['waiting_time']}")
    return message

    
def success_message(number_of_desks):
    
    message = (f"\033[1;32mrequired number of desks: {number_of_desks}\033[0m")
    return message

def run_number_message(run_number):
    
    message = (f'\033[1;34mThis is run #{run_number}\033[0m')
    return message