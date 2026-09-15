import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from jawn.settings import BASE_DIR
from krogoth_gantry.krogoth_compiler import MasterCompiler
from krogoth_gantry.models.gantry_models import KrogothGantryMasterViewController

COMPILED_DIR = os.path.join(BASE_DIR, 'static', 'compiled')


class Command(BaseCommand):
    help = 'Compiles every enabled Master View Controller into static/compiled/ for STATIC_KROGOTH_MODE.'

    def add_arguments(self, parser):
        parser.add_argument('--no-collectstatic', action='store_true',
                            help='Skip collectstatic. Files land in static/compiled/ but are not served yet.')
        parser.add_argument('--clean', action='store_true',
                            help='Delete .js files that no longer match an enabled Master View Controller.')
        parser.add_argument('--name', type=str, default='',
                            help='Only compile this one Master View Controller.')

    def handle(self, *args, **options):
        os.makedirs(COMPILED_DIR, exist_ok=True)
        self.stdout.write('compiling into %s' % COMPILED_DIR)

        masters = KrogothGantryMasterViewController.objects.filter(is_enabled=True).order_by('name')
        if options['name']:
            masters = masters.filter(name=options['name'])
            if not masters.exists():
                self.stdout.write(self.style.ERROR('no enabled Master View Controller named "%s"'
                                                   % options['name']))
                return

        written = []
        failed = []
        total_bytes = 0
        for master in masters:
            target = os.path.join(COMPILED_DIR, master.name + '.js')
            try:
                compiled_js = MasterCompiler(username='Guest').compiled_raw(named=master.name)
            except Exception as exc:
                failed.append(master.name)
                self.stdout.write(self.style.ERROR('  FAIL  %-26s %s: %s'
                                                   % (master.name, type(exc).__name__, exc)))
                continue
            with open(target, 'w') as handle:
                handle.write(compiled_js)
            written.append(master.name + '.js')
            total_bytes += len(compiled_js)
            self.stdout.write(self.style.SUCCESS('  ok    %-26s %8d bytes' % (master.name, len(compiled_js))))

        if options['clean']:
            for stale in sorted(set(os.listdir(COMPILED_DIR)) - set(written)):
                if stale.endswith('.js'):
                    os.remove(os.path.join(COMPILED_DIR, stale))
                    self.stdout.write(self.style.WARNING('  removed stale %s' % stale))

        self.stdout.write('%s compiled, %s failed, %s bytes total'
                          % (len(written), len(failed), total_bytes))

        if failed:
            self.stdout.write(self.style.ERROR(
                'Not running collectstatic because %s file(s) failed to compile.' % len(failed)))
            return

        if options['no_collectstatic']:
            self.stdout.write(self.style.WARNING(
                'Skipped collectstatic. Run it before enabling STATIC_KROGOTH_MODE.'))
        else:
            call_command('collectstatic', interactive=False, verbosity=0)
            self.stdout.write(self.style.SUCCESS('collectstatic done'))

        self.stdout.write(self.style.SUCCESS('Ready for STATIC_KROGOTH_MODE = True'))
