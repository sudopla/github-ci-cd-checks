"""
Application Exceptions
"""


class AwsSecretException(Exception):
    """
    Failed to retrieve AWS secret

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message="Failed to retrieve secret"):
        self.message = message
        super().__init__(self.message)


class SlackChannelException(Exception):
    """
    Failed to retrieve Slack channel information

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message="Failed to retrieve Slack channel information"):
        self.message = message
        super().__init__(self.message)


class SlackMessageException(Exception):
    """
    Failed to send message to Slack channel

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message="Failed to send message to Slack channel"):
        self.message = message
        super().__init__(self.message)


class GithubBranchesException(Exception):
    """
    Failed to get Github branches

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message="Failed to get Github branches"):
        self.message = message
        super().__init__(self.message)


class GithubPRsException(Exception):
    """
    Failed to list Github pull requests

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message="Failed to list Github pull requests"):
        self.message = message
        super().__init__(self.message)
