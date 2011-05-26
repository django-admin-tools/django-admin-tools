import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string


DEFAULT_FILE = 'menu.py'

class Command(BaseCommand):
    help = ('Creates a template file containing the base code to get you '
            'started with your custom menu')
    args = ['file']

    def handle(self, file=None, **options):
        project_name = os.path.basename(os.getcwd())
        dst = file is not None and file or DEFAULT_FILE
        if os.path.exists(dst):
            raise CommandError('Error: file "%s" already exists' % dst)
        open(dst, 'w').write(render_to_string('admin_tools/menu/menu.txt', {
            'project': project_name,
            'file': os.path.basename(dst).split('.')[0]
        }))
        self.stdout.write('"%s" written.' % os.path.join(dst))

