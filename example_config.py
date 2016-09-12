bot_name = 'kakaushka_themes'
token = ''

mongo_db_name = 'kakaushka'
mongo_collection_name = 'themes'

help_message = (
    '/touch {theme text} - create new theme\n'
    '/ls - get list of all themes\n'
    '/ed {theme_number} {new_theme_text} - update theme\n'
    '/rm {theme_number} - remove theme\n'
    '/tar {theme_number} - move theme to archive, not implemented yet\n'
    '/man or /help - this message\n'
    'Each command has a shortcut, /{first_letter}\n'
    'Markdown is allowed'
)
