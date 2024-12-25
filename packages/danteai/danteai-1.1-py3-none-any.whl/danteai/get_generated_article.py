from minions import (
    generator
)

def get_generated_article(*args, **kwargs) -> str:
    data = (
        kwargs.get('tags', []),
        kwargs.get('text_example', ''),
        kwargs.get('short_news_description', ''),
    )

    if not all(data):
        return 'Insufficient parameters to execute the request'

    response = generator(data)
    return response