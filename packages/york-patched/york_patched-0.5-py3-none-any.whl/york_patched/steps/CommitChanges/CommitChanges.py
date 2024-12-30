from __future__ import annotations

import contextlib
from pathlib import Path
import pdb
import git
from git import Repo
from typing_extensions import Generator

from york_patched.common.utils.filter_paths import PathFilter
from york_patched.common.utils.utils import get_current_branch
from york_patched.logger import logger
from york_patched.step import Step, StepStatus


@contextlib.contextmanager
def transitioning_branches(
    repo: Repo, branch_prefix: str, branch_suffix: str = "", force: bool = True, enabled: bool = False
) -> Generator[tuple[str, str], None, None]:
    logger.info(f'self.enabled {enabled}')
        
    if enabled:
        logger.info("Branch creation is disabled.")
        from_branch = get_current_branch(repo)
        from_branch_name = from_branch.name if not from_branch.is_remote() else from_branch.remote_head
        yield from_branch_name, from_branch_name
        return

    logger.info(f'branch ho gya {repo.branches}')
    from_branch = get_current_branch(repo)
    logger.info(f'from_branch {from_branch}')
    from_branch_name = from_branch.name if not from_branch.is_remote() else from_branch.remote_head
    logger.info(f" branch_prefix :{branch_prefix} from_branch_name : {from_branch_name} branch_suffix: {branch_suffix}")
    next_branch_name = f"{branch_prefix}{from_branch_name}{branch_suffix}"
    # next_branch_name = f"t{from_branch_name}{branch_suffix}"
    if next_branch_name in repo.heads and not force:
        raise ValueError(f'Local Branch "{next_branch_name}" already exists.')
    if next_branch_name in repo.remote("origin").refs and not force:
        raise ValueError(f'Remote Branch "{next_branch_name}" already exists.')

    logger.info(f'Creating new branch "{next_branch_name}".')

    to_branch = repo.create_head(next_branch_name, force=force)
    logger.info(f'Created new branch "{next_branch_name}".{to_branch}')

    try:
        logger.info(f'before checkout {repo.branches}')
        logger.info('doneeeee!!!')
        to_branch.checkout()
        logger.info(f'after checkout {repo.branches}')
        
        logger.info('branch checkout')
        yield from_branch_name, next_branch_name
    finally:
        from_branch.checkout()


class _EphemeralGitConfig:
    _DEFAULT = -2378137912

    def __init__(self, repo: Repo):
        self._repo = repo
        self._keys: set[tuple[str, str]] = set()
        self._original_values: dict[tuple[str, str], str] = dict()
        self._modified_values: dict[tuple[str, str], str] = dict()

    def set_value(self, section: str, option: str, value: str):
        self._keys.add((section, option))
        self._modified_values[(section, option)] = value

    @contextlib.contextmanager
    def context(self):
        try:
            self._persist_values_to_be_modified()
            yield
        finally:
            self._undo_modified_values()

    def _persist_values_to_be_modified(self):
        reader = self._repo.config_reader("repository")
        for section, option in self._keys:
            original_value = reader.get_value(section, option, self._DEFAULT)
            if original_value != self._DEFAULT:
                self._original_values[(section, option)] = original_value

        writer = self._repo.config_writer()
        try:
            for section, option in self._keys:
                writer.set_value(section, option, self._modified_values[(section, option)])
        finally:
            writer.release()

    def _undo_modified_values(self):
        writer = self._repo.config_writer()
        try:
            for section, option in self._keys:
                original_value = self._original_values.get((section, option), None)
                if original_value is None:
                    writer.remove_option(section, option)
                else:
                    writer.set_value(section, option, original_value)
        finally:
            writer.release()


def commit_with_msg(repo: Repo, msg: str):
    logger.info('commit with msg called')
    ephemeral = _EphemeralGitConfig(repo)
    logger.info('commit with msg called 1')
    ephemeral.set_value("user", "name", "patched.codes[bot]")
    ephemeral.set_value("user", "email", "298395+patched.codes[bot]@users.noreply.github.com")
    # ephemeral.set_value("user", "name", "admin")
    # ephemeral.set_value("user", "email", "vipulp@york.ie")
    logger.info('commit with msg called 2')
    logger.info("Staging changes...")
    repo.git.add(".")
    logger.info(f'git status {repo.git.status()}')
    logger.info("Staging done...")
    logger.info(f'Staged changes: {repo.git.diff("--cached")}')

    # message_and_diff='hello'
    # import hashlib
    # change_id_hash = hashlib.sha1(message_and_diff.encode('utf-8')).hexdigest()
    
    # with ephemeral.context():
    #     repo.git.commit(
    #         # "--no-verify",
    #         "-m",
    #         "DONEEEE"
            
    #     )
        # repo.git.commit(
        #     "-m",
        #     "done",
        # )
        # repo.git.commit(
        #     "--author",
        #     "patched.codes[bot]<298395+patched.codes[bot]@users.noreply.github.com>",
        #     "-m",
        #     'done',
        #     'Change-Id:{change_id_hash}'.format(change_id_hash=change_id_hash),
        #     '--amend',
        # )
    logger.info('ephemeral set done') 
    
class CommitChanges(Step):
    required_keys = {"modified_code_files"}

    def __init__(self, inputs: dict):
        
        super().__init__(inputs)
        if not all(key in inputs.keys() for key in self.required_keys):
            raise ValueError(f'Missing required data: "{self.required_keys}"')

        self.enabled = not bool(inputs.get("disable_branch"))

        self.modified_code_files = inputs["modified_code_files"]
        logger.info('modified files {self.modified_code_files}')
        if len(self.modified_code_files) < 1:
            logger.warn("No modified files to commit changes for.")
            self.enabled = False

        self.force = inputs.get("force_branch_creation", True)
        self.branch_prefix = inputs.get("branch_prefix", "patchwork-")
        self.branch_suffix = inputs.get("branch_suffix", "")
        if self.enabled and self.branch_prefix == "" and self.branch_suffix == "":
            raise ValueError("Both branch_prefix and branch_suffix cannot be empty")

    def __get_repo_tracked_modified_files(self, repo: Repo) -> set[Path]:
        
        repo_dir_path = Path(repo.working_tree_dir)
        path_filter = PathFilter(repo.working_tree_dir)

        repo_changed_files = set()
        for item in repo.index.diff(None):
            repo_changed_file = Path(item.a_path)
            possible_ignored_grok = path_filter.get_grok_ignored(repo_changed_file)
            if possible_ignored_grok is not None:
                logger.warn(f'Ignoring file: {item.a_path} because of "{possible_ignored_grok}" in .gitignore file.')
                continue
            repo_changed_files.add(repo_dir_path / repo_changed_file)

        return repo_changed_files

    def run(self) -> dict:
        cwd = Path.cwd()
        repo = git.Repo(cwd, search_parent_directories=True)
        repo_dir_path = Path(repo.working_tree_dir)
        repo_changed_files = self.__get_repo_tracked_modified_files(repo)
        repo_untracked_files = {repo_dir_path / item for item in repo.untracked_files}
        modified_files = {Path(modified_code_file["path"]).resolve() for modified_code_file in self.modified_code_files}
        true_modified_files = modified_files.intersection(repo_changed_files.union(repo_untracked_files))
        logger.info(f'true_modified_files {true_modified_files}')
        if len(true_modified_files) < 1:
            self.set_status(
                StepStatus.SKIPPED, "No file found to add, commit and push. Branch creation will be disabled."
            )
            from_branch = get_current_branch(repo)
            from_branch_name = from_branch.name if not from_branch.is_remote() else from_branch.remote_head
            return dict(target_branch=from_branch_name)

        logger.info(f'self.enabled {self.enabled}')
        with transitioning_branches(
            repo,
            branch_prefix=self.branch_prefix,
            branch_suffix=self.branch_suffix,
            force=self.force,
            enabled=self.enabled,
        ) as (
            from_branch,
            to_branch,
        ):
            logger.info('ho rha hai!!!')
            logger.info(true_modified_files)
            for modified_file in true_modified_files:
                logger.info('gerrit adding file to commit')
                repo.git.add(modified_file)
                logger.info('gerrit adding files commit done')
                logger.info(repo)
                logger.info(modified_file)
                commit_with_msg(repo, f"Patched {modified_file}")
            
            logger.info(f'{from_branch} to {to_branch}')

            return dict(
                base_branch=from_branch,
                target_branch=to_branch,
            )
