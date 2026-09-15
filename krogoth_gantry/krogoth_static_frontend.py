"""Single source of truth for the Krogoth core frontend files.

These files live in the KPubStaticInterfaceText table. They are either served
one-at-a-time by load_static_text_readonly (STATIC_KROGOTH_MODE = False) or
written to static/compiled/ by the compilekrogoth command and served by nginx
(STATIC_KROGOTH_MODE = True).

SCRIPT_MANIFEST order is load order. AngularJS needs every angular.module()
definition to run before anything reopens that module, so do not sort it.
"""
import re

DEV_BASE = '/global_static_text/load_static_text_readonly/'
STATIC_BASE = '/static/compiled/'

MASTER_HTML_BASE = '/krogoth_gantry/DynamicHTMLInjector/?name='
SLAVE_HTML_BASE = '/krogoth_gantry/DynamicHTMLSlaveInjector/?name='

SCRIPT_MANIFEST = (
    'quick-panel.module.js',
    'core.module.js',

    'AKCustom.downloadLargeImageBackground.es6',
    'AKCustom.frostedGlassdirective.es6',
    'core.config.es6',
    'core.exampleCtrlLoadedByInjection.es6',
    'core.module.es6',
    'core.run.es6',
    'fil_altDate.filter.es6',
    'fil_basic.filter.es6',
    'filterByIds.filter.es6',
    'filterByPropIds.filter.es6',
    'fuse-config.provider.es6',
    'fuse-generator.service.es6',
    'fuse-palettes.constant.es6',
    'fuse-themes.constant.es6',
    'fuse-theming.config.es6',
    'fuse-theming.service.es6',
    'highlight.directive.es6',
    'ms-api.provider.es6',
    'ms-card.directive.es6',
    'ms-datepicker-fix.directive.es6',
    'ms-form-wizard.directive.es6',
    'ms-info-bar.directive.es6',
    'ms-masonry.directive.es6',
    'ms-nav.directive.es6',
    'ms-navigation.directive.es6',
    'ms-responsive-table.directive.es6',
    'ms-scroll.directive.es6',
    'ms-search-bar.directive.es6',
    'ms-sidenav-helper.directive.es6',
    'ms-splash-screen.directive.es6',
    'ms-stepper.directive.es6',
    'ms-timeline.es6',
    'ms-utils.service.es6',
    'ms-widget.directive.es6',
    'srv_api-resolver.service.es6',
    'tag.filter.es6',

    'chat-tab.controller.js',
    'toolbar.module.js',
    'toolbar.controller.js',
    'navigation.module.js',
    'navigation.controller.js',
    'quick-panel.controller.js',
    'index.module.js',
    'main.controller.js',
    'core.run.js',
    'core.config.js',
    'index.run.js',
    'index.route.js',
    'index.controller.js',
    'index.constants.js',
    'index.config.js',
)

STYLE_MANIFEST = (
    'LoadingScreen.css',
    'Core.css',
    'CoreElements.css',
    'CustomGlobals.css',
    'Background.css',
)

LOADING_STYLE = 'LoadingScreen.css'

_REFERENCE = re.compile(re.escape(DEV_BASE) + r'([A-Za-z0-9._-]+)')

# The trailing lookahead skips the "&tmpl=" lazy-load form, which carries a
# second parameter and so cannot be reduced to one static file.
VIEW_REFERENCE = re.compile(
    r'/krogoth_gantry/DynamicHTML(?:Slave)?Injector/\?name=([A-Za-z0-9._-]+)(?![A-Za-z0-9._-]|&)')


def compiled_name(filename):
    """Name to use on disk. nginx serves .es6 as octet-stream, so JS gets a .js tail."""
    if filename.endswith('.es6'):
        return filename + '.js'
    return filename


def dev_url(filename):
    # load_static_text_readonly is routed with a trailing slash; omitting it costs a 301.
    return DEV_BASE + filename + '/'


def static_url(filename):
    return STATIC_BASE + compiled_name(filename)


def frontend_url(filename, static_mode):
    return static_url(filename) if static_mode else dev_url(filename)


def frontend_urls(static_mode):
    return {
        'krogoth_frontend_scripts': [frontend_url(f, static_mode) for f in SCRIPT_MANIFEST],
        'krogoth_frontend_styles': [frontend_url(f, static_mode) for f in STYLE_MANIFEST],
        'krogoth_loading_style': frontend_url(LOADING_STYLE, static_mode),
    }


def view_html_name(name):
    return name + '.html'


def render_view_html(view_html, style_css, theme_style):
    """The body the DynamicHTML*Injector views return for one view controller.

    The injectors also carry a "no HTML component" placeholder, but it is
    unreachable: the style block is concatenated first, so the response is
    never empty. Only the reachable form is reproduced here.
    """
    return view_html + '<style>' + style_css + theme_style + '</style>'


def rewrite_references(body, view_html_available=None):
    """Point runtime template URLs at static/compiled/ instead of the live endpoints.

    view_html_available limits the templateUrl rewriting to names that were
    actually compiled. A target that does not exist is left on the live injector
    so a route already broken in dynamic mode breaks identically here, rather
    than turning into a confusing 404 for a missing static file.
    """
    body = _REFERENCE.sub(lambda m: STATIC_BASE + compiled_name(m.group(1)), body)

    def swap_view(match):
        name = match.group(1)
        if view_html_available is not None and name not in view_html_available:
            return match.group(0)
        return STATIC_BASE + view_html_name(name)

    return VIEW_REFERENCE.sub(swap_view, body)


def enabled_master_names():
    """Lazy queryset, so it only costs a query when index.module.js asks for it.

    Both the live endpoint and the compiler go through here; identical ordering
    is what keeps their output byte-for-byte the same.
    """
    from krogoth_gantry.models.gantry_models import KrogothGantryMasterViewController
    return KrogothGantryMasterViewController.objects.filter(
        is_enabled=True).order_by('name').values_list('name', flat=True)


def render_document(document, filename, enabled_master_names=(), static_mode=False):
    """Produce the exact bytes served for one framework file.

    Shared by load_static_text_readonly and compilekrogoth so the dynamic and
    compiled builds cannot drift apart.
    """
    injection = "console.log('DEPENDENCY CALLED: " + filename + "');var vm = this"
    body = document.content.replace("var vm = this", injection)

    if filename == 'index.module.js':
        my_apps = ''.join("\t\t\t'app." + name + "',\n" for name in enabled_master_names)
        body = body.replace('/*|#apps#|*/', my_apps)

    if static_mode:
        body = rewrite_references(body)
    return body


def content_type_for(file_kind):
    mime = (file_kind or '').upper()
    if mime in ('JS', 'ES6'):
        return 'text/javascript'
    return 'text/' + (file_kind or 'plain')
