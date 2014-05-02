"""
Celery tasks
"""

from celery import task
from celery.utils.log import get_task_logger

from webfaction.utils import WebFactionClient


logger = get_task_logger(__name__)


@task()
def create_domain(domain_name):
    """
    Creates a domain using WebFaction API
    """
    from .models import Domain
    try:
        domain = Domain.objects.get(name=domain_name)
    except User.DoesNotExist:
        logger.error('Domain %s does not exist. Aborting...' % domain_name)
        return
    
    
    wf = WebFactionClient()
    try:
        subdomains = [subdomain.name for subdomain in domain.subdomains.all() if subdomain.name]  
        wf.create_domain(domain.name, *subdomains)
    except Exception as webfaction_error:
        logger.warning(webfaction_error)

@task()
def delete_domain(domain):
    """
    Deletes a domain using WebFaction API
    """
    wf = WebFactionClient()
    try:
        wf.delete_domain(domain)
    except Exception as webfaction_error:
        logger.warning(webfaction_error)       


@task()
def delete_subdomain(domain, *subdomains):
    """
    Deletes a subdomain using WebFaction API
    
    """
    if not len(subdomains):
        return
    wf = WebFactionClient()
    try:
        wf.delete_domain(domain, *subdomains)
    except Exception as webfaction_error:
        logger.warning(webfaction_error)       
