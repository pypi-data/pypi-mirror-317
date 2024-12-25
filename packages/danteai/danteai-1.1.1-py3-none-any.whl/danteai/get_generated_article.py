from .minions import (
    generator,
    load_model,
    load_tokenizer
)

def get_generated_article(*args, **kwargs) -> str:
    data = (
        kwargs.get('tags', []),
        kwargs.get('text_example', ''),
        kwargs.get('short_news_description', ''),
    )

    if not all(data):
        return 'Insufficient parameters to execute the request'

    model = load_model()
    tokenizer = load_tokenizer()

    if not all((model, tokenizer)):
        return 'Model not exists'

    response = generator(model, tokenizer, *data)
    return response