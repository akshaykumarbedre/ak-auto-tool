# GitHub GraphQL API Example

This directory contains examples for working with GitHub's GraphQL API.

## Overview

GitHub's GraphQL API allows you to create, read, update, and manage GitHub resources like issues, pull requests, and repositories using GraphQL queries and mutations.

## Issue Created via GraphQL

This example was created in response to an issue that was created via GitHub's GraphQL API, demonstrating the automation capabilities of the platform.

## Examples

### Query to Get Repository Issues

```graphql
query {
  repository(owner: "akshaykumarbedre", name: "ak-auto-tool") {
    issues(first: 10, states: OPEN) {
      nodes {
        number
        title
        body
        author {
          login
        }
      }
    }
  }
}
```

### Mutation to Create an Issue

```graphql
mutation {
  createIssue(input: {
    repositoryId: "REPOSITORY_ID",
    title: "My New Issue via GraphQL",
    body: "This issue should be assigned to Copilot."
  }) {
    issue {
      number
      title
      url
    }
  }
}
```

### Mutation to Update an Issue

```graphql
mutation {
  updateIssue(input: {
    id: "ISSUE_ID",
    assigneeIds: ["USER_ID"]
  }) {
    issue {
      number
      title
      assignees(first: 5) {
        nodes {
          login
        }
      }
    }
  }
}
```

## Resources

- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer)
- [GraphQL Specification](https://graphql.org/)

## Authentication

To use GitHub's GraphQL API, you need a personal access token with appropriate permissions:

```bash
export GITHUB_TOKEN="your_token_here"
```

## Using with curl

```bash
curl -H "Authorization: bearer $GITHUB_TOKEN" \
     -X POST \
     -d '{"query": "query { viewer { login } }"}' \
     https://api.github.com/graphql
```

## Next Steps

- Explore the GitHub GraphQL API documentation
- Try the examples in GitHub's GraphQL Explorer
- Build automation tools using GraphQL queries and mutations
