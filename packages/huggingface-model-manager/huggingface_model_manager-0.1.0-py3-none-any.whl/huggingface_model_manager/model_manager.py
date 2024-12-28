from transformers import AutoTokenizer, AutoModel, pipeline

DEFAULT_MODEL_NAME = "distilbert-base-uncased"

def save_model(model, tokenizer, save_path):
    """
    Save a model and tokenizer to a specified path.
    
    Args:
        model: The Hugging Face model to save.
        tokenizer: The tokenizer to save.
        save_path: The path to save the model and tokenizer.
    """
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

def load_model(model_path=None):
    """
    Load a model and tokenizer from a specified path or use a default model.
    
    Args:
        model_path: The path to the model directory. If None, load the default model.
    
    Returns:
        model: The loaded Hugging Face model.
        tokenizer: The loaded tokenizer.
    """
    if model_path:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModel.from_pretrained(model_path)
    else:
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL_NAME)
        model = AutoModel.from_pretrained(DEFAULT_MODEL_NAME)
    
    return model, tokenizer

def use_pipeline(task, model_path=None):
    """
    Use a Hugging Face pipeline for a specific task with a model loaded from a specified path or use a default model.
    
    Args:
        task: The task for the pipeline (e.g., "automatic-speech-recognition", "text-classification").
        model_path: The path to the model directory. If None, use the default model.
    
    Returns:
        pipe: The Hugging Face pipeline.
    """
    if model_path:
        pipe = pipeline(task, model=model_path)
    else:
        pipe = pipeline(task, model=DEFAULT_MODEL_NAME)
    return pipe