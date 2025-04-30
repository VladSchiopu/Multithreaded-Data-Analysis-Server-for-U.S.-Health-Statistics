
## Objectives

This project implements a **multi-threaded Python server** using Flask to expose statistical APIs based on a public dataset about physical activity, nutrition, and obesity in the United States.

- Synchronization mechanisms and multithreading in Python
- Flask framework and API development
- Data processing using `pandas`
- Logging and job queue management
- Graceful shutdown and concurrent processing patterns

## Dataset

The dataset is provided by the **U.S. Department of Health & Human Services** and includes yearly health and nutrition statistics per U.S. state. Each row contains:

- A state
- A question (e.g., _"Percent of adults aged 18 years and older who have obesity"_)
- A `Data_Value` (percentage)
- Optional stratification information (age, gender, education, etc.)

## Implementation Overview

The server follows a **job-based request model**:

1. Clients send a request (e.g., to compute state averages).
2. A unique `job_id` is assigned, and the job is added to a **job queue**.
3. A **Thread Pool** processes the job and saves the result to `results/job_id_x.json`.
4. Clients can check status or retrieve results via `/api/get_results/<job_id>`.

## Project Structure

```
app/
├── data_ingestor.py         # Loads and filters the CSV data; processing logic
├── task_runner.py           # Manages thread pool and job queue
├── routes.py                # Defines all Flask routes
├── logging.py               # Rotating log handler for access logs
unittests/
├── TestWebserver.py         # Unit tests for core functionality
results/                     # Output directory for job results
nutrition_activity_obesity_usa_subset.csv  # Dataset file
checker/
├── checker.py               # Functionality checker
pylintrc                     # Code style configuration
```

## Available API Endpoints

### Statistical Requests

| Endpoint                         | Description |
|----------------------------------|-------------|
| `/api/states_mean`              | Mean per state (sorted), given a question |
| `/api/state_mean`               | Mean for a single state |
| `/api/best5` / `/api/worst5`   | Top/bottom 5 states based on mean value |
| `/api/global_mean`              | Overall average across all states |
| `/api/diff_from_mean`           | State differences from global mean |
| `/api/state_diff_from_mean`     | One state's difference from global mean |
| `/api/mean_by_category`         | Mean values per category (e.g., gender) |
| `/api/state_mean_by_category`   | Mean by category for a specific state |

### Job Management

| Endpoint                          | Description |
|-----------------------------------|-------------|
| `/api/get_results/<job_id>`      | Check status or retrieve result |
| `/api/jobs`                      | List all jobs and their status |
| `/api/num_jobs`                  | Number of remaining jobs in queue |
| `/api/graceful_shutdown`         | Initiate graceful shutdown (stop accepting new jobs) |

## Testing & Running

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Running the Server

In the first terminal:

```bash
source venv/bin/activate
make run_server
```

In the second terminal (to run tests):

```bash
source venv/bin/activate
make run_tests
```

## Logging

All route accesses and major events are logged to `webserver.log` with **UTC timestamps** and **rotating file size management**.

Logs include:

- Route calls and request parameters
- Job creation and completion
- Error tracking and exceptions
