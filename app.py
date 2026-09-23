from config.settings import load_settings
from core.logging_setup import configure_logging
from security.policy import PermissionLevel, evaluate_permission


def main() -> None:
    settings = load_settings()
    logger = configure_logging(settings.log_level)

    decision = evaluate_permission(
        PermissionLevel.READ_ONLY,
        confirmed=False,
    )

    logger.info("ANNA AI foundation started.")
    logger.info("Environment: %s", settings.environment)
    logger.info("Privacy mode: %s", settings.privacy_mode)
    logger.info("Read-only policy check: allowed=%s", decision.allowed)

    print("ANNA AI foundation is running.")


if __name__ == "__main__":
    main()
