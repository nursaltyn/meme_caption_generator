# meme_caption_generator

A program that generates memes based on the input image

Welcome to the meme caption generator!

## Repository structure

The structure of this repo is as follows:

my-project/ ├── data/ │ ├── raw/ │ └── processed/ ├── notebooks/ ├── scripts/ └── README.md

my-project/
├── data/
│ ├── raw/
│ │ └── README.md
│ ├── processed/
│ │ └── README.md
├── notebooks/
│ └── README.md
├── scripts/
│ └── README.md
└── README.md

meme_caption_generator/
├── experiments/
│ ├── raw/
│ └── processed/
├── fonts/
├── memes_900k_files/
├── my_fun_results/
├── test_images/
├── utils/
├── requirements.txt
├── run_your_meme.py
├── walk_through_notebook.ipynb
└── README.md

In the experiments folder, there
In the fonts folder, you can load fonts which you want to use for meme generation. The default font we use is Anton.

For training the models, we used memes_900k dataset, which is available here: {link}

## Methods

In this project, I am using two different approaches to generate meme captions.

1.

I noti

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
   Thus, my first approach was to detect the sentiment using a vision-language model. CLIP-base model performed well on this task zero-shot: https://huggingface.co/openai/clip-vit-base-patch32

   I choose 10 labels for different emotions (because of limitations of possible label input in this CLIP version).

Choice of labels:
American psychologist Paul Ekman identified six basic emotions: anger, disgust, fear, happiness, sadness and surprise.
For the labels, I chose the following:
Wallace V. Friesen and Phoebe C. Ellsworth worked with him on the same basic structure.[37] The emotions can be linked to facial expressions

Maybe can use it if we have templates already, find a similar template and produce a similar joke, but this seems not very useful and too rule based.
In the meme dataset I used, there were different languages mixed, so need to stick to english.
Open ended generation seems difficult - a large search space of topics.
Also many formars of the memes: POV, Me when, This feeling when, Nobody: , etc…

Another challenge is that memes are often expressions of stances, especially those that don’t make sense without a text.
