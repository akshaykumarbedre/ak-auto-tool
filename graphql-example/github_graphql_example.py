#!/usr/bin/env python3
"""
GitHub GraphQL API Example Script

This script demonstrates how to interact with GitHub's GraphQL API
to query and manage issues.

Usage:
    export GITHUB_TOKEN="your_token_here"
    python github_graphql_example.py
"""

import os
import json
import sys

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class GitHubGraphQL:
    """Simple wrapper for GitHub GraphQL API"""
    
    def __init__(self, token=None):
        """Initialize with GitHub token"""
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable.")
        
        self.endpoint = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def execute_query(self, query, variables=None):
        """Execute a GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Query failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        
        if "errors" in result:
            raise Exception(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}")
        
        return result["data"]
    
    def get_repository_issues(self, owner, repo, first=10):
        """Get issues from a repository"""
        query = """
        query($owner: String!, $repo: String!, $first: Int!) {
          repository(owner: $owner, name: $repo) {
            issues(first: $first, states: OPEN, orderBy: {field: CREATED_AT, direction: DESC}) {
              totalCount
              nodes {
                number
                title
                body
                createdAt
                author {
                  login
                }
                labels(first: 5) {
                  nodes {
                    name
                  }
                }
              }
            }
          }
        }
        """
        
        variables = {
            "owner": owner,
            "repo": repo,
            "first": first
        }
        
        return self.execute_query(query, variables)
    
    def get_viewer(self):
        """Get information about the authenticated user"""
        query = """
        query {
          viewer {
            login
            name
            email
          }
        }
        """
        
        return self.execute_query(query)


def main():
    """Main function demonstrating API usage"""
    print("GitHub GraphQL API Example")
    print("=" * 50)
    
    try:
        # Initialize the API client
        gh = GitHubGraphQL()
        
        # Get authenticated user info
        print("\n1. Getting authenticated user info...")
        viewer = gh.get_viewer()
        print(f"   Logged in as: {viewer['viewer']['login']}")
        if viewer['viewer']['name']:
            print(f"   Name: {viewer['viewer']['name']}")
        
        # Example: Get repository issues
        print("\n2. Example: Get repository issues")
        print("   (Modify owner/repo as needed)")
        
        # You can uncomment and modify the following to query a specific repo:
        # owner = "OWNER"
        # repo = "REPO"
        # issues_data = gh.get_repository_issues(owner, repo, first=5)
        # issues = issues_data['repository']['issues']
        # print(f"\n   Found {issues['totalCount']} open issues")
        # for issue in issues['nodes']:
        #     print(f"   - #{issue['number']}: {issue['title']}")
        
        print("\n✓ GraphQL API connection successful!")
        print("\nYou can now use this script as a base for your automation tasks.")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("   Please set your GitHub token: export GITHUB_TOKEN='your_token'")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
