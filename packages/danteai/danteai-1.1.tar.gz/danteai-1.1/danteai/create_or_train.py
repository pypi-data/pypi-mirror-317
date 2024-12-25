from minions import (
    load_model,
    load_tokenizer,
    train_dataset,
    data_collator,
    train_args,
    trainer,
    model_store_dir
)

def create_or_train(*args, **kwargs) -> str:
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

    new_model = kwargs.get('create_new_model', False)
    data = kwargs.get('data', [])

    if not all(data):
        return 'The list with parameters for training is empty'

    model = load_model(new_model)
    tokenizer = load_tokenizer(new_model)

    if any((
        isinstance(model, None),
        isinstance(tokenizer, None),
    )):
        return '\'MODEL_STORE_DIR\' parameter is blank'
    
    train_dataset_response = train_dataset(data, tokenizer=tokenizer)
    if isinstance(train_dataset_response, str):
        return train_dataset_response
    
    train_args_response = train_args()

    data_collator_response = data_collator(
         model, tokenizer
    )
    
    trainer_response = trainer(
        model, 
        tokenizer,
        train_dataset_response,
        train_args_response,
        data_collator_response
    )

    trainer_response.train()

    model.save_pretrained(model_store_dir)
    tokenizer.save_pretrained(model_store_dir)

    return 'The model training has been completed successfully'