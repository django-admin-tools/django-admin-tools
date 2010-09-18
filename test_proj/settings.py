# settings for django-admin-tools test project.
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')
MEDIA_URL = '/static/'
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'testdb.sqlite'
SITE_ID = 1
DEBUG = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates',
)

FIXTURE_DIRS = ['fixtures']

ADMIN_TOOLS_INDEX_DASHBOARD = 'test_proj.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_MENU = 'test_proj.menu.CustomMenu'

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'test_app',
]

try:
    import django_coverage
    TEST_RUNNER = 'django_coverage.coverage_runner.run_tests'
    COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(PROJECT_PATH, '_coverage')
except ImportError:
    pass
