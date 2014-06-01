from django.test import TestCase
import mock

from webfaction.models import User
from .models import Application, Database, APPTYPES, ENGINES


class ApplicationTests(TestCase):
    
    def setUp(self):
        with mock.patch('webfaction.tasks.create_user.delay'):
            owner = User.objects.create(email=u'brian@alwayslook.com', 
                                        preferred_name=u'Brian',
                                        wf_username='brian')
            Application.objects.create(name='static', apptype=APPTYPES.static, owner=owner)
            Application.objects.create(name='phpmysql', apptype=APPTYPES.phpmysql, owner=owner)
            Application.objects.create(name='wordpress', apptype=APPTYPES.wordpress, owner=owner)

    
    def test_wf_name(self):
        static = Application.objects.get(name='static')
        self.assertEqual(static.wf_name, '%s_%s' % (static.owner.wf_username, 'static'))
        
    
    def test_database(self):
        static = Application.objects.get(name='static')
        self.assertFalse(static.needs_db())
        self.assertEquals(static.needed_db_engine, None)
        
        php = Application.objects.get(name='phpmysql')
        self.assertTrue(php.needs_db())
        self.assertEquals(php.needed_db_engine, ENGINES.mysql)
        
        wordpress = Application.objects.get(name='wordpress')
        self.assertTrue(wordpress.needs_db())
        self.assertEquals(wordpress.needed_db_engine, ENGINES.mysql)
