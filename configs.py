from os import getenv

PROMPT_COLLECTION = [
    '''
        Create a simple casual 2D game.

        Genre: arcade.
        Goal: the player must collect points and avoid obstacles.
        Gameplay: the character moves left and right, obstacles fall from the top of the screen, collectibles give bonus points.
        Difficulty: increases over time.
        Lose condition: collision with an obstacle.
        Win condition: survive as long as possible and get a high score.
        Visual style: colorful, minimalistic, cartoon.
        Controls: simple touch or swipe.
        Make the game fun and fast-paced.
    ''',

    '''
        Create a puzzle game.

        Genre: logic puzzle.
        Goal: solve each level using the least number of moves.
        Gameplay: the player moves blocks to reach the target area.
        Rules: blocks can be pushed but not pulled.
        Difficulty: each level becomes more complex.
        Visual style: clean, minimalist, soft colors.
        Controls: tap to select, swipe to move.
    ''',

    '''
        Create a 2D platformer game.

        Goal: reach the end of each level.
        Gameplay: jump between platforms, avoid enemies, collect coins.
        Player abilities: jump and move left/right.
        Lose condition: falling off the map or touching enemies.
        Visual style: pixel art.
        Difficulty: medium.
    ''',

    '''
        You are a game designer.
        Create a playable mobile game.

        Genre: casual arcade.
        Target audience: beginners.
        Main mechanic: simple but addictive.
        Game loop: play → score → retry.
        Controls: one-touch.
        Visuals: bright, friendly, minimal UI.
        Performance: optimized for mobile.
        Make the game easy to understand in 5 seconds.
    '''
]
OPENAI_API_KEY = getenv('OPENAI_API_KEY')
OPENAI_MODEL = getenv('OPENAI_MODEL')
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = getenv('AWS_REGION_NAME')
S3_BUCKET_NAME = getenv('S3_BUCKET_NAME')
RESOURCE_GAME_URL = getenv('RESOURCE_GAME_URL')
GAMES = [
    ('Color Dash', f'{RESOURCE_GAME_URL}/cc8de42d-46aa-4ffd-b6e1-eeb613dba414.html'),
    ('Tap Flyer', f'{RESOURCE_GAME_URL}/d5b5e201-d9f9-43d6-9c0f-e4055c15bc96.html'),
    ('Logic Blocks', f'{RESOURCE_GAME_URL}/490acc3c-42a2-4139-8ae2-37424a80f28f.html'),
    ('City of Voices: Interactive English & Russian learning adventure', f'{RESOURCE_GAME_URL}/41351c07-f6b2-491c-86a1-396922076a8a.html'),
    ('Kill Time Game', f'{RESOURCE_GAME_URL}/81aa4dbe-0524-4737-a033-db4761f83ab3.html')
]
PAGE_ICON_PATH = getenv('PAGE_ICON_PATH')
DOWNLOAD_GAME_URL = getenv('DOWNLOAD_GAME_URL')