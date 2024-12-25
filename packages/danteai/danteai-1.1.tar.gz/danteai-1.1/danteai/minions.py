from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer
)

from datasets import Dataset
from os import getenv
from os.path import exists

global model_store_dir 
model_store_dir = getenv('MODEL_STORE_DIR', './model')

def if_model_store_dir_exists() -> bool:
    return exists(model_store_dir)

def load_model(new_model: bool = False):
    if new_model:
        return T5ForConditionalGeneration.from_pretrained('google/mt5-xxl').to('cpu')

    if not new_model and if_model_store_dir_exists():
        return T5ForConditionalGeneration.from_pretrained(model_store_dir).to('cpu')
    
    return None

def load_tokenizer(new_model: bool = False):
    if new_model:
        return T5Tokenizer.from_pretrained('google/mt5-xxl')

    if not new_model and if_model_store_dir_exists():
        return T5Tokenizer.from_pretrained(model_store_dir)
    
    return None

def trainer(*args):
    model, tokenizer, train_dataset, train_args, data_collator = args
    return Trainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        data_collator=data_collator,
        train_args=train_args
    )

def train_args():
    return TrainingArguments(
        output_dir='./settings',
        per_device_train_batch_size=4,
        num_train_epochs=3
    )

def data_collator(*args):
    model, tokenizer = args
    return DataCollatorForSeq2Seq(
        model=model,
        tokenizer=tokenizer
    )

def train_dataset(data: list, **kwargs) -> list:
    tokenizer = kwargs.get('tokenizer')
    if not tokenizer:
        return 'Tokenizer is NULL'
    
    prepared_data = [
        {
            'input_id': tokenizer(
                f"Tags: {', '.join(item.get('tags', []))}. Text example: \'{item.get('text_example', '')}\'. Short news description: \'{item.get('short_news_description', '')}\'",
                padding=True,
                truncation=True,
                return_tensors='pt'
            ),
            'label': tokenizer(
                f"{item.get('response', '')}",
                padding=True,
                truncation=True,
                return_tensors='pt'
            )
        }

        for item in data if 
        all((value for value in item.values()))
    ]

    if not prepared_data:
        return 'There are no prepared data'
    
    return Dataset.from_dict({
        'input_ids': [item['input_id'] for item in prepared_data],
        'label': [item['labels'] for item in prepared_data],
    })

def generator(*args) -> str:
    if not if_model_store_dir_exists():
        return 'Model not exists'

    model, tokenizer, tags, text_example, short_news_description = args
    input = f"Tags: {', '.join(tags)}. Text example: \'{text_example}\'. Short news description: \'{short_news_description}\'"
    inputs = tokenizer(input, padding=True, truncation=True, return_tensors='pt').to(model.device)
    output, *_ = model.generate(inputs['input_ids'], max_new_tokens=5000)
    response = tokenizer.decode(output, skip_special_tokens=True)

    return response