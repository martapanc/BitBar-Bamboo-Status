# Bamboo API

Useful links:
- [Using the API](https://developer.atlassian.com/server/bamboo/using-the-bamboo-rest-apis/)
- [REST resources](https://developer.atlassian.com/server/bamboo/bamboo-rest-resources/)

## Build plans - Naming
**Dashboard**
- Each team usually have their own Bamboo dashboard, which has a unique id, and often contains multiple **plans**. 
- For example, [Supplier Booking Service](https://bamboo-master.server.traveljigsaw.com/browse/SBS)'s dashboard is identified as "SBS" and includes 6 plans.

**Plans**
- Plans' ids are formed as [dashboard_id]-[plan_id]
- Examples: SBS-SBS, SBS-PT, NDL-WEBNDL, BCAPI-WEB...

**Branches**
- Plans may include several branches, whose ids are formed as [dashboard_id]-[plan_id][branch_id]
- The id of the Master branch is usually the same as the plan id, e.g. SBS-SBS
- Examples include: SBS-SBS4, SBS-SBS337, NDL-WEBNDL466

**Runs**
- Finally, every branch can be built multiple times, and every run is identified as follows: [dashboard_id]-[plan_id][branch_id]-[run_id]
- For example: SBS-SBS-353, SBS-SBS337-1, NDL-WEBNDL465-1
- To access the latest run, the path is [branch]/latest

## Deployment plans - Naming
**Project**
- Similarly to the dashboards, Deployment Projects list the available deployment plans of a team
- The project id is usually numeric and can be found at the end of the project url. For example, [SBS's deployment](https://bamboo-master.server.traveljigsaw.com/deploy/viewDeploymentProjectEnvironments.action?id=97648645) id is "97648645"

**Environments**
- These are similar to the build plans, however their unique id is again a numeric string, such as "108298249" for [SBS's stage ](https://bamboo-master.server.traveljigsaw.com/deploy/viewEnvironment.action?id=108298249) environment

## Requests
The following function connects to the API and returns a json response. Username and password are set in config/config.py and are the general Jira/Bamboo credentials.
```python
def get_json_response(url):
    return requests.get(url, auth=(USERNAME, PASSWORD)).json()
```

The request urls are constructed as follows:
```
<server>/rest/api/latest/[request-specific parameters]
```
For example:
```
https://bamboo-master.server.traveljigsaw.com/rest/api/latest/plan/SBS-SBS.json
```

## Useful endpoints
**Build**
- `/plan/{plan}/branch.json?enabledOnly` : list enabled branches
- `/plan/{branch}.json` : get branch info
- `/result/{branch}/latest.json` : get the result info of the latest run of the selected branch

**Deploy**
- `/deploy/project/{project_id}` : list the available environments of a deployment project, and their info
- `/deploy/environment/{env_id}/results` : display info about the deployment result of a given environment

See the attached [Postman collection](Bamboo_API.postman_collection.json) for more details and examples about requests and responses (add your own username and password to the auth configuration).