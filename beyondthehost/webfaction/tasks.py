"""
Celery tasks
"""

from celery import task
from celery.utils.log import get_task_logger

from .utils import WebFactionClient


logger = get_task_logger(__name__)


@task()
def create_user(uid, username, shell):
    """
    Creates a WebFaction user
    """
    from .models import User
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        logger.error('User %s does not exist. Aborting...' % username)
        return
    
    wf = WebFactionClient()
    try:        
        wf.create_user(username, shell, ['beyondwall'])
        user.wf_username = username
        user.save()
    except Exception as webfaction_error:
        logger.warning(webfaction_error)
        user.wf_username = ''
        user.save()
        return
    wf.system()

@task()
def delete_user(username):
    """
    Write a log entry to the database
    """
    wf = WebFactionClient()
    try:
        wf.delete_user(username)
    except Exception as webfaction_error:
        logger.warning(webfaction_error)       


@task()
def change_user_password(username, password):
    """
    Creates a WebFaction user
    """
    wf = WebFactionClient()
    try:
        wf.change_user_password(username, password)
    except Exception as webfaction_error:
        logger.warning(webfaction_error)


"""
from webfaction.tasks import create_user
from webfaction.models import User

user =User.objects.all()[0]

create_user(user)



"""