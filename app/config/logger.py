from app.config.logging_config import setup_logger, LOG_DIR

logger = setup_logger("app_logger")
db_logger = setup_logger("database", LOG_DIR / "database.log")
repository_logger = setup_logger("repository", LOG_DIR / "repository.log")
services_logger = setup_logger("service", LOG_DIR / "service.log")
routes_logger = setup_logger("routes", LOG_DIR / "routes.log")
