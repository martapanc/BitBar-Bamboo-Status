#!/usr/bin/env python3

from config import authentication
from config import config
import requests
from datetime import datetime

DATETIME_FORMAT = '%d %b %Y %H:%M'

USERNAME = authentication.credentials['jira_credentials']['username']
PASSWORD = authentication.credentials['jira_credentials']['password']
SERVER = config.config['bamboo']['url']
PLANS = config.config['bamboo']['plans']
DEPLOYMENT_PROJECT_ID = config.config['bamboo']['deployment_project_id']


def get_json_response(url):
    return requests.get(url, auth=(USERNAME, PASSWORD)).json()


def icons(state):
    switcher = {
        'Building': '🔄',
        'Deploying': '🔄',
        'Successful': '✅',
        'SUCCESS': '✅',
        'Failed': '‼️',
        'FAILURE': '‼️',
        'Never_deployed': '🤷'
    }
    return switcher.get(state, '✖️')


def get_build_status(plan):
    result = []
    enabled_branches_url = '{}/rest/api/latest/plan/{}/branch.json?enabledOnly'.format(SERVER, plan)
    enabled_branches_response = get_json_response(enabled_branches_url)

    branch_keys = [plan]  # master branch has same id as plan
    for branch in enabled_branches_response['branches']['branch']:
        branch_keys.append(branch['key'])

    for branch_key in branch_keys:
        plan_url = '{}/rest/api/latest/plan/{}.json?os_authType=basic'.format(SERVER, branch_key)
        result_url = '{}/rest/api/latest/result/{}/latest.json?os_authType=basic'.format(SERVER, branch_key)
        plan_response = get_json_response(plan_url)
        result_response = get_json_response(result_url)

        result.append(get_json_build_from_response(branch_key, plan, plan_response, result_response))
    return result


def get_json_build_from_response(branch_key, plan, plan_response, result_response):
    if "planName" in result_response:
        branch_name = '[{}] master'.format(plan_response['projectKey']) if branch_key == plan else result_response['planName']
        return {
            'branch_key': branch_key,
            'display_url': 'href={}/browse/{}/latest'.format(SERVER, branch_key),
            'name': branch_name,
            'build_state': 'Building' if plan_response['isBuilding'] else result_response['state'],
            'build_summary': result_response['buildTestSummary'],
            'relative_time': result_response['buildRelativeTime']
        }
    else:
        return {
            'branch_key': '[{}] master'.format(plan_response['shortKey']),
            'build_state': 'never_built'
        }


def print_build_status(status):
    for branch in status:
        if branch['build_state'] == "never_built":
            print('Branch with id {} was never built'.format(branch['branch_key']))
        else:
            print('{:>3} {:<20}{:>20} | {} font=Menlo'
                  .format(icons(branch['build_state']), branch['name'], branch['relative_time'], branch['display_url']))
            if branch['build_state'] == 'Failed':
                print('\t- {} | color=red trim=false'.format(branch['build_summary']))
    print('---')


def get_plans():
    for plan in PLANS:
        print_build_status(get_build_status(plan))


def get_deployment_status(env):
    deployment_result_url = '{}/rest/api/latest/deploy/environment/{}/results'.format(SERVER, env['id'])
    return get_deploy_json_from_response(env, get_json_response(deployment_result_url))


def get_deploy_json_from_response(env, response):
    json_result = {'display_url': 'href={}/deploy/viewEnvironment.action?id={}'.format(SERVER, env['id']),
                   'name': env['name']}
    if len(response['results']) > 0:
        result = response['results'][0]

        if result['lifeCycleState'] == 'FINISHED':
            completed_time = datetime.fromtimestamp(result['finishedDate'] / 1000).strftime(DATETIME_FORMAT)
            json_result['time'] = completed_time
            json_result['state'] = result['deploymentState']
            json_result['version'] = result['deploymentVersionName']
        else:
            started_time = datetime.fromtimestamp(result['startedDate'] / 1000).strftime(DATETIME_FORMAT)
            json_result['time'] = started_time
            json_result['state'] = 'Deploying'

        json_result['creator'] = result['deploymentVersion']['creatorDisplayName']
    else:
        json_result['state'] = 'Never_deployed'
    return json_result


def print_deployment_status(branch):
    if branch['state'] == "Never_deployed":
        print('{}️ {} - never deployed | {} font=Menlo'.format(icons(branch['state']), branch['name'],
                                                               branch['display_url']))
    elif branch['state'] == 'Deploying':
        print('{} {} - started on {} | {} font=Menlo'.format(icons(branch['state']), branch['name'],
                                                             branch['time'], branch['display_url']))
    else:
        print('{:>3} {:<27} {:>12}| {} font=Menlo'
              .format(icons(branch['state']), branch['name'], branch['version'], branch['display_url']))
        print('-- Run by {}'.format(branch['creator']))
        print('-- Completed on {}'.format(branch['time']))


def get_deployment_environments():
    deployment_url = '{}/rest/api/latest/deploy/project/{}'.format(SERVER, DEPLOYMENT_PROJECT_ID)
    deployment_response = get_json_response(deployment_url)

    for env in deployment_response['environments']:
        print_deployment_status(get_deployment_status(env))


print('Bamboo')
print('---')
get_plans()
print('---')
get_deployment_environments()
