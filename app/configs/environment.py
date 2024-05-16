from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # APPLICATION
    GET_IMOVEIS_API_URL: str
    GET_IMOVEIS_API_URL: str

    class Config:
        """Load config file"""

        env_file = ".env"
        extra = "ignore"
