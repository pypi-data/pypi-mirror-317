from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_MIDDLEWARE_SECRET: str
    KEYCLOAK_BASE_URL: str
    SMTP_SERVER: str
    SMTP_PORT: str
    SENDER_EMAIL: str

    @property
    def KEYCLOAK_PUBLIC_KEY_URL(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/certs"


    class Config:
        env_file = ".env"

settings = Settings(
    KEYCLOAK_CLIENT_ID="KEYCLOAK_CLIENT_ID",
    SMTP_SERVER="smtprelay.dar.global",
    SMTP_PORT="25",
    SENDER_EMAIL="paracode_admin@dar.com"
)