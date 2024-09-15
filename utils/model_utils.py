import base64
import requests
import json
import pandas as pd
import os
from tqdm import tqdm
import re
import torch



def query_clip(data, hf_token):
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


def get_sentiment(img_path, hf_token):
    print("Getting the sentiment of the image...")
    output = query_clip({
        "image_path": img_path,
        "parameters": {"candidate_labels": ["angry", "happy"]},
    }, hf_token)
    try:
        print("Sentiment:", output[0]['label'])
        return output[0]['label']
    except:
        print(output)
        print("If the model is loading, try again in a minute. If you've reached a query limit (300 per hour), try within the next hour.")


def query_blip(filename, hf_token):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": f"Bearer {hf_token}"}
    with open(filename, "rb") as f:
        file = f.read()
    response = requests.post(API_URL, headers=headers, data=file)
    return response.json()


def get_description(img_path, hf_token):
    print("Getting the context of the image...")
    output = query_blip(img_path, hf_token)

    try:
        print("Context:", output[0]['generated_text'])
        return output[0]['generated_text']
    except:
        print(output)
        print("The model is not available right now due to query limits. Try running again now or within the next hour")


def get_model_caption(img_path, base_model, tokenizer, hf_token, device='cuda'):
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