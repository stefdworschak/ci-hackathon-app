import requests

from django.conf import settings


def get_repo_events(owner, repo):
    """ Retrieve all events from a public GitHub repo

    This endpoint can only retrieve events from the last 90 days

    Returns the collated list of all paginated results """
    data = []
    url = f'https://api.github.com/repos/{owner}/{repo}/events?per_page=100'
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
    pagination = {
        'next': url,
    }
    while pagination.get('next'):
        res = requests.get(pagination.get('next'), headers=headers)
        if res.status_code != 200:
            print(res.content)
            return []

        data += res.json()
        if not res.headers.get('Link'):
            print(res.headers.get('Link'))
            break

        pagination = get_pagination(res.headers.get('Link'))
        print(pagination)
    return data


def get_commit_details(url):
    """ Gets the commit's details from the GitHub API endpoint """
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {}
    return res.json()


def get_pagination(header_links):
    """ Extracts the pagination information from the GitHub API response
    headers """
    pagination = {}
    links = header_links.split(',')
    for link in links:
        url, params = link.split(';')
        # Remove quotes at the front and back
        position = params.split('=')[-1][1:-1]
        # Remove pointy brackets at the front and back
        pagination[position] = url.strip()[1:-1]
    return pagination


def create_activity_record(event):
    """ Creates an aggregate of one event including retrieving information
    from the commits from the GitHub API """
    activity_record = {}
    event_type = event.get('type')
    activity_record['type'] = event_type
    activity_record['user'] = event['actor']['login']
    if event_type == 'PullRequestEvent':
        pull_request = event.get('payload', {}).get('pull_request', {})
        activity_record['commits'] = pull_request.get('commits', 0)
        activity_record['additions'] = pull_request.get('additions', 0)
        activity_record['deletions'] = pull_request.get('deletions', 0)
    elif event_type == 'PushEvent':
        commits = event.get('payload', {}).get('commits', {})
        activity_record['commits'] = len(commits)
        # TODO: Tranverse through commits to get additions and deletions
        additions, deletions = get_push_additions_and_deletions(commits)
        activity_record['additions'] = additions
        activity_record['deletions'] = deletions
    else:
        activity_record['commits'] = 0
        activity_record['additions'] = 0
        activity_record['deletions'] = 0

    return activity_record


def get_push_additions_and_deletions(commits):
    additions = 0
    deletions = 0
    commit_details = []
    for commit in commits:
        url = commit.get('url')
        if url:
            commit_details.append(get_commit_details(url))

    additions = sum([commit.get('stats', {}).get('additions', 0)
                     for commit in commit_details])
    deletions = sum([commit.get('stats', {}).get('deletions', 0)
                     for commit in commit_details])

    return additions, deletions


def compile_repo_activity_by_user(owner, repo):
    repo_events = get_repo_events(owner, repo)
    repo_activity_records = [create_activity_record(event)
                             for event in repo_events]
    repo_activity = {}
    for record in repo_activity_records:
        user = record.get('user')
        event_type = record.get('type')
        repo_activity.setdefault(user, {})
        repo_activity[user].setdefault(event_type, [])
        repo_activity[user][event_type].append(record)

    return repo_activity
