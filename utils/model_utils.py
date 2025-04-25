import os
import re
import torch
import json
import base64
import requests
import pandas as pd
from tqdm import tqdm


def query_clip(data, hf_token):
    """
    Query the CLIP model to get the image sentiment.
    Args:
        data (dict): A dictionary containing the image path and parameters.
    Returns:
        dict: The sentiment from the CLIP model.
    """ 
    API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
    headers = {"Authorization": f"Bearer {hf_token}"}
    with open(data["image_path"], "rb") as f:
        img = f.read()
    payload={
		"parameters": data["parameters"],
		"inputs": base64.b64encode(img).decode("utf-8")
	}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_sentiment(img_path, hf_token, candidate_labels=["angry", "happy"]):
    """
    Get the sentiment of the image using the CLIP model.
    Args:
        img_path (str): The path to the image.
        hf_token (str): The Hugging Face token for authentication.
        candidate_labels (list): The candidate labels for sentiment analysis.
    Returns:
        str: The sentiment of the image.    
    """
    print("Getting the sentiment of the image...")
    output = query_clip({
        "image_path": img_path,
        "parameters": {"candidate_labels": candidate_labels},
    }, hf_token)
    try:
        print("Sentiment:", output[0]['label'])
        return output[0]['label']
    except:
        print(output)
        print("If the model is loading, try again in a minute. If you've reached a query limit (300 per hour), try within the next hour.")


def query_blip(filename, hf_token):
    """
    Query the BLIP model to get the image caption.
    Args:
        filename (str): The path to the image file.
    Returns:
        dict: The caption from the BLIP model.
    """
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": f"Bearer {hf_token}"}
    with open(filename, "rb") as f:
        file = f.read()
    response = requests.post(API_URL, headers=headers, data=file)
    return response.json()


def get_description(img_path, hf_token):
    """
    Get the description of the image using the BLIP model.
    Args:
        img_path (str): The path to the image.
        hf_token (str): The Hugging Face token for authentication.
    Returns:
        str: The description of the image.
    """
    print("Getting the context of the image...")
    output = query_blip(img_path, hf_token)

    try:
        print("Context:", output[0]['generated_text'])
        return output[0]['generated_text']
    except:
        print(output)
        print("The model is not available right now due to query limits. Try running again now or within the next hour")


def get_model_caption(img_path, base_model, tokenizer, hf_token, device='cpu'):
    """Generate a meme caption based on the image sentiment and description.
    Args:
        img_path (str): The path to the image.
        base_model (transformers.PreTrainedModel): The base model for caption generation.
        tokenizer (transformers.PreTrainedTokenizer): The tokenizer for the model.
        hf_token (str): The Hugging Face token for authentication.
        device (str): The device to run the model on ('cpu','cuda','mps').
    Returns:
        str: The generated meme caption.
    """
    print("Getting the sentiment and context of the image... Device:", device)

    sentiment = get_sentiment(img_path, hf_token)
    description = get_description(img_path, hf_token)
    
    prompt_template = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request.\\n\\n
    You are given a topic. Your task is to generate a meme caption based on the topic. Only output the meme caption and nothing more.
    Topic: {query}
    <end_of_turn>\\n<start_of_turn>model Caption:
    """
    prompt = prompt_template.format(query=description)
    
    print("Generating captions...")
    encodeds = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)
    model_inputs = encodeds.to(device)
    base_model.set_adapter(sentiment)
    base_model.to(device)
    generated_ids = base_model.generate(**model_inputs, max_new_tokens=20, do_sample=True, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return (decoded)