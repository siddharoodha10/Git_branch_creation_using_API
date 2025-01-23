import json
import requests
from datetime import datetime

class GitHub:
    def __init__(self,gith_user, git_token, repo_name, release_branch_name="main"):
        self.auth = (gith_user,git_token)
        self.repo_name = repo_name
        self.release_branch_name = release_branch_name
        self.sha = None
        self.headers = {'accept': 'application/vnd.github.v3+json'}
        self.get_branch_sha()

    def get_branch_sha(self):
        url = "https://api.github.com/repos/{0}/branches/{1}".format(self.repo_name, self.release_branch_name)
        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code != 200:
            raise Exception("There is an issue to get the {0} branch sha: {1}".format(self.release_branch_name,response.text))
        self.sha = response.json()['commit']['sha']

    def create_new_branch(self):
        now = str(datetime.now()).replace(" ", "").replace("-","").replace(":","").replace('.',"")
        new_branch_name = "hotfix-{0}-{1}".format(now,self.release_branch_name)
        url ="https://api.github.com/repos/{0}/git/refs".format(self.repo_name)
        data = {
            "ref": "refs/heads/{0}".format(new_branch_name),
            "sha": self.sha
        }
        data = json.dumps(data)
        response = requests.post(url, auth=self.auth, headers=self.headers,data=data)
        if response.status_code != 201:
            raise Exception("There is an issue with the branch creation: {0}".format(response.text))
        print("The hotfix branch= {0} created succefully on top of the release branch= {1}".format(new_branch_name, self.release_branch_name))
        return new_branch_name


#Executation starts from here
g = GitHub()
g.create_new_branch()
