import os
from src import create_logger


def check_running(logger):
    logger.info(f'ChatBot has been started.')


def check_dir(logger, dir_name: str):
    if os.path.isdir(dir_name):
        logger.info(f'Directory "ChatBot/{dir_name}" exists.')
    else:
        logger.critical(f'Directory "ChatBot/{dir_name}" does not exist.')


def check_dirs(logger, dir_names: list[str]):
    for dir_name in dir_names:
        check_dir(logger, dir_name)

def check_openai_token(logger):
    try:
        logger.info(f'OpenAI token: "{os.environ["OPENAI_API_KEY"]}"')
    except KeyError:
        logger.exception('OpenAI token does not exist.')


def check_app():
    logger = create_logger('check_app.log')
    
    check_openai_token(logger)
    check_running(logger)
    check_dirs(logger, ['src', 'docs', 'logs', 'index'])
