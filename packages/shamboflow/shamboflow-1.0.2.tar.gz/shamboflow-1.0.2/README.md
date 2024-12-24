<div align="center">
    <img src="https://files.catbox.moe/j06xze.png">
</div>

![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-white?style=for-the-badge&labelColor=gray&color=blue)
[![PyPI - Version](https://img.shields.io/pypi/v/shamboflow?style=for-the-badge&link=https%3A%2F%2Fpypi.org%2Fproject%2Fshamboflow%2F)](https://pypi.org/project/shamboflow/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ShambaC/shamboflow/python-publish.yml?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/ShambaC/shamboflow?display_date=published_at&style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/shamboflow?style=for-the-badge&color=black)


> [!IMPORTANT]
> This is an elaborate meme I put a lot of effort into.
> So please, no one sue me.

ShamboFlow is an open source API for creating machine learning models. It is only available in python.

ShamboFlow is super fast drop in replacemnet for TensorFlow (Read adds nothing, not even performance improvement). It is build from scratch (Read, using numpy) and comes with Cuda GPU support out of the box. I will tell the story at the end of this file on how this came to be. 

On a serious note, I always wanted to implement a neural network using just numpy and no additional libraries and this gave me an excuse to do so. And so I did. I made this in a week. Learned a lot of stuff in the process and it was a stressfull and fun experience. This library is dependent on numpy as stated but also uses cupy to add GPU support. Other two dependencies are tqdm for progress bar and colorama for colorful texts. I will probably work more on this as I have already put in quite some effort.

# Documentation
[![Static Badge](https://img.shields.io/badge/API-docs-black?style=for-the-badge)](https://shambac.github.io/shamboflow/)

[![Static Badge](https://img.shields.io/badge/Guide-In_Progress-black?style=for-the-badge)](https://pingutinguorg.gitbook.io/shamboflow)

# Install

Install using the pip package.
```bash
$ pip install shamboflow
```

To update ShamboFlow to the latest version, add `--upgrade` flag to the above command

# Example

A small example program that shows how to create a simple ANN with 3-2-1 topology and train it with data to perform predictions.

## Define the model and train it

```python
import numpy as np

# Dataset
x_data = np.array([[1, 0, 1]])
y_data = np.array([[1]])

# Parameters
learning_rate = 0.9
train_epochs = 20

# Import the library
import shamboflow as sf

# Create a model
model = sf.models.Sequential()
# Add layers
model.add(sf.layers.Dense(3))
model.add(sf.layers.Dense(2, activation='sigmoid'))
model.add(sf.layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(learning_rate=learning_rate, loss='mean_squared_error', verbose=True)

# Callbacks
checkpoint = sf.callbacks.ModelCheckpoint(monitor='loss', save_best_only=True, verbose=True)

# Train the model with the dataset
model.fit(
    x_data,
    y_data,
    epochs=train_epochs,
    callbacks=[checkpoint]
)

# Save the trained model to disk
model.save('model.meow')
```

## Load the saved model and predict
```python
import numpy as np
import shamboflow as sf

model = sf.models.load_model("./model.meow")

a = np.array([[1, 0, 1]])

res = model.predict(a)
print(res)
```

# Story
Its storytime.

Last week we had a class on Neural Networks at university. At the end of the class, our professor told us to implement the given network in python. Now, previously he had told us to not use any libraries to perform our tasks as that would just ruin the purpose of learning algorithms. So, I got excited that I am gonna implement a neural network using just python. Then he told us that we can use libraries for making the network. And I was a little bummed. My [friend](https://github.com/Shreyashi07) jokingly told me that, "No you have to make it". And I said, if I finish it within a week, will you use it in the assignment. My friends agreed to it.

So, here it is. My library. I am so gonna make them use this for the assignments.
