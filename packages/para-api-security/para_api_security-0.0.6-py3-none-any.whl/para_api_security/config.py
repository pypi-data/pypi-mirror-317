from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_MIDDLEWARE_SECRET: str
    KEYCLOAK_BASE_URL: str
    KEYCLOAK_REALM: str
    SMTP_SERVER: str
    SMTP_PORT: str
    SENDER_EMAIL: str
    KEYCLOAK_PUBLIC_KEY_URL: str
    PARA_APP_CLIENT_ID: str

    class Config:
        env_file = ".env"

settings = Settings()