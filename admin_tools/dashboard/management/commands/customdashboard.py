import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

DEFAULT_FILE = "dashboard.py"


class Command(BaseCommand):
    help = (
        "Creates a template file containing the base code to get you "
        "started with your custom dashboard."
    )

    def add_arguments(self, parser):
        parser.add_argument("output_file", type=str)

    def handle(self, output_file=None, **options):
        context = {}
        context["project"] = os.path.basename(os.getcwd())
        tpl = [
            "dashboard/dashboard.txt",
            "admin_tools/dashboard/dashboard.txt",
        ]
        dst = output_file is not None and output_file or DEFAULT_FILE
        if os.path.exists(dst):
            raise CommandError('file "%s" already exists' % dst)
        context["file"] = os.path.basename(dst).split(".")[0]

        with open(dst, "w") as f:
            f.write(render_to_string(tpl, context))
        self.stdout.write('"%s" written.' % os.path.join(dst))
