import re
import requests

from django.conf import settings
import plotly.graph_objects as go

GITHUB_EVENTS = [
    'CommitCommentEvent', 'CreateEvent', 'DeleteEvent', 'ForkEvent',
    'GollumEvent', 'IssueCommentEvent', 'IssuesEvent', 'MemberEvent',
    'PublicEvent', 'PullRequestEvent', 'PullRequestReviewEvent',
    'PullRequestReviewCommentEvent', 'PushEvent', 'ReleaseEvent',
    'SponsorshipEvent', 'WatchEvent',
    ]

MODEBAR_REMOVE = [
    "autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio",
    "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d",
    "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset",
    "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo",
    "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews",
    "resetcameradefault", "resetcameralastsave", "resetsankeygroup",
    "resetscale", "resetview", "resetviews", "select", "select2d",
    "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation",
    "toImage", "toggleHover", "toggleSpikelines", "togglehover",
    "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d",
    "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox",
    "zoomin", "zoomout"]

GITHUB_DEFAULT_MAIN_BRANCHES = ["refs/heads/master", "refs/heads/main"]


def get_repo_events(owner, repo):
    """ Retrieves all events from a public GitHub repo

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
            return []

        data += res.json()
        if not res.headers.get('Link'):
            break

        pagination = get_pagination(res.headers.get('Link'))
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
        ref = event.get('payload', {}).get('ref')
        activity_record['commits'] = len(commits)
        # TODO: Tranverse through commits to get additions and deletions
        if ref in GITHUB_DEFAULT_MAIN_BRANCHES:
            additions, deletions = get_push_additions_and_deletions(commits)
        else:
            additions, deletions = 0, 0
        activity_record['additions'] = additions
        activity_record['deletions'] = deletions
    else:
        activity_record['commits'] = 0
        activity_record['additions'] = 0
        activity_record['deletions'] = 0

    return activity_record


def get_push_additions_and_deletions(commits):
    """ Retrieves all additions and deletions from a commit from the GitHub
    API endpoint """
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
    """ Compiles all activity for each user working on a repo """
    repo_events = get_repo_events(owner, repo)
    repo_activity_records = [create_activity_record(event)
                             for event in repo_events]
    repo_activity = {}
    for record in repo_activity_records:
        user = record.get('user')
        event_type = record.get('type')
        repo_activity.setdefault(user, {
            'events': {},
            'commits': 0,
            'additions': 0,
            'deletions': 0,
        })
        repo_activity[user]['events'].setdefault(event_type, 0)
        repo_activity[user]['events'][event_type] += 1
        repo_activity[user]['commits'] += record.get('commits', 0)
        repo_activity[user]['additions'] += record.get('additions', 0)
        repo_activity[user]['deletions'] += record.get('deletions', 0)

    return repo_activity


def create_spider_chart_data(repo_activity):
    """ Creates the data used for the spider charts"""
    data = []
    for user, activity in repo_activity.items():
        chart_data = {}
        chart_data['label'] = user
        chart_data['data'] = [activity['events'].get(category, 0)
                              for category in GITHUB_EVENTS]
        chart_data['categories'] = GITHUB_EVENTS
        data.append(chart_data)

    return data


def create_activity_spider_chart(chart_data):
    """ Creates chart from chart data and returns the HTML for the chart """
    fig = go.Figure()
    upper_range = 0
    for datapoint in chart_data:
        upper_range = max(upper_range, max(datapoint['data']))
        fig.add_trace(go.Scatterpolar(
            r=datapoint['data'],
            theta=datapoint['categories'],
            fill='toself',
            name=datapoint['label'],
            hovertemplate="%{theta}s: %{r}"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, upper_range]
            ),
        ),
        showlegend=True,
        autosize=True,
        modebar=dict(remove=MODEBAR_REMOVE),
    )

    return fig.to_html(full_html=False, default_height=500, default_width=600)


def extract_owner_and_repo_from_url(url):
    """ Extracts the owner and repo from a github repo url """
    pattern = r'^((http|https)[:][\/][\/]|www)?([a-zA-Z0-9]|[._-]|[@])*[\/]'
    owner_repo = re.sub(pattern, '', url).split('/')
    owner, repo = owner_repo[0], owner_repo[1]
    return owner, repo
