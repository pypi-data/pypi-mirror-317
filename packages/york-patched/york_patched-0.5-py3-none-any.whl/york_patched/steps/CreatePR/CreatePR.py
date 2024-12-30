from pathlib import Path

import git
from git.exc import GitCommandError

from york_patched.common.client.scm import (
    GithubClient,
    GitlabClient,
    GerritClient,
    ScmPlatformClientProtocol,
    get_slug_from_remote_url,
)
from york_patched.logger import logger
from york_patched.step import Step, StepStatus
from git import Repo, GitCommandError


class CreatePR(Step):
    required_keys = {"target_branch"}

    def __init__(self, inputs: dict):
        super().__init__(inputs)
        if not all(key in inputs.keys() for key in self.required_keys):
            raise ValueError(f'Missing required data: "{self.required_keys}"')

        self.original_remote_name = "origin"
        logger.info('call create PR')
        self.enabled = not bool(inputs.get("disable_pr", False))
        if self.enabled:
            logger.info('hello world!')
            self.scm_client = None
            if "github_api_key" in inputs.keys():
                self.scm_client = GithubClient(inputs["github_api_key"])
            elif "gitlab_api_key" in inputs.keys():
                self.scm_client = GitlabClient(inputs["gitlab_api_key"])
            elif "gerrit_http_password" in inputs.keys():
                self.scm_client = GerritClient(inputs["gerrit_username"],inputs["gerrit_http_password"])
            
            else:
                logger.warning(
                    f'Missing required input data: "github_api_key" or "gitlab_api_key",'
                    f" PR creation will be disabled."
                )
                self.enabled = False

        if self.enabled:
            if "scm_url" in inputs.keys():
                self.scm_client.set_url(inputs["scm_url"])

            if not self.scm_client.test():
                logger.warning(
                    f"{self.scm_client.__class__.__name__} token test failed. " f"PR creation will be disabled."
                )
                self.enabled = False

        self.pr_body = inputs.get("pr_body", "")
        self.title = inputs.get("pr_title", "Patchwork PR")
        self.force = bool(inputs.get("force_pr_creation", False))
        self.base_branch = inputs.get("base_branch")
        if self.enabled and self.base_branch is None:
            logger.warn("Base branch not provided. Skipping PR creation.")
            self.enabled = False
        self.target_branch = inputs["target_branch"]
        if self.enabled and self.base_branch == self.target_branch:
            logger.warn("Base branch and target branch are the same. Skipping PR creation.")
            self.enabled = False

    def __push(self, repo):
        push_args = ["--set-upstream", self.original_remote_name, self.target_branch]
        if self.force:
            push_args.insert(0, "--force")
        logger.info(f'called __push {repo}, {push_args}')
        # is_push_success = push(repo, push_args)
        is_push_success = push_to_gerrit(repo=repo,branch='main',gerrit_ref='refs/for/main')
        logger.debug(f"Pushed to {self.original_remote_name}/{self.target_branch}")
        return is_push_success

    def run(self) -> dict:
        # remote_repo_url = '/plugins/gitiles/testing-gerrit/.git'
        # repo = git.Repo(remote_repo_url,search_parent_directories=True)
        repo = git.Repo(Path.cwd(), search_parent_directories=True)
        logger.info(f'repo.branches{repo.branches}')
        logger.info(f'repo: {repo}')
        logger.info(f'self.target_branch & self.base_branch{self.target_branch},{self.base_branch}')
        if not self.enabled:
            logger.info('not enable!')
            if (
                self.base_branch == self.target_branch
                and len(list(repo.iter_commits(f"{self.target_branch}@{{u}}..{self.target_branch}"))) > 0
            ):
                logger.info('done 11')
                is_push_success = self.__push(repo)
                if not is_push_success:
                    self.set_status(
                        StepStatus.FAILED,
                        f"Failed to push to {self.original_remote_name}/{self.target_branch}. Skipping PR creation.",
                    )
                return dict()

            self.set_status(StepStatus.WARNING, "PR creation is disabled. Skipping PR creation.")
            logger.warning(f"PR creation is disabled. Skipping PR creation.")
            return dict()
        logger.info('its enabled')
        is_push_success = self.__push(repo)
        if not is_push_success:
            self.set_status(
                StepStatus.FAILED,
                f"Failed to push to {self.original_remote_name}/{self.target_branch}. Skipping PR creation.",
            )
            return dict()
        logger.info('code success fully pushed!!!')
        return dict()



def push_to_gerrit(repo: Repo, branch: str, gerrit_ref: str = None, force: bool = False) -> bool:
    """
    Push changes to a Gerrit server for code review.

    Args:
        repo (git.Repo): The git repository instance.
        branch (str): The local branch to push.
        gerrit_ref (str): The Gerrit refspec, e.g., 'refs/for/branch_name'. If None, 'refs/for/<branch>' is used.
        force (bool): Force push the changes.

    Returns:
        bool: True if the push succeeds, False otherwise.
    """ 
    if gerrit_ref is None:
        gerrit_ref = f"refs/for/{branch}"  # Default Gerrit refspec
    logger.info(f'function gerrit called {gerrit_ref}')
    push_args = [f"HEAD:{gerrit_ref}"]
    if force:
        push_args.insert(0, "--force")
    
    try:
        with repo.git.custom_environment(GIT_TERMINAL_PROMPT="0"):
            '-main'
            # repo.git.rebase('generatereadme-main')
            logger.info('hellooooooo')
            logger.info(push_args)
            # repo.git.push("origin", *push_args)
        logger.info("Push to Gerrit successful........")
        return True
    except GitCommandError as e:
        logger.error("Git command failed with1:")
        logger.error(e.stdout)
        logger.error(e.stderr)

    # Retry logic using `logger.freeze` if available
    logger.info('not working')
    freeze_func = getattr(logger, "freeze", None)
    if freeze_func:
        try:
            with logger.freeze():
                repo.git.push("origin", *push_args)
            logger.info("Push to Gerrit successful after retry.")
            return True
        except GitCommandError as e:
            logger.error("Git retry failed with:")
            logger.error(e.stdout)
            logger.error(e.stderr)

    return False

def push(repo: git.Repo, args) -> bool:
    try:
        with repo.git.custom_environment(GIT_TERMINAL_PROMPT="0"):
            # logger.info('push args',args)            

            repo.git.push(*args)
            logger.info("Push to Gerrit successful.")
        return True
    except GitCommandError as e:
        logger.error("Git command failed with:")
        logger.error(e.stdout)
        logger.error(e.stderr)

    freeze_func = getattr(logger, "freeze", None)
    if freeze_func is None:
        return False

    try:
        with logger.freeze():
            repo.git.push(*args)
        return True
    except GitCommandError as e:
        logger.error("Git command failed with:")
        logger.error(e.stdout)
        logger.error(e.stderr)

    return False


def create_pr(
    repo_slug: str,
    body: str,
    title: str,
    base_branch_name: str,
    target_branch_name: str,
    scm_client: ScmPlatformClientProtocol,
    force: bool = False,
):
    prs = scm_client.find_prs(repo_slug, original_branch=base_branch_name, feature_branch=target_branch_name)
    pr = next(iter(prs), None)
    if pr is None:
        pr = scm_client.create_pr(
            repo_slug,
            title,
            body,
            base_branch_name,
            target_branch_name,
        )

        pr.set_pr_description(body)

        return pr.url()

    if force:
        pr.set_pr_description(body)
        return pr.url()

    logger.error(
        f"PR with the same base branch, {base_branch_name}, and target branch, {target_branch_name},"
        f" already exists. Skipping PR creation."
    )
    return ""
