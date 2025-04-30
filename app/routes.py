"""This module defines the API routes for job management"""
from flask import request, jsonify
from app import webserver
from app.logging import logger

def make_job(task, *args, **kwargs):
    """Helper function to make a job with incremented job ID"""
    # Create a job id based on the current number of jobs
    job_id = f"job_id_{webserver.job_counter}"
    # Update number of jobs
    webserver.job_counter += 1
    # Send job to task_runner
    return webserver.task_runner.submit_job(job_id, task, *args, **kwargs)

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """API endpoint to compute the mean values for all states for a given question."""
    logger.info("Entering states_mean_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.states_mean, data['question'])
    logger.info("Exiting states_mean_request")
    return result

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """API endpoint to compute the mean value for a specific state and question."""
    logger.info("Entering state_mean_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.state_mean, data['question'], data['state'])
    logger.info("Exiting state_mean_request")
    return result

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """API endpoint to retrieve the top 5 states with the best values for a given question."""
    logger.info("Entering best5_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.best5, data['question'])
    logger.info("Exiting best5_request")
    return result

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """API endpoint to retrieve the bottom 5 states with the worst values for a given question."""
    logger.info("Entering worst5_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.worst5, data['question'])
    logger.info("Exiting worst5_request")
    return result

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """API endpoint to compute the global mean for a given question."""
    logger.info("Entering global_mean_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.global_mean, data['question'])
    logger.info("Exiting global_mean_request")
    return result

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """API endpoint to compute the difference from the global mean for all states."""
    logger.info("Entering diff_from_mean_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.diff_from_mean, data['question'])
    logger.info("Exiting diff_from_mean_request")
    return result

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """API endpoint to compute the difference from the global mean for a specific state."""
    logger.info("Entering state_diff_from_mean_request with parameters: %s", request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.state_diff_from_mean, data['question'], data['state'])
    logger.info("Exiting state_diff_from_mean_request")
    return result

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """API endpoint to compute the mean value for each category across all states."""
    logger.info("Entering mean_by_category_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.mean_by_category, data['question'])
    logger.info("Exiting mean_by_category_request")
    return result

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """API endpoint to compute the mean value for each category within a specific state."""
    logger.info("Entering state_mean_by_category_request with parameters: %s",request.json)
    data = request.json
    result = make_job(webserver.data_ingestor.state_mean_by_category, data['question'],
    data['state'])
    logger.info("Exiting state_mean_by_category_request")
    return result

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """API endpoint to retrieve the result of a specific job."""
    logger.info("Entering get_response with job_id: %s",job_id)
    result = jsonify(webserver.task_runner.get_job_result(job_id))
    logger.info("Exiting get_response")
    return result

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """API endpoint to gracefully shut down the server."""
    logger.info("Entering graceful_shutdown")
    result = jsonify(webserver.task_runner.graceful_shutdown())
    logger.info("Exiting graceful_shutdown")
    return result

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """API endpoint to retrieve the status of all running and pending jobs."""
    logger.info("Entering get_jobs")
    result = jsonify(webserver.task_runner.get_job_status())
    logger.info("Exiting get_jobs")
    return result

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """API endpoint to retrieve the number of pending jobs."""
    logger.info("Entering num_jobs")
    result = jsonify(webserver.task_runner.num_pending_jobs())
    logger.info("Exiting num_jobs")
    return result
