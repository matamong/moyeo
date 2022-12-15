from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev moyeo-dc"

    class Config(AppSettings.Config):
        env_file = ".env"