AMIZONE_ID = 'AMIZONE ID HERE'
AMIZONE_PASSWORD = 'AMIZONE PASSWORD HERE'
BOT_TOKEN = 'BOT TOKEN HERE'

# Seed values that are stored in DB after "bot.py --fresh-db-seed" or "bot.py --db-seed"
SUPER_ADMIN_ID = 'SUPER ADMIN ID HERE'  # Super admin can use "/set_group", "/set_subjects" and "/set_admins" commands
GROUP_ID = 'GROUP ID HERE'  # Group ID where bot sends messages to (using "/send_group", "/reply_group" etc. commands)
# GROUP_ID can be set as None or ''
# NOTE: Telegram group ID format starts from -100: add prefix -100 if not present
