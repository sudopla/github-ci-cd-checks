"""
Check repos specified in config file and send slack messages to groups when CI/CD actions are required
"""

import logging

from app.config import (
    SLACK_CHANNEL_REPOS_MAPPING,
    GITHUB_ORGANIZATION,
    GITHUB_ACCESS_TOKEN_SECRET_NAME,
    SLACK_APP_TOKEN_SECRET_NAME,
)
from app.github_cicd_checks import GithubCiCdChecks
from app.slack import Slack
from app.utils import get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Get Github and Slack token values from Secrets Manager
try:
    github_token = get_secret(GITHUB_ACCESS_TOKEN_SECRET_NAME)
    slack_token = get_secret(SLACK_APP_TOKEN_SECRET_NAME)
except Exception as exc:
    # pylint: disable=invalid-name
    msg = (
        "Failed to retrieve Github or Slack tokens"
        + "Traceback - "
        + getattr(exc, "message", str(exc))
    )
    logger.error(msg)
    raise RuntimeError(msg) from exc


def handler(event, context):
    # pylint: disable=unused-argument
    """
    Lambda handler

    Parameters
    ----------
    event (dict): The AWS event payload
    context (dict): The AWS context object

    Return
    ------
    None
    """

    github_checks = GithubCiCdChecks(GITHUB_ORGANIZATION, github_token)
    slack = Slack(slack_token)

    for slack_channel, repos in SLACK_CHANNEL_REPOS_MAPPING.items():
        channel_id = slack.get_slack_channel_id(slack_channel)
        slack_message = []

        # loop cloud application repos
        for repo in repos.get("cloud_apps", []):
            # check if a release is needed
            message = github_checks.check_cd(repo)
            if message:
                slack_message.append(message)

            # check if there are PRs that need to be merged
            message = github_checks.check_open_prs(repo)
            if message:
                slack_message.append(message)

        # loop library repos
        for repo in repos.get("libraries", []):
            # check if there are PRs that need to be merged
            message = github_checks.check_open_prs(repo)
            if message:
                slack_message.append(message)

        # send message to slack channel
        if slack_message:
            slack_message = "\n".join(slack_message)
            logger.info("Send message to Slack channel - %s", slack_channel)
            slack.send_slack_message(slack_message, channel_id)
        else:
            logger.info(f"{slack_channel} is good")
