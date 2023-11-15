from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # APPLICATION
    PROPERTIES_API_URL: str
    GREY_WOLF_SERVICE_URL: str

    class Config:
        """Load config file"""

        env_file = ".env"
        extra = "ignore"
