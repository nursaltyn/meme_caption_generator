# %%
import base64
import requests
import json
import os
import re
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse

from utils.model_utils import get_model_caption
from utils.image_utils import overlay_caption


def generate_meme_from_image(img_path, base_model, tokenizer, hf_token, output_dir, device='cuda'):
  caption = get_model_caption(img_path, base_model, tokenizer, hf_token)
  image = overlay_caption(caption, img_path, output_dir)
  return image, caption
  
base_model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model_angry = PeftModel.from_pretrained(base_model, "NursNurs/outputs_gemma2b_angry")
model_happy = PeftModel.from_pretrained(base_model, "NursNurs/outputs_gemma2b_happy")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
base_model.to(device)
model_happy.to(device)
model_angry.to(device)

base_model.load_adapter("NursNurs/outputs_gemma2b_happy", "happy")  
base_model.load_adapter("NursNurs/outputs_gemma2b_angry", "angry")  

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", required=True) 
    parser.add_argument("--hf_token", required=True)
    # parser.add_argument("--force_mood", type=str, help='["happy", "angry"]', required=False) # if you want to generate specific mood of memes
    parser.add_argument("--output_dir", required=False, default= r'result_memes/gemma')
    
    args = parser.parse_args()

    hf_token = args.hf_token
    
    if "\\" in args.img_path:
        args.img_path = args.img_path.replace("\\", "/")

    image, caption = generate_meme_from_image(args.img_path, 
                                              base_model, 
                                              tokenizer, 
                                              args.hf_token,
                                              args.output_dir, 
                                              device=device)
    image.show()
   
