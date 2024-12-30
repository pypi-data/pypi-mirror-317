import os
import tempfile
from typing import List

import git
from github import Github
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from dataclasses import dataclass
import logging
import time

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Document:
    url: str
    content: str

class GitRepoIngestor:
    def __init__(
        self,
        gittoken: str=None,
        max_file_size: int = 50,  # Default max file size is 50 KB
        file_types: list = ['.py'],  # Default file types are .py files
        log_level: str = 'INFO',  # Default log level is DEBUG
        max_retries: int = 3,  # Maximum number of retries for cloning
        use_ssh: bool = False  # Use SSH instead of HTTPS
    ):
        self.github_token = gittoken or "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"
        self.max_file_size = max_file_size * 1024  # Convert to kb
        self.file_types = file_types
        self.log_level = log_level.upper()
        self.max_retries = max_retries
        self.use_ssh = use_ssh
        logging.getLogger().setLevel(self.log_level)

    def get_repo_content(self, github_url: str) -> Document:
        # Initialize a Github instance with your token
        g = Github(self.github_token)

        # Extract the repository name from the URL
        repo_name = github_url.strip('/').split('/')[-2:]
        if len(repo_name) != 2:
            raise ValueError("Invalid GitHub URL")

        # Get the repository
        repo = g.get_repo('/'.join(repo_name))

        # Create a temporary directory to clone the repository
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the repository with retries
            for attempt in range(self.max_retries):
                try:
                    logging.info(f"Cloning repository to {temp_dir} (Attempt {attempt + 1})")
                    start_time = time.time()

                    if self.use_ssh:
                        # Convert HTTPS URL to SSH URL
                        ssh_url = f"git@github.com:{repo.full_name}.git"
                        git.Repo.clone_from(ssh_url, temp_dir, env={'GIT_SSH_COMMAND': 'ssh'})
                    else:
                        git.Repo.clone_from(repo.clone_url, temp_dir)

                    logging.info(f"Repository cloned in {time.time() - start_time:.2f} seconds")
                    break
                except git.exc.GitCommandError as e:
                    logging.error(f"Clone failed on attempt {attempt + 1}: {e}")
                    if attempt == self.max_retries - 1:
                        raise

            # Collect all files in the repository
            file_paths = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, temp_dir)
                    file_paths.append((file_path, relative_path))

            logging.info(f"Found {len(file_paths)} files in the repository")

            # Function to process a single file
            def process_file(file_path, relative_path):
                try:
                    # Check if the file type is in the allowed list
                    if not any(relative_path.endswith(ext) for ext in self.file_types):
                        logging.debug(f"Skipping file {relative_path} (not in allowed types)")
                        return None

                    # Check if the file size is within the limit
                    file_size = os.path.getsize(file_path)
                    if file_size > self.max_file_size:
                        logging.debug(f"Skipping file {relative_path} (size exceeds limit)")
                        return f"================================================\nFile: {relative_path}\n================================================\nFile size exceeds the limit of {self.max_file_size} bytes.\n"

                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        logging.debug(f"Read file {relative_path} with size {file_size} bytes")
                        return f"================================================\nFile: {relative_path}\n================================================\n{file_content}\n"
                except Exception as e:
                    logging.error(f"Could not read file {relative_path}: {str(e)}")
                    return f"================================================\nFile: {relative_path}\n================================================\nCould not read file {relative_path}: {str(e)}\n"

            # Use ThreadPoolExecutor to process files concurrently
            logging.debug(f"Processing files with ThreadPoolExecutor")
            start_time = time.time()
            with ThreadPoolExecutor() as executor:
                future_to_path = {executor.submit(process_file, file_path, relative_path): (file_path, relative_path) for
                                  file_path, relative_path in file_paths}
                content = []
                for future in as_completed(future_to_path):
                    file_path, relative_path = future_to_path[future]
                    try:
                        result = future.result()
                        if result:
                            content.append(result)
                    except Exception as e:
                        logging.error(f"Error processing file {relative_path}: {str(e)}")

            logging.info(f"Files processed in {time.time() - start_time:.2f} seconds")

            # Join all file contents into a single string
            return Document(url=github_url, content='\n'.join(content))

    def __call__(self, github_urls: list|str) -> List[Document]|Document:
        if isinstance(github_urls,str):
            # Single URL, process normally
            return self.get_repo_content(github_urls)
        else:
            # Multiple URLs, use multiprocessing
            with ProcessPoolExecutor() as executor:
                futures = {executor.submit(self.get_repo_content, url): url for url in github_urls}
                results = []
                for future in as_completed(futures):
                    url = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logging.error(f"Error processing repository {url}: {str(e)}")
                        results.append(Document(url=url, content=f"Error processing repository {url}: {str(e)}\n"))

            return results

    def run(self,github_urls:list|str) -> List[Document] | Document:
        return self.__call__(github_urls)

if __name__ == '__main__':
    github_urls = [
    "https://github.com/WooooDyy/AgentGym",
    "https://github.com/cyclotruc/gitingest"
]
    git_extractor = GitRepoIngestor()
    content = git_extractor(github_urls)
