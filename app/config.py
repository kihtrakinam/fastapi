from pydantic import BaseSettings

class Settings(BaseSettings):
	db : str
	db_driver : str
	db_host : str
	db_port : str
	db_name : str
	db_user : str
	db_password : str
	secret_key : str
	algorithm : str
	access_token_expire_minutes : int
	
	class Config:
		env_file = ".env"

settings = Settings()