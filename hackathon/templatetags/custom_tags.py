
# range snippet from: https://www.djangosnippets.org/snippets/1357/
# adjusted to current project needs based on https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
import re

from django.template import Library
from django.db.models import Q
import datetime
from hackathon.models import Hackathon

ANCHOR_PATTERN = r'href[=][\"]?.+?(?=[\"])[\"]'

register = Library()


@register.filter
def get_range(value, start):
    """
        Filter - returns a list containing range made from given value
        Usage (in template):
        <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
        {% endfor %}</ul>
        Results with the HTML:
        <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
        </ul>
        Instead of 3 one may use the variable set in the views
    """
    return range(start, value+1, 1)


@register.filter
def event_ended(date_event):
    '''Set a filter to check if hackaton has ended
    In order to show the enroll button only for hackatons which are not ended
    Date can be updated if organisers want to put a deadline to enrol
    Help provided in Stack overflow: https://stackoverflow.com/questions/64605335/comparing-dates-using-a-comparator-inside-django-template/64605785#64605785'''
    return date_event.date() >= datetime.date.today()


@register.filter
def get_value_from_dict(data, key):
    """ Retrieves a value from a dict based on a given key """
    if key:
        return data.get(key)


@register.filter
def to_list(data):
    return list(data)


@register.filter
def sort_list(data):
    return sorted(list(data))


@register.filter
def place_identifier(num):
    num_str = str(num)
    if not isinstance(num, int):
        # no score
        return ''
    if num_str[-1] == '1':
        return num_str + 'st'
    elif num_str[-1] == '2':
        return num_str + 'nd'
    elif num_str[-1] == '3':
        return num_str + 'rd'
    else:
        return num_str + 'th'


@register.filter
def prettify_status(status, max_participants_reached):
    if status == 'published' or status == 'draft':
        return "Registration Starts Soon"
    elif status == 'registration_open' and not max_participants_reached:
        return "Registration Open"
    elif status == 'registration_open' and max_participants_reached:
        return "Registration Closed"
    elif status == 'hack_prep':
        return "Hackathon Starting Soon"
    elif status == 'hack_in_progress':
        return "Hackathon In Progress"
    elif status == 'judging':
        return "Judging In Progress"
    else:
        return "Hackathon Finished"


@register.filter
def get_assigned_team(participant, hackathon):
    """ Return the team for the current hackathon for a participant """
    participant_team = None
    if not hackathon.teams:
        return

    teams = hackathon.teams.all()
    participant_team = [team for team in teams
                        if participant in team.participants.all()]

    if len(participant_team) == 0:
        return

    return participant_team[0]


@register.filter
def get_mentored_team(mentor, hackathon):
    """ Retrieve all mentored teams for a Judge at a Hackathon """
    mentored_teams = None
    mentored_teams = mentor.mentored_teams.filter(
        hackathon=hackathon).order_by('display_name')
    return mentored_teams


@register.filter
def filter_judge_scores(scores, judge):
    """ Filters all scores for a team based on judge """
    judge_scores = scores.filter(judge=judge)
    if judge_scores:
        return judge_scores
    return


@register.filter
def remove_hrefs(text):
    """ Remove all href attributes from the text
    
    TODO: Add functionality to only remove specific links and show others
    """
    return re.sub(ANCHOR_PATTERN, '', text)


@register.filter
def user_is_blocked(user, hackathon):
    """ Checks if the user is blocked from the this hackathon""" 
    if not user.dropped_off_hackathon:
        return False
    else:
        orgs = [1]
        orgs.append(user.organisation.id)
        hackathons = Hackathon.objects.filter((Q(organisation__in=orgs) | Q(is_public=True)) & Q(end_date__lte=hackathon.end_date)).exclude(status__in=['deleted', 'draft']).order_by('-end_date')
        if user.dropped_off_hackathon in hackathons[:2]:
            return True
        return False
      
