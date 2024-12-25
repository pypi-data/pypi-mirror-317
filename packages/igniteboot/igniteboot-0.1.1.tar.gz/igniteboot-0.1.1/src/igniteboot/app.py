import logging
from .config import settings
from .route import Router
from .templates import template_engine
from .events import event_manager
from .session import SessionManager
from .db import create_database
from .auth import AuthSystem
from .plugin import PluginManager

logger = logging.getLogger("ignite")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class IgniteApp:
    def __init__(self):
        self.settings = settings
        self.router = Router()
        self.template_engine = template_engine
        self.event_manager = event_manager
        self.session_manager = SessionManager()
        self.db = create_database(self.settings.DATABASE_URL)
        self.auth_system = AuthSystem()
        self.plugin_manager = PluginManager(plugins_folder=self.settings.PLUGINS_FOLDER)

        logger.info("IgniteApp initialized with DB URL=%s", self.settings.DATABASE_URL)

        self.load_plugins()

    def add_route(self, path, handler, methods=["GET"]):
        self.router.add_route(path, handler, methods)

    def load_plugins(self):
        logger.info("Loading plugins from '%s'", self.plugin_manager.plugins_folder)
        self.plugin_manager.load_all_plugins()

    def run(self, host="127.0.0.1", port=8000):
        from .server import run_server
        logger.info("Starting server on %s:%d (debug=%s)", host, port, self.settings.DEBUG)
        run_server(self, host, port)

    def __call__(self, scope, receive, send):
        return self.router(scope, receive, send)
