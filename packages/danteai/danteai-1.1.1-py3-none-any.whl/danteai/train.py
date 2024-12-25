from minions import (
    train_dataset,
    data_collator,
    train_args,
    trainer,

    model_store_dir, model, tokenizer
)

def train(*args, **kwargs) -> str:
    """
        data = [
            {
                'tags': [],
                'text_example: '',
                'short_news_description: '',
                'response': ''
            },
            ...
        ]
    """
    data = kwargs.get('data', [])

    if not all(data):
        return 'The list with parameters for training is empty'
    
    train_dataset_response = train_dataset(data)
    if isinstance(train_dataset_response, str):
        return train_dataset_response
    
    train_args_response = train_args()

    data_collator_response = data_collator()
    
    trainer_response = trainer(
        train_dataset_response,
        train_args_response,
        data_collator_response
    )

    trainer_response.train()

    model.save_pretrained(model_store_dir)
    tokenizer.save_pretrained(model_store_dir)

    return 'The model training has been completed successfully'