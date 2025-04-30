"""This module implements a thread pool to manage background tasks and job execution"""
import os
import json
import threading
from queue import Queue
from typing import Callable
from threading import Thread


class ThreadPool:
    """Thread pool for managing task_runner threads"""
    def __init__(self):

        # Getting the number of threads on the system
        self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS', os.cpu_count() or 1))

        # Queue for pending jobs
        self.job_queue = Queue()

        # Event to signal graceful shutdown
        self.shutdown_event = threading.Event()

        # Variable to track if shutdown is in progress
        self.is_shutting_down = False

        # Dictionary to track job status
        self.job_status = {}

        # Lock for synchronised update of the job statu
        self.job_status_lock = threading.Lock()

    def start(self):
        """Start the workers"""
        for _ in range(self.num_threads):
            worker = TaskRunner(self.job_queue, self.shutdown_event,
            self.job_status, self.job_status_lock)
            worker.start()

    def submit_job(self, job_id: str, task: Callable, *args, **kwargs):
        """Add the job to the queue"""
        if self.is_shutting_down:
            return {
                "status": "error",
                "reason": "shutting down"
            }

        with self.job_status_lock:
            self.job_status[job_id] = "running"

        # Mark the job as running before putting it in the queue
        self.job_queue.put((job_id, task, args, kwargs))
        return {"job_id": job_id}


    def graceful_shutdown(self):
        """Initiate graceful shutdown of thread pool"""
        self.is_shutting_down = True

        # Signal all workers to stop
        self.shutdown_event.set()

        self.job_queue.join()

        return {
            "status": "done" if self.job_queue.empty() else "running"
        }

    def get_job_status(self):
        """Get status of all jobs"""
        with self.job_status_lock:
            return {
                "status": "done",
                "data": [
                    {job_id: status} for job_id, status in self.job_status.items()
                ]
            }

    def get_job_result(self, job_id: str):
        """Retrieve results for a specific job or the specific error"""
        with self.job_status_lock:
            if job_id not in self.job_status:
                return {
                    "status": "error", 
                    "reason": "Invalid job_id"
                }

            status = self.job_status[job_id]

            if status == "running":
                return {"status": "running"}

            if status == "done":
                try:
                    with open(f'results/{job_id}', 'r', encoding='utf-8') as f:
                        result = json.load(f)
                    return {
                        "status": "done",
                        "data": result
                    }
                except FileNotFoundError:
                    return {
                        "status": "error", 
                        "reason": "Result file not found"
                    }


    def num_pending_jobs(self):
        """Get number of pending jobs"""
        return self.job_queue.qsize()

class TaskRunner(Thread):
    """A worker thread that fetches and executes jobs from the queue."""
    def __init__(self, job_queue: Queue, shutdown_event: threading.Event,
        job_status: dict, job_status_lock: threading.Lock):
        super().__init__()
        self.job_queue = job_queue
        self.shutdown_event = shutdown_event
        self.job_status = job_status
        self.job_status_lock = job_status_lock

    def run(self):
        while not self.shutdown_event.is_set():
            try:
                # Get a job from the queue with a timeout to allow graceful shutdown
                job_id, task, args, kwargs = self.job_queue.get(timeout=1)

                try:
                    result = task(*args, **kwargs)

                    # Create the results directory if it doesnt exist
                    os.makedirs('results', exist_ok=True)

                    # Put the output in the corresponding file
                    with open(f'results/{job_id}', 'w', encoding='utf-8') as f:
                        json.dump(result, f)

                    with self.job_status_lock:
                        self.job_status[job_id] = "done"

                except Exception:
                    with self.job_status_lock:
                        self.job_status[job_id] = "error"

                # Notify queue that job is finished
                self.job_queue.task_done()

            except Exception:
                continue
