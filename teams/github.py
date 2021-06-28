from copy import deepcopy
import re
import requests

from django.conf import settings
import plotly.graph_objects as go
import pandas as pd

GITHUB_EVENTS = [
    'CommitCommentEvent', 'CreateEvent', 'DeleteEvent', 'ForkEvent',
    'GollumEvent', 'IssueCommentEvent', 'IssuesEvent', 'MemberEvent',
    'PublicEvent', 'PullRequestEvent', 'PullRequestReviewEvent',
    'PullRequestReviewCommentEvent', 'PushEvent', 'ReleaseEvent',
    'SponsorshipEvent', 'WatchEvent',
    ]

GITHUB_EVENTS_DEFAULT = {
    'CommitCommentEvent': 0,
    'CreateEvent': 0,
    'DeleteEvent': 0,
    'ForkEvent': 0,
    'GollumEvent': 0,
    'IssueCommentEvent': 0,
    'IssuesEvent': 0,
    'MemberEvent': 0,
    'PublicEvent': 0,
    'PullRequestEvent': 0,
    'PullRequestReviewEvent': 0,
    'PullRequestReviewCommentEvent': 0,
    'PushEvent': 0,
    'ReleaseEvent': 0,
    'SponsorshipEvent': 0,
    'WatchEvent': 0,
}

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


def get_repo_events(owner, repo, endpoint='events'):
    """ Retrieves all events from a public GitHub repo

    This endpoint can only retrieve events from the last 90 days

    Returns the collated list of all paginated results """
    data = []
    url = (f'https://api.github.com/repos/{owner}/{repo}/{endpoint}'
           f'?per_page=100')
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


def aggregate_repo_events(owner, repo):
    """ Aggregates the repo events based on the contributor """
    aggregated_events = {}
    repo_events = get_repo_events(owner, repo)
    unique_repo_events = list(set(event.get('type') for event in repo_events))
    default_events = {k: v for k, v in GITHUB_EVENTS_DEFAULT.items()
                      if k in unique_repo_events}
    for event in repo_events:
        user = event.get('actor', {}).get('login')
        event_type = event.get('type')
        aggregated_events.setdefault(user, {})
        aggregated_events[user].setdefault('events',
                                           deepcopy(default_events))
        aggregated_events[user]['events'][event_type] += 1
    return aggregated_events, default_events


def aggregate_contributor_stats(owner, repo):
    """ Aggregates the repo contributor stats based on the contributor """
    aggregated_contributor_stats = {}
    repo_contributor_stats = get_repo_events(owner, repo,
                                             endpoint='stats/contributors')
    for contributor in repo_contributor_stats:
        user = contributor.get('author', {}).get('login')
        if not contributor.get('weeks'):
            continue

        df = pd.DataFrame(contributor.get('weeks'))
        # Aggregates additions, deletions and commits over all weeks and
        # converts df back to a dict
        aggregated_values = df.loc[:, ['a', 'd', 'c']].sum(
            axis=0, skipna=True).to_dict()
        aggregated_contributor_stats.setdefault(user, {})
        aggregated_contributor_stats[user]['stats'] = aggregated_values
    return aggregated_contributor_stats


def combine_stats_and_events(owner, repo):
    """ Combines contributor stats and repo events for the contributor in
    one dict """
    repo_events, default_events = aggregate_repo_events(owner, repo)
    contributor_stats = aggregate_contributor_stats(owner, repo)
    for user, contributor in contributor_stats.items():
        events = repo_events.get(user, {}).get('events',
                                               deepcopy(default_events))
        contributor_stats[user]['events'] = events
    return contributor_stats


def create_spider_chart_data(contributor_stats):
    """ Creates the data used for the spider charts"""
    data = []
    for user, stats in contributor_stats.items():
        chart_data = {}
        chart_data['label'] = user
        chart_data['data'] = [val for val in stats['events'].values()]
        chart_data['categories'] = [key for key in stats['events'].keys()]
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
    fig.update_xaxes(automargin=True)

    return fig.to_html(full_html=False, default_height=400, default_width=550)


def extract_owner_and_repo_from_url(url):
    """ Extracts the owner and repo from a github repo url """
    pattern = r'^((http|https)[:][\/][\/]|www)?([a-zA-Z0-9]|[._-]|[@])*[\/]'
    owner_repo = re.sub(pattern, '', url).split('/')
    owner, repo = owner_repo[0], owner_repo[1]
    return owner, repo
