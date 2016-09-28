bot_name = 'kakaushka_themes'
token = ''

mongo_db_name = 'kakaushka'
mongo_collection_name = 'themes'
mongo_test_collection_name = 'themes_test'

help_message = (
    '/touch {theme text} - create new theme. Shortcut is /t\n'
    '/ls - get list of all themes. Shortcut is /l\n'
    '/ed {theme_number} {new_theme_text} - update theme. Shortcut is /e\n'
    '/rm {theme_number} - remove theme. Shortcut is /r\n'
    '/tar {theme_number} - move theme to archive, not implemented yet\n'
    '/man or /help - this message. Shortcuts are /m and /h\n'
    'Markdown is allowed'
)
