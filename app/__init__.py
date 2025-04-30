"""This module initializes the Flask web server, sets up the thread pool for job execution,
and loads the data ingestor for handling statistical computations."""
import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.logging import logger

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)
webserver.task_runner = ThreadPool()

webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

from app import routes
