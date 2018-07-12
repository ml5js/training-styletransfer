# Style Transfer training and using the model in ml5js

This repository contains a slightly modified version of [Fast Style Transfer in TensorFlow](https://github.com/lengstrom/fast-style-transfer). It trains a neural network on the style of any image you provide it and outputs a model you can use in [ml5.js](https://ml5js.org/) with the [ml5.styleTransfer()](https://ml5js.org/docs/StyleTransfer) method.

**Notes**: 
- **[Here]()** is a blog post describing how to train your own custom style with [Paperspace](https://www.paperspace.com/). **This is the easiest way to get up and running without installing dependencies and libraries.**
- You should train your network using a GPU. Just using CPU will result in training times of [several months](https://github.com/lengstrom/fast-style-transfer/issues/92) :calendar:
- Training requires access to the [COCO Dataset](http://cocodataset.org/#home). COCO is a large-scale object detection, segmentation, and captioning dataset. The version of the dataset we will be using is about 14GB in total. The docker image will download and unzip it.

## Requirements

- Set up a python environment with tensorflow installed. [More detailed instructions here](https://ml5js.org/docs/training-setup). 

- If you are familiar with Docker, you can use this [container](https://hub.docker.com/r/cvalenzuelab/styletransfer/) that comes preinstalled with everything you need.


## Usage

### 1) Download this repository

Start by [downloading](https://github.com/ml5js/training_styletransfer/archive/master.zip) or cloning this repository:

```bash
git clone https://github.com/ml5js/training_styletransfer.git
cd training_styletransfer
```

### 2) Install dependencies and get the training data

This step is required only if you are running this **without** the Docker image. You will need to get the complete [COCO Dataset](http://cocodataset.org/#home), about 14GB of data. This is a requirement for training. You can download the data by running:

```
bash setup.sh
```

You will also need to install specific dependencies for this project:

```
pip install -r requirements.txt
```

### 3) Select a style image

Put the image you want to train the style on, in the `/images` folder.

### 4) Start the training

To train a new style transfer network you can use open the `run.sh` script, modified the `--style` argument to point to your image and run:

```bash
bash run.sh
```

Or run the training code directly:

```
python style.py --style images/YOURIMAGE.jpg \
  --checkpoint-dir checkpoints/ \
  --model-dir models/ \
  --test images/violetaparra.jpg \
  --test-dir tests/ \
  --content-weight 1.5e1 \
  --checkpoint-iterations 1000 \
  --batch-size 20
```

`--style` should point to the image you want to use. `--model-dir` will be the folder where the ml5.js model will be saved.

You can learn more about how to use all the parameters for training in the on the original repository for this code [here](https://github.com/lengstrom/fast-style-transfer#documentation) and [here](https://github.com/lengstrom/fast-style-transfer/blob/master/docs.md).

Once the training setup is ready, you should see something like this:

```
ml5.js Style Transfer Training!
Note: This traning will take a couple of hours.
Training is starting!...
Train set has been trimmed slightly..
(1, 451, 670, 3)
UID: 56
Epoch 0, Iteration: 1000, Loss: 1.75362e+07
style: 5.5727e+06, content:1.15116e+07, tv: 451984.0
...
Training complete. For evaluation:
    `python evaluate.py --checkpoint checkpoints/ ...`
Converting model to ml5js
Writing manifest to models/manifest.json
Done! Checkpoint saved. Visit https://ml5js.org/docs/StyleTransfer for more informationlive
```

### 5) Use it!

Once the model is ready, your model will be in the `models/` folder. You will just need to point to it in your ml5 sketch:

```javascript
const style = new ml5.styleTransfer('./models/your_new_model');
```

Check [ml5.js documentation](https://ml5js.org/docs/StyleTransfer) on the `styleTransfer()` method or the [style transfer simple example](https://ml5js.org/docs/style-transfer-image-example).