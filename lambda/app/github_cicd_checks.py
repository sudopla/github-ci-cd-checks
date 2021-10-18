"""
Github Class
"""

from typing import Union
from datetime import datetime, timedelta
import re
import logging
from github import Github, GithubException
from app.exceptions import GithubBranchesException, GithubPRsException

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GithubCiCdChecks:
    """
    Class to check some of the DevOps CI/CD pratices in Github repos

    It assumes that application release to production are triggered
    when a release branch is created in the repo with the following
    naming convention - release-x.y.z
    """

    def __init__(self, organization_name: str, github_token: str):
        """
        Attributes
        ----------
        organization_name : str
            Name of Github organization
        github_token : str
            Github token
        """

        github = Github(github_token)
        self.github_org = github.get_organization(organization_name)

    def check_cd(self, repo_name: str, cd_frequency_hours: int = 4) -> Union[str, bool]:
        """
        Check if code is deployed to production frequently
        It assumes a release branch is created when code is deployed to production
        DevOps - Continous Deployment

        Parameters
        ----------
        github_organizations : str
            Github organization name
        repo_name : str
            Repository name
        cd_frequency_hours : int
            Time frame for releases

        Returns
        -------
        Union[str, bool]
            Message or False no need for a release

        """

        git_repo = self.github_org.get_repo(repo_name)

        # get release branches for repo
        release_branches = []
        try:
            for branch in git_repo.get_branches():
                branch_name = branch.name
                match = re.match(r"^release-([0-9]+).([0-9]+).([0-9]+)", branch_name)
                if match:
                    major_n, minor_n, patch_n = match.groups()
                    release_branches.append(
                        {
                            "name": branch_name,
                            "major_n": int(major_n),
                            "minor_n": int(minor_n),
                            "patch_n": int(patch_n),
                        }
                    )
        except GithubException as exc:
            logger.error("Failed to get Github branches - %s", exc)
            raise GithubBranchesException from exc

        # get latest release branch
        release_branches.sort(
            key=lambda x: (x["major_n"], x["minor_n"], x["patch_n"]), reverse=True
        )
        latest_release_branch_name = release_branches[0]["name"]

        # get date for latest release branch
        latest_release_branch = git_repo.get_branch(latest_release_branch_name)  # type: ignore
        latest_release_date = latest_release_branch.commit.commit.author.date

        # Get commits to default branch (main) after release branch was created
        # and less than continous delivery frequency hours
        until_date = datetime.utcnow() - timedelta(hours=cd_frequency_hours)
        commits = git_repo.get_commits(since=latest_release_date, until=until_date)

        num_commits_after_release = commits.totalCount - 1
        if num_commits_after_release == 1:
            msg = (
                f"*{repo_name }* has one commit that needs to be deployed to production. "
                f"Latest release was on _{latest_release_date.strftime('%m-%d-%Y, %H:%M')}UTC_"
            )
            logger.info(msg)
            return msg
        if num_commits_after_release > 1:
            msg = (
                f"*{repo_name }* has {num_commits_after_release} commits that need to be deployed to production. "
                f"Latest release was on _{latest_release_date.strftime('%m-%d-%Y, %H:%M')}UTC_"
            )
            logger.info(msg)
            return msg

        msg = f"No need to create a release for {repo_name}"
        logger.info(msg)
        return False

    def check_open_prs(
        self, repo_name: str, ci_frequency_hours: int = 4
    ) -> Union[str, bool]:
        """
        Check if pull requests are merged fast
        DevOps - Continous Integration

        Parameters
        ----------
        github_organizations : str
            Github organization name
        repo_name : str
            Repository name
        ci_frequency_hours : int
            Time frame to merge PRs

        Returns
        -------
        Union[str, bool]
            Message or False if there are not PRs to be merged
        """

        git_repo = self.github_org.get_repo(repo_name)

        # Look for PRs that have been opened for > continous_integration_frequency
        num_open_prs = 0
        try:
            for pull_request in git_repo.get_pulls(state="open"):
                diff = datetime.utcnow() - pull_request.created_at
                if diff.days >= 1 or diff.seconds > ci_frequency_hours * 3600:
                    num_open_prs += 1
        except GithubException as exc:
            logger.error("Failed to list pull requests - %s", exc)
            raise GithubPRsException from exc

        if num_open_prs == 1:
            msg = f"*{repo_name}* has one pull request that needs to be merged"
            logger.info(msg)
            return msg
        if num_open_prs > 1:
            msg = f"*{repo_name}* has {num_open_prs} pull requests that need to be merged into main"
            logger.info(msg)
            return msg

        msg = f"{repo_name } does not have any open PRs that need to be merged"
        logger.info(msg)
        return False
