#!/usr/bin/env python

import argparse
import collections
import ConfigParser
import json
import math
import requests

from pyvotecore.irv import IRV
from pyvotecore.stv import STV


def request(api_key, access_token, url, data):
    """Return the response from a JSON request over OAuth."""
    client = requests.session()
    client.headers = {
        "Authorization": "bearer {}".format(access_token),
        "Content-Type": "application/json"
    }
    client.params = {"api_key": api_key}
    response = client.post(url, data=json.dumps(data))
    return response


def get_url(hostname, endpoint):
    """Returns a URL by joining a hostname and an endpoint."""
    return "{}{}".format(hostname, endpoint)


def get_json(response):
    """Returns the JSON from a response object."""
    try:
        return response.json()
    except:
        print "SurveyMonkey returned no JSON. Please wait and try again."
        exit()


def print_data(data, ballots, verbose=False):
    """Prints out results for a runoff."""
    winner = data['winner']
    print "Elected candidate: {}".format(winner)
    if verbose:
        print "Second choice support:"
        for candidate in data['candidates']:
            if candidate == winner:
                continue
            candidate_count = 0
            winner_count = 0
            for ballot in ballots:
                ranking = ballot['ballot']
                if ranking[0] == candidate:
                    candidate_count += 1
                    if ranking[1] == winner:
                        winner_count += 1
            print "{}: {}/{}".format(candidate, winner_count, candidate_count)


# Parse arguments

parser = argparse.ArgumentParser(
    description='Tallies votes from a SurveyMonkey survey.')
parser.add_argument(
    "--verbose", "-v", help="turns on verbose mode", action="store_true")
args = parser.parse_args()

# Load SurveyMonkey configuration values

config = ConfigParser.ConfigParser()
config.read('config.ini')

access_token = config.get('SurveyMonkey API', 'access_token').replace("\n", "")
api_key = config.get('SurveyMonkey API', 'api_key')
survey_id = config.get('SurveyMonkey API', 'survey_id')
respondents_per_request = int(
    config.get('SurveyMonkey API', 'respondents_per_request'))
hostname = config.get('SurveyMonkey API', 'hostname')

# Acquire list of respondents

respondent_url = get_url(hostname, "/v2/surveys/get_respondent_list")
respondent_data = {"survey_id": survey_id}
respondent_response = request(
    api_key, access_token, respondent_url, respondent_data)
respondent_json = get_json(respondent_response)['data']['respondents']
all_respondent_ids = [respondent['respondent_id']
                      for respondent in respondent_json]

# Get details for the survey

detail_url = get_url(hostname, "/v2/surveys/get_survey_details")
detail_data = {"survey_id": survey_id}
detail_response = request(api_key, access_token, detail_url, detail_data)
detail_json = get_json(detail_response)['data']['pages'][
    0]['questions'][0]['answers']
answer_texts = {answer['answer_id']: answer['text'] for answer in detail_json}

# Find votes for each respondent

ballot_url = get_url(hostname, "/v2/surveys/get_responses")
num_calls = int(
    math.ceil(len(all_respondent_ids) / float(respondents_per_request)))
ballots_counter = collections.Counter()

for call in range(num_calls):
    start = respondents_per_request * call
    end = min(start + respondents_per_request, len(all_respondent_ids))
    respondent_ids = all_respondent_ids[start:end]
    ballot_data = {
        "survey_id": survey_id,
        "respondent_ids": respondent_ids
    }
    ballot_response = request(api_key, access_token, ballot_url, ballot_data)
    responses_by_id = get_json(ballot_response)['data']
    answers_by_id = [responses_by_id[respondent_id]['questions'][0][
        'answers'] for respondent_id in range(len(responses_by_id))]
    answers = [tuple(answer_texts[vote['row']] for vote in answer)
               for answer in answers_by_id]
    ballots_counter.update(answers)

# Convert ballots and tally with py-vote-core

keys = ("ballot", "count")
ballots = []
for vote in ballots_counter.most_common():
    ballot, count = vote
    value = {"count": count, "ballot": list(ballot)}
    ballots.append(value)

voting_methods = {
    'IRV': IRV,
    'STV': STV
}
algorithm = voting_methods[config.get('Voting System', 'algorithm')]
print_data(algorithm(ballots).as_dict(), ballots, verbose=args.verbose)
