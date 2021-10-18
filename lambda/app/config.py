"""
Configuration Options
"""

from typing import Dict, List
from typing_extensions import TypedDict


GITHUB_ORGANIZATION = "<Github_Organization_Name>"


# Slack channels and repos associated with them
class SlackRepoConfig(TypedDict, total=False):
    """
    Configuration options for Slack channel and Github Repos mapping

    Keys
    ----
    cloud_apps : List[str]
        List of Github repo names for application that are deployed to the cloud
    libraries : List[str]
        List of Github repo names for libraries
    """

    cloud_apps: List[str]
    libraries: List[str]


SLACK_CHANNEL_REPOS_MAPPING: Dict[str, SlackRepoConfig] = {
    "team_channel_1": {
        "cloud_apps": ["app1", "app2", "app3"],
        "libraries": ["lib1", "libr2"],
    },
    "team_channel_2": {
        "cloud_apps": ["app4", "app5"],
    },
}


# Secret Names in AWS Secrets Manager
GITHUB_ACCESS_TOKEN_SECRET_NAME = "<Github_Token_Secret_Name>"
SLACK_APP_TOKEN_SECRET_NAME = "<Slack_Token_Secret_Name>"
