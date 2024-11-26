# Hospital Simulation Visualization

Abstract. This paper uses discrete event simulation theory and stochastic service system to analyze the queuing problems in hospital outpatient services. It applies the event scheduling simulation strategy to create a system that assigns random pain scores (from 1 to 10) to patients and classifies those with scores below 5 as needing urgent service. The system aims to optimize the number of service desks and the waiting times based on the patients’ pain scores. This paper tackles the challenge of balancing the number of servers and the urgency of patients.

## Features

- **Simulation**:
  - Models patient arrivals, priority-based service, and queue dynamics using `simpy`.
  - Dynamically adjusts the number of service desks based on failures (e.g., excessive waiting times or queue capacity breaches).
  - Real-time simulation updates streamed to the frontend.

- **Visualization**:
  - Interactive scatterplot created with D3.js.
  - Points represent simulation runs, color-coded for failure or success:
    - **Red**: Waiting time failure.
    - **Orange**: Queue capacity failure.
    - **Green**: Successful run.
  - Hover over points to see the run information.

- **Backend**:
  - Flask-based API streams simulation results as **Server-Sent Events (SSE)**.
  - Fully modular structure for simulation logic, visualization, and configuration.

---

## Prerequisites

### Install Dependencies
1. **Python 3.8+** is required.
2. Install required Python packages:
   ```bash
   pip install flask simpy numpy matplotlib
   ```
3. Install `D3.js` by including it in your `index.html`:
   ```html
   <script src="https://d3js.org/d3.v7.min.js"></script>
   ```

---


## How to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/p0ur1a/Hospital_Simulation
   cd Hospital_Simulation
   ```

2. **Set Up Environment**:
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Flask Server**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Simulation Workflow

1. The backend simulates patient flow, calculating:
   - Average waiting times.
   - Causes of system failures (waiting time or queue capacity breaches).
2. Results are streamed to the frontend after each run using **SSE**.
3. The frontend visualizes the results dynamically with D3.js:
   - A scatterplot updates incrementally as runs are completed.
   - Hovering over points reveals details like run number and average waiting time.

---

## Interactive Visualization

- **Hover Tooltip**: Displays run number and average waiting time for each point.
- **Color Codes**:
  - **Red**: Waiting time failure.
  - **Orange**: Queue capacity failure.
  - **Green**: Success.
- **Dynamic Updates**: Points appear incrementally as the simulation progresses.

---

## Configuration

Adjust simulation parameters in `config.py`:
- **Simulation Time**: `SIMULATION_TIME`
- **Service Time Distribution**: `SERVICE_TIME_LAMBDA_PARAM`
- **Priority Levels**: `PRIORITY_LOWER_BOUND`, `PRIORITY_UPPER_BOUND`
- **Queue Capacity**: `WAITING_LINE_CAPACITY`
- **Interarrival Rate**: `INTERARRIVAL_RATE_LAMBDA_PARAM`

---

## Dependencies

### Python Packages:
- **Flask**: Backend web framework.
- **SimPy**: Process-based discrete-event simulation library.
- **Numpy**: For numerical calculations.
- **Matplotlib**: For optional visualizations.

### JavaScript Library:
- **D3.js**: Interactive data visualizations.

---

## Author

**Pouria Bahri**  
Email: Bapouria@gmail.com 
GitHub: (https://github.com/p0ur1a)

---

## License

This project is licensed under the [MIT License](LICENSE).

---
