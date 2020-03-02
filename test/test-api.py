import json
from random import randint

from flask import Flask

app = Flask(__name__)

build_plan_branches_path = "test/sample_responses/build_plan_branches.json"
build_plan_path = "test/sample_responses/build_plan.json"
build_result_path = "test/sample_responses/build_result.json"
deploy_plan_path = "test/sample_responses/deploy_plan.json"
deploy_result_path = "test/sample_responses/deploy_result.json"

rel_times = ["3 minutes ago", "2 hours ago", "1 day ago"]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/rest/api/latest/plan/<branch_id>/branch.json')
def enabled_branches(branch_id):
    obj = read_json_file_to_object(build_plan_branches_path)
    obj['link']['href'] = "https://bamboo-master.server.traveljigsaw.com/rest/api/latest/plan/{}/branch".format(
        branch_id)
    return obj


@app.route('/rest/api/latest/plan/<branch_id>.json')
def build_plan(branch_id):
    obj = read_json_file_to_object(build_plan_path)
    obj['key'] = branch_id
    obj['planKey']['key'] = branch_id
    obj['link']['href'] = "https://bamboo-master.server.traveljigsaw.com/rest/api/latest/plan/{}".format(branch_id)
    return obj


@app.route('/rest/api/latest/result/<branch_id>/latest.json')
def build_result(branch_id):
    obj = read_json_file_to_object(build_result_path)
    obj['plan']['planKey']['key'] = branch_id
    obj['plan']['key'] = branch_id
    obj['buildRelativeTime'] = rel_times[randint(0, 2)]
    return obj


@app.route('/rest/api/latest/deploy/project/<env_id>')
def deploy_plan(env_id):
    obj = read_json_file_to_object(deploy_plan_path)
    obj['id'] = env_id
    obj['key']['key'] = env_id
    return obj


@app.route('/rest/api/latest/deploy/environment/<env_id>/results')
def deploy_result(env_id):
    obj = read_json_file_to_object(deploy_result_path)
    print(obj['results'][0])
    obj['results'][0]['deploymentState'] = "SUCCESS" if randint(0, 1) == 0 else "FAILURE"
    obj['results'][0]['lifeCycleState'] = "FINISHED" if randint(0, 1) == 0 else "RUNNING"
    return obj


def read_json_file_to_object(file):
    with open(file, 'r') as f:
        return json.load(f)
