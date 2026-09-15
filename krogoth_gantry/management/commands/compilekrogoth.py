import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from jawn.settings import BASE_DIR
from krogoth_gantry.krogoth_compiler import MasterCompiler
from krogoth_gantry.krogoth_modelview_pods.kg_publicstatic_text import KPubStaticInterfaceText
from krogoth_gantry.krogoth_static_frontend import (
    SCRIPT_MANIFEST,
    STYLE_MANIFEST,
    VIEW_REFERENCE,
    compiled_name,
    enabled_master_names,
    render_document,
    render_view_html,
    rewrite_references,
    view_html_name,
)
from krogoth_gantry.models.gantry_models import (
    KrogothGantryMasterViewController,
    KrogothGantrySlaveViewController,
)

COMPILED_DIR = os.path.join(BASE_DIR, 'static', 'compiled')


class Command(BaseCommand):
    help = ('Compiles the Master View Controllers and the core frontend files into '
            'static/compiled/ for STATIC_KROGOTH_MODE.')
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument('--no-collectstatic', action='store_true',
                            help='Skip collectstatic. Files land in static/compiled/ but are not served yet.')
        parser.add_argument('--clean', action='store_true',
                            help='Delete files in static/compiled/ that this run did not produce.')
        parser.add_argument('--name', type=str, default='',
                            help='Only compile this one Master View Controller. Skips the core frontend.')
        parser.add_argument('--masters-only', action='store_true',
                            help='Compile only the Master View Controllers.')
        parser.add_argument('--framework-only', action='store_true',
                            help='Compile only the core frontend files.')

    def handle(self, *args, **options):
        if options['clean'] and options['name']:
            self.stdout.write(self.style.ERROR(
                '--clean cannot be used with --name; it would delete every other compiled file.'))
            return
        if options['masters_only'] and options['framework_only']:
            self.stdout.write(self.style.ERROR('--masters-only and --framework-only conflict.'))
            return

        os.makedirs(COMPILED_DIR, exist_ok=True)
        self.stdout.write('compiling into %s' % COMPILED_DIR)

        self.enabled_names = list(enabled_master_names())
        self.view_html_status = {}

        written = []
        failed = []

        do_masters = not options['framework_only']
        do_framework = not options['masters_only'] and not options['name']

        if do_masters:
            self.stdout.write(self.style.HTTP_INFO('Master View Controllers'))
            w, f = self.compile_masters(options['name'])
            written += w
            failed += f

        if do_framework:
            self.stdout.write(self.style.HTTP_INFO('Core frontend'))
            w, f = self.compile_framework()
            written += w
            failed += f

        collisions = sorted({n for n in written if written.count(n) > 1})
        if collisions:
            failed.append('name collision')
            self.stdout.write(self.style.ERROR(
                'Two sources wrote the same file: %s' % ', '.join(collisions)))

        if options['clean']:
            for stale in sorted(set(os.listdir(COMPILED_DIR)) - set(written)):
                os.remove(os.path.join(COMPILED_DIR, stale))
                self.stdout.write(self.style.WARNING('  removed stale %s' % stale))

        self.stdout.write('%s file(s) written, %s failed' % (len(written), len(failed)))

        if failed:
            self.stdout.write(self.style.ERROR(
                'Not running collectstatic because %s item(s) failed.' % len(failed)))
            return

        if options['no_collectstatic']:
            self.stdout.write(self.style.WARNING(
                'Skipped collectstatic. Run it before enabling STATIC_KROGOTH_MODE.'))
        else:
            call_command('collectstatic', interactive=False, verbosity=0)
            self.stdout.write(self.style.SUCCESS('collectstatic done'))

        if not options['name'] and not options['no_collectstatic']:
            self.stdout.write(self.style.SUCCESS('Ready for STATIC_KROGOTH_MODE = True'))

    def write(self, name, body):
        with open(os.path.join(COMPILED_DIR, name), 'w') as handle:
            handle.write(body)
        self.stdout.write(self.style.SUCCESS('  ok    %-54s %8d bytes' % (name, len(body))))

    def compile_masters(self, only_name):
        masters = KrogothGantryMasterViewController.objects.filter(is_enabled=True).order_by('name')
        if only_name:
            masters = masters.filter(name=only_name)
            if not masters.exists():
                self.stdout.write(self.style.ERROR(
                    '  no enabled Master View Controller named "%s"' % only_name))
                return [], ['missing master %s' % only_name]

        written, failed = [], []
        for master in masters:
            try:
                body = MasterCompiler(username='Guest').compiled_raw(named=master.name)
            except Exception as exc:
                failed.append(master.name)
                self.stdout.write(self.style.ERROR(
                    '  FAIL  %-54s %s: %s' % (master.name, type(exc).__name__, exc)))
                continue

            # The view HTML each templateUrl points at has to exist before the
            # URL is rewritten, so take the names from the compiled JS itself.
            available = set()
            for referenced in VIEW_REFERENCE.findall(body):
                name, ok = self.compile_view_html(referenced)
                if name:
                    written.append(name)
                if ok:
                    available.add(referenced)

            name = master.name + '.js'
            # MVC templates also reach for core partials such as content-only.html.
            self.write(name, rewrite_references(body, view_html_available=available))
            written.append(name)
        return written, failed

    def compile_view_html(self, referenced):
        """Write the .html a templateUrl resolves to, whether master or slave.

        Returns (name written or None, whether the target resolved). Two masters
        can share one slave view, so results are cached.
        """
        if referenced in self.view_html_status:
            return None, self.view_html_status[referenced]

        body = None
        master = KrogothGantryMasterViewController.objects.filter(name=referenced).first()
        if master is not None:
            body = render_view_html(master.view_html, master.style_css, master.get_theme_style)
        else:
            slave = KrogothGantrySlaveViewController.objects.filter(name=referenced).first()
            owner = slave.owner.first() if slave is not None else None
            if slave is None:
                self.stdout.write(self.style.WARNING(
                    '  skip  %-54s templateUrl target is neither a master nor a slave; '
                    'left on the live injector' % referenced))
            elif owner is None:
                self.stdout.write(self.style.WARNING(
                    '  skip  %-54s slave view has no owning master for its CSS; '
                    'left on the live injector' % referenced))
            else:
                body = render_view_html(slave.view_html, owner.style_css, owner.get_theme_style)

        self.view_html_status[referenced] = body is not None
        if body is None:
            return None, False

        name = view_html_name(referenced)
        self.write(name, rewrite_references(body))
        return name, True

    def compile_framework(self):
        documents = KPubStaticInterfaceText.objects.all().order_by('file_name')
        available = set()
        written, failed = [], []

        for document in documents:
            available.add(document.file_name)
            try:
                body = render_document(document, document.file_name,
                                       enabled_master_names=self.enabled_names,
                                       static_mode=True)
            except Exception as exc:
                failed.append(document.file_name)
                self.stdout.write(self.style.ERROR(
                    '  FAIL  %-54s %s: %s' % (document.file_name, type(exc).__name__, exc)))
                continue
            name = compiled_name(document.file_name)
            self.write(name, body)
            written.append(name)

        for expected in list(SCRIPT_MANIFEST) + list(STYLE_MANIFEST):
            if expected not in available:
                failed.append(expected)
                self.stdout.write(self.style.ERROR(
                    '  MISSING %-52s referenced by index_alt.html but not in the database' % expected))

        return written, failed
