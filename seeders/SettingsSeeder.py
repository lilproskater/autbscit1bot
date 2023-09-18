from helper import sql_exec
from config import SUPER_ADMIN_ID, GROUP_ID


class SettingsSeeder:
    @staticmethod
    def run():
        data = {
            'SUPER_ADMIN_ID': SUPER_ADMIN_ID,
        }
        if GROUP_ID:
            data['GROUP_ID'] = GROUP_ID
        q = None
        for key, value in data.items():
            try:
                q = f"INSERT INTO settings(key, value) VALUES('{key}', {value})"
                sql_exec(q)
            except Exception as e:
                return '\n'.join([f'Query: {q}', f'Error: {e}'])
