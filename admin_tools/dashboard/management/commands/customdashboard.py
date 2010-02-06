import os, shutil
from optparse import make_option
from django.core.management.base import BaseCommand, LabelCommand, CommandError
from django.template.loader import render_to_string


DEFAULT_FILE = 'dashboard.py'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            '--file',
            help='The file path where the base code should be written (default: dashboard.py)',
            default=DEFAULT_FILE,
        ),
    )
    help = ('Creates a template file containing the base code to get you '
            'started with your custom dashboard.')
    args = '[appname]'
    label = 'application name'

    def handle(self, appname=None, **options):
        context = {}
        context['project'] = os.path.basename(os.getcwd())
        if appname:
            tpl = 'dashboard/dashboard_app_index.txt'
            if not os.path.exists(appname):
                raise CommandError('application "%s" not found' % appname)
            dst = os.path.join(appname, options['file'])
            context['app'] = appname
            if options['file'] != DEFAULT_FILE:
                context['warning'] = True
        else:
            tpl = 'dashboard/dashboard.txt'
            dst = os.path.join(options['file'])
        if os.path.exists(dst):
            raise CommandError('file "%s" already exists' % dst)
        context['file'] = os.path.basename(dst).split('.')[0]
        open(dst, 'w').write(render_to_string(tpl, context))
        print '"%s" written.' % os.path.join(options['file'])

