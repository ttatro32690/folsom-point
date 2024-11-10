from github import Github, GithubException, Repository
from ..config.config_loader import config
import logging
import base64
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubIntegration:
    def __init__(self):
        self.client = Github(config["GITHUB_ACCESS_TOKEN"])
        logger.info("GitHub client initialized")

    def _format_repository_details(self, repo: Repository.Repository) -> Dict[str, Any]:
        """Format repository details into a structured response."""
        return {
            "basic_info": {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "default_branch": repo.default_branch,
            },
            "stats": {
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "open_issues": repo.open_issues_count,
                "size": repo.size,  # in KB
                "network_count": repo.network_count,
                "subscribers_count": repo.subscribers_count,
            },
            "timestamps": {
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            },
            "owner": {
                "login": repo.owner.login,
                "url": repo.owner.html_url,
                "avatar_url": repo.owner.avatar_url,
                "type": repo.owner.type,
            },
            "settings": {
                "private": repo.private,
                "archived": repo.archived,
                "disabled": repo.disabled,
                "language": repo.language,
                "license": {
                    "name": repo.license.name if repo.license else None,
                    "key": repo.license.key if repo.license else None,
                    "url": repo.license.url if repo.license else None,
                },
                "topics": repo.get_topics(),
            },
            "features": {
                "has_issues": repo.has_issues,
                "has_projects": repo.has_projects,
                "has_wiki": repo.has_wiki,
                "has_downloads": repo.has_downloads,
                "has_pages": repo.has_pages,
            },
            "merge_settings": {
                "allow_forking": repo.allow_forking,
                "allow_squash_merge": repo.allow_squash_merge,
                "allow_merge_commit": repo.allow_merge_commit,
                "allow_rebase_merge": repo.allow_rebase_merge,
                "delete_branch_on_merge": repo.delete_branch_on_merge,
            },
            "metadata": {
                "homepage": repo.homepage,
                "visibility": repo.visibility,
                "organization": repo.organization.login if repo.organization else None,
            }
        }

    async def get_repository(self, repo_name: str) -> Dict[str, Any]:
        """
        Get comprehensive repository information.
        
        Args:
            repo_name (str): Repository name in format 'owner/repo'
            
        Returns:
            dict: Detailed repository information including statistics,
                 settings, and metadata
        
        Raises:
            GithubException: If repository access fails or not found
        """
        try:
            repo = self.client.get_repo(repo_name)
            response = self._format_repository_details(repo)
            
            # Add additional repository insights
            try:
                response["insights"] = {
                    "latest_release": {
                        "tag": repo.get_latest_release().tag_name,
                        "published_at": repo.get_latest_release().published_at.isoformat(),
                    } if repo.get_latest_release() else None,
                    "open_pull_requests": repo.get_pulls(state='open').totalCount,
                    "open_issues": repo.get_issues(state='open').totalCount,
                    "contributors_count": repo.get_contributors().totalCount,
                }
            except GithubException:
                response["insights"] = None
                logger.warning(f"Could not fetch additional insights for {repo_name}")
            
            return response
        except GithubException as e:
            logger.error(f"Error fetching repository {repo_name}: {str(e)}")
            raise

    async def list_files(self, repo_name: str, path: str = "", ref: str = None) -> Dict[str, Any]:
        """
        List files and directories in a repository path with enhanced metadata.
        
        Args:
            repo_name (str): Repository name in format 'owner/repo'
            path (str): Directory path within the repository
            ref (str): Branch or commit SHA
            
        Returns:
            Dict[str, Any]: Directory contents with metadata and structure information
        """
        try:
            repo = self.client.get_repo(repo_name)
            contents = repo.get_contents(path, ref=ref)
            
            response = {
                "repository": repo.full_name,
                "path": repo.path,
                "ref": ref or repo.default_branch,
                "total_items": len(contents) if isinstance(contents, list) else 1,
                "items": [],
                "structure": {
                    "directories": [],
                    "files": [],
                }
            }
            
            if not isinstance(contents, list):
                contents = [contents]
            
            for content in contents:
                item = {
                    "name": content.name,
                    "path": content.path,
                    "type": content.type,
                    "size": content.size,
                    "url": content.html_url,
                    "download_url": content.download_url,
                    "sha": content.sha,
                }
                
                response["items"].append(item)
                if content.type == "dir":
                    response["structure"]["directories"].append(content.path)
                else:
                    response["structure"]["files"].append(content.path)
            
            return response
        except GithubException as e:
            logger.error(f"Error listing files for {repo_name}: {str(e)}")
            raise

    async def read_file(self, repo_name: str, file_path: str, ref: str = None) -> Dict[str, Any]:
        """
        Read file contents with enhanced metadata and content analysis.
        
        Args:
            repo_name (str): Repository name in format 'owner/repo'
            file_path (str): Path to the file within the repository
            ref (str): Branch or commit SHA
            
        Returns:
            Dict[str, Any]: File contents and metadata
        """
        try:
            repo = self.client.get_repo(repo_name)
            content = repo.get_contents(file_path, ref=ref)
            
            # Get commit history for the file
            commits = repo.get_commits(path=file_path)
            latest_commit = next(iter(commits), None)
            
            # Decode content
            if content.encoding == "base64":
                file_content = base64.b64decode(content.content).decode('utf-8')
            else:
                file_content = content.content
            
            response = {
                "file_info": {
                    "name": content.name,
                    "path": content.path,
                    "size": content.size,
                    "sha": content.sha,
                    "type": content.type,
                    "encoding": content.encoding,
                    "url": content.html_url,
                    "download_url": content.download_url,
                },
                "content": file_content,
                "repository": {
                    "full_name": repo.full_name,
                    "default_branch": repo.default_branch,
                    "current_ref": ref or repo.default_branch,
                },
                "history": {
                    "latest_commit": {
                        "sha": latest_commit.sha if latest_commit else None,
                        "author": latest_commit.author.login if latest_commit and latest_commit.author else None,
                        "date": latest_commit.commit.author.date.isoformat() if latest_commit else None,
                        "message": latest_commit.commit.message if latest_commit else None,
                    } if latest_commit else None,
                    "total_commits": commits.totalCount,
                },
                "metadata": {
                    "lines": len(file_content.splitlines()) if isinstance(file_content, str) else None,
                    "extension": content.name.split('.')[-1] if '.' in content.name else None,
                }
            }
            
            return response
        except GithubException as e:
            logger.error(f"Error reading file {file_path} from {repo_name}: {str(e)}")
            raise

    async def search_code(self, query: str, repo_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced code search with detailed results and metadata.
        
        Args:
            query (str): Search query
            repo_name (Optional[str]): Limit search to specific repository
            
        Returns:
            Dict[str, Any]: Search results with metadata and statistics
        """
        try:
            if repo_name:
                query = f"{query} repo:{repo_name}"
            
            code_results = self.client.search_code(query)
            
            response = {
                "query": query,
                "total_count": code_results.totalCount,
                "incomplete_results": code_results.incomplete_results,
                "items": [],
                "statistics": {
                    "repositories": set(),
                    "languages": set(),
                    "file_types": set(),
                }
            }
            
            for item in code_results[:20]:  # Limit to first 20 results
                result = {
                    "file": {
                        "name": item.name,
                        "path": item.path,
                        "sha": item.sha,
                        "url": item.html_url,
                        "size": item.size,
                    },
                    "repository": {
                        "full_name": item.repository.full_name,
                        "description": item.repository.description,
                        "url": item.repository.html_url,
                        "stars": item.repository.stargazers_count,
                    },
                    "score": item.score,
                    "text_matches": item.text_matches if hasattr(item, 'text_matches') else None,
                }
                
                response["items"].append(result)
                
                # Update statistics
                response["statistics"]["repositories"].add(item.repository.full_name)
                if item.repository.language:
                    response["statistics"]["languages"].add(item.repository.language)
                if '.' in item.name:
                    response["statistics"]["file_types"].add(item.name.split('.')[-1])
            
            # Convert sets to lists for JSON serialization
            response["statistics"]["repositories"] = list(response["statistics"]["repositories"])
            response["statistics"]["languages"] = list(response["statistics"]["languages"])
            response["statistics"]["file_types"] = list(response["statistics"]["file_types"])
            
            return response
        except GithubException as e:
            logger.error(f"Error searching code: {str(e)}")
            raise

# Create a single instance
github_integration = GitHubIntegration()