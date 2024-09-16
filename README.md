# meme_caption_generator

A program that generates memes based on the input image

Welcome to the meme caption generator!

## Repository structure

The structure of this repo is as follows:

```
meme_caption_generator/
├── experiments/
├── fonts/
├── memes_900k_files/
├── my_fun_results/
├── test_images/
├── utils/
├── requirements.txt
├── run_your_meme.py
├── walk_through_notebook.ipynb
└── README.md
```

## About

In this project, I am using two different approaches to generate meme captions.

1. User input -> sentiment detection -> prompt LLaMA3-8B-Instruct with sentiment and in-context learning examples.
2. User input -> sentiment+context detection -> prompt Gemma-2B with customly trained adapters to generate specific genres/formats of memes.

## How to get your meme?

1. For testing the first approach, please refer to this [Colab notebook](https://colab.research.google.com/drive/1IoiNmQLWkTSiMJDY0q_XFAgYuwlzOVko?usp=sharing).
Please first make sure you have access to the [Drive folder](https://drive.google.com/drive/folders/1hLV_fUtwA_vmGImays2pMvvacc8xGqT_?usp=sharing), and then run the **Meme_caption_generator.ipynb** notebook. It will require:
- an access to mount your drive
- your HuggingFace API token

2. For testing the second approach:

1) Clone this repository to your Downloads folder: 
```
git clone https://github.com/nursaltyn/meme_caption_generator
```
You might download it in another folder, however, you might have to adjust some paths in some notebooks.
This inconvenience will be fixed in the future.

2) While you are in the "meme_caption_generator" folder, run:

```
python run_your_meme.py --img_path YOUR_FULL_IMAGE_PATH --hf_token hf_YOUR_TOKEN
```

If you are not sure, which image to run, you can use "test_images" folder to get inspiration. Some templates are available there.



In the experiments folder, there
In the fonts folder, you can load fonts which you want to use for meme generation. The default font we use is Anton.

For training the models, we used memes_900k dataset, which is available here: {link}

Gemma2B turned out to be a good compromise between size and performance. 
With relatively few samples (300 to 500), I was able to train adapters. 

Other models were also tried for the purpose of caption generation (e.g., FLAN-T5 family - large, XL, and XXL; ...), but they didn't achieve reliable performance neither before training nor after. Notebooks with prefix-tuning of FLAN-T5 are added in the folder.

## Explanation of the first approach.

Sometimes the meme captions were too specific to the image
E.g. the Disaster girl next to the burning house
"boxes": [
"THE LETTERS",
"",
"ELIZA:"
]

# Prerequisits

Note: for some models we will be using Inference API from Hugging Face to save space and time for running this code.
Inference API requires a hugging face token.

I realized using only emotions is not always good since
classifier is limited
the context is important. E.g. if there is a doctor in the topic, maybe a meme should be about pain, doctors, or some medical content. If it is office, then about work, etc. Otherwise the model is blind
Unexpected problem - how to extract captions? the model does somewhat arbitrary format. Maybe experiment with the temperature
If extraction of the text from the model’s answer is empty, return some template or sth

## Some issues faced and solution

1. One feature is that different memes have different themes of jokes, different format (where the text is placed), specific word order etc. E.g.

2. Dataset selection: while several meme datasets are available online, not all of them are suitable for our task.
   Sometimes the meme captions are too specific to the image.
   E.g. the Disaster girl next to the burning house
   "boxes": [
   "THE LETTERS",
   "",
   "ELIZA:"
   ]

Some memes are self-content, they don’t need a text. We are talking specifically about the category of memes that are IWT so without text the image doesn’t make sense. Hence many datasets didn’t suit the task. https://ojs.aaai.org/index.php/ICWSM/article/view/7287/7141
E.g. this doesn’t suit https://www.kaggle.com/datasets/sayangoswami/reddit-memes-dataset

3. Another feature: the memes often have nothing to do with the background. Therefore, descriptions of the images might be not very helpful, or very vaguely. For example, a picture of a dog smiling might have tons of different captions - which have nothing to do with the dog itself. But what matters is the fact that it is a very positive picture, and this "vibe" can be exploited in describing many different situations.

For example, if the caption is: "POV: your face when you got your dream internship", it doesn't really matter if there is a smiling person on the image, or a smiling dog, or a smiling frog.

Thus, my first approach was to detect the sentiment using a vision-language model. CLIP-base model performed well on this task zero-shot: https://huggingface.co/openai/clip-vit-base-patch32

I choose 10 labels for different emotions (because of limitations of possible label input in this CLIP version).

Choice of labels:
American psychologist Paul Ekman identified six basic emotions: anger, disgust, fear, happiness, sadness and surprise.
For the labels, I chose the following:
Wallace V. Friesen and Phoebe C. Ellsworth worked with him on the same basic structure.[37] The emotions can be linked to facial expressions

4. After choosing sentiments, I manually provide 10 examples of meme captions for each sentiment. This is necessary as there is no dataset available with a fine-grained labeled sentiments of memes (or labels are not the same as we want).

   This way, my model is able to do in-context learning. I choose open-source LLaMA-3-8B (instruction-tuned) due to its relatively small size and good balance between creativity and sticking to the in-context examples. However, any other bigger model can be utilized.

I choose to give captions in the same format: "POV: ..."
This is done to achieve a more predictable behavior of the model and make it easier to parse the model's output.

The expected outcome in this approach is that it can generalize well to different images.

## Second approach: training adapters

As you probably noticed, a shortcoming of the sentiment approach is that it doesn't care about details in the context. E.g., if you input an image of a smiling doctor or an image of a smiling dog, it might still produce the same caption (since the sentiment is "happy").

To address that, I introduce another approach: training adapters that learn specific genres of memes.

After looking through many datasets, I stopped at memes_900k. It contains 300 meme templates, each with 3000 captions available from different users.

I label each of 300 meme templates with a sentiment (using CLIP).
Then I focus only on two sentiments: "angry" and "happy" (purely because of time constraints).
Within the memes with these sentiments, I choose templates that

1. have the most recognizable form: This is done so that the model is able to learn the pattern better with fewer examples. Some meme captions differ too much from each other.
2. are not too image-specific;
3. don't require complex text overlay (e.g. "Me", )

For "angry" memes, I choose templates "Y U No" and "Y U So". They express rage or irritation at some situation.
For "happy" memes, I choose templates "If you know what I mean" and "tobey-maguire". They express happiness after doing or saying something sneaky.

Note: in my opinion, "angry" adapters perform better, since they had a more consistent template for every caption, while "happy" memes captions were more diverse.

After that, I want to teach the adapter to generate topic-specific captions. I want to create a dataset with topics as inputs and captions as outputs. The meme900k dataset provides captions, but not topics. Hence, I label topics for each caption using Llama-3-8B-Instruct Inference API. For each meme template, I manually label 10 random captions and provide them as examples to Llama.

I labeled around 600 samples for each sentiment type due to query limit == 300/hour in Inference API.

Then I train Gemma2B adapters with train-test split 80:20.

I am using a Gemma model with 2 billion parameters + customly trained adapters.

Gemma2B turned out to be a good compromise between size and performance. 
With relatively few samples (300 to 500), I was able to train adapters. 

Other models were also tried for the purpose of caption generation (e.g., FLAN-T5 family - large, XL, and XXL; ...), but they didn't achieve reliable performance neither before training nor after. Notebooks with prefix-tuning of FLAN-T5 are added in the folder.

Alternative approach could be simply taking hundreds/thousands of different templates, labeling their sentiments, then getting the image descriptions and passing to the model for training. However, this wouldn't fit in the time/resource constraints well, thus I do the bootstrapping.

### Handling noise

Memes900k dataset contained many captions in various languages, so I filtered only English captions using langdetect library.
Unfortunately, there were captions that were offensive and inappropriate. Some captions were filtered by Gemma, as it refused to process them, however, there is no guarantee it detected every possible offensive statement.
In production, I would do a safety-check for each caption training a classifier with high recall.

Open ended generation seems difficult - a large search space of topics.
Also many formars of the memes: POV, Me when, This feeling when, Nobody: , etc…

Another challenge is that memes are often expressions of stances, especially those that don’t make sense without a text.

### Limitations and future work

Add more adapters for different sentiments
Adapters for more templates - choose randomly - e.g. sad -> different templates

The free option has a limited rate of queries per hour, which is 300. In the more advanced setting (e.g. in production with more GPUs), a model can be stored locally to avoid this limitation.