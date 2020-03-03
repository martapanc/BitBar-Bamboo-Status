# Bamboo Status plugin for BitBar

[BitBar](https://github.com/matryer/bitbar) plugin to display Bamboo build and deployment status of a given environment


## Requisites
- [Python 3](https://docs.python-guide.org/starting/install3/osx/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://www.codingforentrepreneurs.com/blog/install-django-on-mac-or-linux)
## Installation
* Install the BitBar app following instructions [here](https://github.com/matryer/bitbar).  
* Clone this repository. The local directory should be set as BitBar's plugin folder (`BitBar icon > Preferences > Change Plugin Folder`):
```bash
git clone https://github.com/martapanc/BitBar-Bamboo-Status
cd bitbar-bamboo-status
```
* Copy the `config.yaml.local` file to `config.yaml`.
```bash
cp bamboo_status_plugin/config/config.yaml.local bamboo_status_plugin/config/config.yaml
```
`config.yaml` can now be used to store your own credentials and access details. 
Make sure your tokens and credentials are always stored locally and never pushed to the remote repository.

```yaml
bamboo:
  credentials:
    username: your_username
    password: your_password
  config:
    url: https://bamboo-example.server.com
    plans: ['PLAN-A', 'PLAN-B']
    deployment_project_id: 12345678
```

* Run the script in a terminal session: this will setup the Python virtual environment for the first time and will install all needed dependencies.
```bash
./bamboo-build-status.30s.sh
```
* Once the command above has finished, click on the BitBar icon and hit `CMD + R` to refresh the plugins. Now the toolbar should be up and running!

### Configuration
- [Bamboo API](docs/Bamboo_API_info.md)

### Fake Bamboo API for local tests
If the servers are unreachable for some reason, a local Flask server can be used to replace the live Bamboo one.
Open a new terminal session and use the following commands:
```
source bamboo_status_plugin/venv/bin/activate
export FLASK_APP=test/test-api.py
flask run
```
Now, changing the url to `http://127.0.0.1:5000` in `config/config.yaml`, the Bamboo plugin will show fake data for testing purposes.