
from dotenv import dotenv_values

from snowflake.snowpark.context import get_active_session

env_vars=dotenv_values('.env')
from snowflake.snowpark import Session
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
ctx = get_script_run_ctx()


class SessionManager:
    is_session_local = None
    def is_data_local():
        if SessionManager.is_session_local is None:
            try:
                session = get_active_session()
                SessionManager.is_session_local = False
            except:
                SessionManager.is_session_local = True 
        return SessionManager.is_session_local
    
    def get_session_id():      
        return ctx.session_id
    

    
class SnowflakeSession:
    def get_session(self):
        try:
            session=get_active_session()
            return session
        except:
            session= Session.builder.configs({
                "user": env_vars.get('user'),
                "password": env_vars.get('password'),
                "account": env_vars.get('account'),
                "role": env_vars.get('role'),
                "database": env_vars.get('database'),
                "schema": env_vars.get('schema')
                }).create()
            return session