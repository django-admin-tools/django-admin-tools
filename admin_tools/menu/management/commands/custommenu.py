import os, shutil
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            '--file',
            help='The file path where the base code should be written (default: menu.py)',
            default='menu.py',
        ),
    )
    help = 'Creates a template file containing the base code to get you \
            started with your custom menu'
    args = '[file]'

    def handle(self, **options):
        project_name = os.path.basename(os.getcwd())
        src = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'menu.txt')
        dst = os.path.join(options['file'])
        if os.path.exists(dst):
            raise CommandError('Error: file "%s" already exists' % dst)
        open(dst, 'w').write(open(src).read() % {
            'project': project_name,
            'file': os.path.basename(options['file']).split('.')[0]
        })
        print '"%s" written.' % os.path.join(options['file'])

