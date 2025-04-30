"""This module handles data processing for statistical analysis from a CSV file."""
import pandas as pd

class DataIngestor:
    """Class to process and analyze health data from a CSV file."""
    def __init__(self, csv_path: str):
        # Read csv from csv_path
        self.data = pd.read_csv(csv_path)
        # These lists help determine how to interpret "best" and "worst" for different questions
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]
        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity'
            ' aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic'
            ' activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity'
            ' aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic'
            ' physical activity and engage in muscle-strengthening activities on 2 or more '
            'days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity'
            ' aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic'
            ' activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more'
            ' days a week',
        ]

    def states_mean(self, question):
        """Calculate mean for each state for a given question"""
        # Filter the data to get the rows matching the question
        filtered_data = self.data[self.data['Question'] == question]
        # Group them by state name, calculate the mean of the data values and sort the results by mean
        return filtered_data.groupby('LocationDesc')['Data_Value'].mean().sort_values().to_dict()

    def state_mean(self, question, state):
        """Calculate mean for a specific state for a given question"""
        filtered_data = self.data[
            (self.data['Question'] == question) &
            (self.data['LocationDesc'] == state)
        ]

        state_mean_value = filtered_data['Data_Value'].mean()
        return {state: state_mean_value}

    def best5(self, question):
        """Get top 5 states based on the question"""
        means = self.states_mean(question)
        # Return 5 states with the lowest or highest means based on the question type
        if question in self.questions_best_is_min:
            return dict(sorted(means.items(), key=lambda x: x[1])[:5])
        return dict(sorted(means.items(), key=lambda x: x[1], reverse=True)[:5])

    def worst5(self, question):
        """Get bottom 5 states based on the question"""
        means = self.states_mean(question)

        if question in self.questions_best_is_min:
            return dict(sorted(means.items(), key=lambda x: x[1], reverse=True)[:5])
        return dict(sorted(means.items(), key=lambda x: x[1])[:5])

    def global_mean(self, question):
        """Calculate global mean for a given question"""
        filtered_data = self.data[self.data['Question'] == question]
        global_mean_value = filtered_data['Data_Value'].mean()

        return {'global_mean': global_mean_value}

    def diff_from_mean(self, question):
        """Calculate difference from global mean for each state"""
        global_mean_val = self.global_mean(question)['global_mean']
        means = self.states_mean(question)

        return {state: global_mean_val - mean for state, mean in means.items()}

    def state_diff_from_mean(self, question, state):
        """Calculate difference from global mean for a specific state"""
        global_mean_val = float(self.global_mean(question)['global_mean'])
        state_mean_val = float(self.state_mean(question, state)[state])

        return {state: global_mean_val - state_mean_val}

    def mean_by_category(self, question):
        """Calculate mean for each segment in each state"""
        filtered_data = self.data[self.data['Question'] == question]
        grouped = filtered_data.groupby(['LocationDesc', 'StratificationCategory1',
        'Stratification1'])['Data_Value'].mean()
        result = {}

        # Build a nested dictionary to match the required format
        for (state, category, stratification), value in grouped.items():
            result[f"('{state}', '{category}', '{stratification}')"] = value

        return result

    def state_mean_by_category(self, question, state):
        """Calculate mean for each segment in a specific state"""
        filtered_data = self.data[(self.data['Question'] == question) &
        (self.data['LocationDesc'] == state)]
        grouped = filtered_data.groupby(['StratificationCategory1',
        'Stratification1'])['Data_Value'].mean()
        result = {state: {}}

        for (category, stratification), value in grouped.items():
            result[state][f"('{category}', '{stratification}')"] = value

        return result
