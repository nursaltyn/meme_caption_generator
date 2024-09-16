# meme_caption_generator

A program that generates memes based on the input image

# Welcome to the meme caption generator!

## Repository structure

The structure of this repo is as follows:

```
meme_caption_generator/
├── notebooks/ 
├── fonts/                             #fonts for meme captions
├── memes_900k_files/                  #files used for training
├── my_fun_results/                    #some of my results
├── test_images/                       #some templates you might want to use
├── utils/           
├── requirements.txt
├── run_your_meme.py                   #a script to get your meme
├── walk_through_notebook.ipynb        
└── README.md  
```

## About

In this project, I am using two different approaches to generate meme captions.

1. **Sentiment-based Caption Generation**

User input -> sentiment detection -> prompt LLaMA3-8B-Instruct with sentiment and in-context learning examples.

2. **Adapters imitating meme styles**
User input -> sentiment+context detection -> prompt Gemma-2B with customly trained adapters to generate specific genres/formats of memes.

Before you proceed with the code, I recommend having a look at the [project report](https://docs.google.com/document/d/1sfV_8dGUYDKhsDxamNgNgsKsxOrn2vAecXm-wvp5Uu0/edit) to get a higher-level overview of the whole pipeline.

## How to get your meme?

1. For testing the first approach, please refer to this [Colab notebook](https://colab.research.google.com/drive/1IoiNmQLWkTSiMJDY0q_XFAgYuwlzOVko?usp=sharing).
Please first make sure you have access to the [Drive folder](https://drive.google.com/drive/folders/1hLV_fUtwA_vmGImays2pMvvacc8xGqT_?usp=sharing), and then run the **Meme_caption_generator.ipynb** notebook. It will require:
- an access to mount your drive
- your HuggingFace API token

2. For testing the second approach:

1) Make sure you have:
- an access to [Gemma-2b model](https://huggingface.co/google/gemma-2-2b) - it is open-source
- a HuggingFace API token


2) Clone this repository to your Downloads folder: 
```
git clone https://github.com/nursaltyn/meme_caption_generator
```
You might download it in another folder, however, you might have to adjust some paths in some notebooks.
This inconvenience will be fixed in the future.

3) Please make sure you have installed the requirements to avoid compatibility problems:
```
requirements.txt
```

4) While you are in the "meme_caption_generator" folder, run:

```
python run_your_meme.py --img_path YOUR_FULL_IMAGE_PATH --hf_token hf_YOUR_TOKEN
```

- If you are not sure, which image to run, you can use "test_images" folder to get inspiration. Some templates are available there.
- FOR MAC users: add an argument --device mps when running the script:

```
python run_your_meme.py --img_path YOUR_FULL_IMAGE_PATH --hf_token hf_YOUR_TOKEN --device mps
```

5) By default, you will see the result meme in the folder "result_memes/gemma". If you want to receive memes in a different folder, you can path it in the optional argument "output_dir":   

```
python run_your_meme.py --img_path YOUR_FULL_IMAGE_PATH --hf_token hf_YOUR_TOKEN --output_dir YOUR_OUTPUT_PATH
```

## Web-application

You can also explore the web-interface on Streamlit. However, since we are using Gemma model under the hood, and Gemma requires a private API token (although still open-source), we weren't able to launch the application in public. However, you can clone it to your local machine, and run streamlit.

https://huggingface.co/spaces/NursNurs/Meme-caption-generator/tree/main

When you are in the Meme-caption-generator folder, run:

```
streamlit run app.py
```

## Potential errors you might get (but hopefully won't)

- Since we use Inference API for some HuggingFace models, there might be two potential errors:
   - The model isn't loaded yet (usually the first time you prompt it; later this error disappears)
   - You've reached the query limit (300 queries/hour). 
- In the requirement.txt, some libraries might be missing. We are working on fixing that and apologize for possible inconveniences.

## Other notes

In the fonts folder, you can load fonts which you want to use for meme generation. The default font we use is Anton.

For training the models, we used memes_900k dataset, which is available [here](https://drive.google.com/file/d/1j6YG3skamxA1-mdogC1kRjugFuOkHt_A/edit).


## Resources

- Dataset memes900k: Borovik, Ilya & Khabibullin, Bulat & Kniazev, Vladislav & Pichugin, Zakhar & Olaleke, Oluwafemi. (2020). DeepHumor: Image-Based Meme Generation Using Deep Learning. 10.13140/RG.2.2.14598.14400.
- https://huggingface.co/blog/gemma-peft (Gemma tuning)
- https://medium.com/@samvardhan777/fine-tune-gemma-using-qlora-%EF%B8%8F-6b2f2e76dc55 (Gemma tuning)
- https://colab.research.google.com/drive/1Ys44kVvmeZtnICzWz0xgpRnrIOjZAuxp?usp=sharing (running Llama efficiently with Unsloth library) 
