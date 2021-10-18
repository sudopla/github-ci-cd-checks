"""
Slack Class
"""

import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.exceptions import SlackChannelException, SlackMessageException

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Slack:
    """
    Send message to Slack channels
    """

    def __init__(self, slack_token: str):
        """
        Attributes
        ----------
        slack_token : str
            Token of Slack application used to send messages
        """
        self.slack_client = WebClient(token=slack_token)

    def get_slack_channel_id(self, channel_name: str):
        """
        Get Slack Channel ID

        Parameters
        ----------
        channel_name : str
            Slack channel name

        Returns
        -------
        str
            Slack channel id
        """
        channel_id = None
        try:
            for response in self.slack_client.conversations_list():
                for channel in response["channels"]:
                    if channel["name"] == channel_name:
                        channel_id = channel["id"]
        except SlackApiError as exc:
            logger.error("Error getting Slack channel information: %s", exc)
            raise SlackChannelException from exc
        return channel_id

    def send_slack_message(self, msg: str, channel_id: str):
        """
        Send Message to Slack Channel

        Parameters
        ----------
        msg : str
            Message that will be sent to slack
        channel_id : str
            Slack channel id

        Returns
        -------
        None
        """

        try:
            result = self.slack_client.chat_postMessage(
                channel=channel_id,
                username="GitHub",
                as_user=True,
                text="",
                attachments=[
                    {
                        "mrkdwn_in": ["text"],
                        "color": "#36a64f",
                        "pretext": "Following DevOps CI/CD Best Practices",
                        "text": msg,
                        "fallback": "fallback",
                    }
                ],
            )
            logger.info(result)
        except SlackApiError as exc:
            logger.error("Error posting message: %s", exc)
            raise SlackMessageException from exc
