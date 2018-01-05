# cozmo-tensorflow
Cozmo the Robot learns to recognize everyday objects using TensorFlow and FloydHub.

![finder](assets/cozmo-detective.gif)

## The setup

Install the [Cozmo SDK](http://cozmosdk.anki.com/docs/)
```bash
virtualenv ~/.env/cozmo -p python3
source ~/.env/cozmo/bin/activate
git clone https://www.github.com/whatrocks/cozmo-tensorflow
cd cozmo-tensorflow
pip install -r requirements.txt
```

Login to FloydHub CLI (sign up for a [free account here](https://www.floydhub.com/plans))
```bash
floyd login
```

## 1. Use Cozmo to generate training data

Getting enough training data for a deep learning project is often a pain. But thankfully we have a robot who loves to run around and take photos with his camera, so let's just ask Cozmo to take pictures of things we want him to learn. Let's start with a can of delicious overpriced seltzer. Place Cozmo directly in front of a bottle of seltzer, and make sure that he has enough space to rotate around the can to take some pictures. Be sure to enter the name of the object that Cozmo is photographing when you run the `cozmo-paparazzi` script.
```bash
python3 cozmo-paparazzi.py seltzer
```

![CozmoPaparazzi](assets/cozmo-paparazzi.gif)

Repeat that step for as many objects (categories) as you want Cozmo to learn! You should now see all your image categories as subdirectories within the `/data` folder.

### Uploading dataset to FloydHub

Now, let's upload our images to [FloydHub](https://www.floydhub.com/whatrocks/datasets/cozmo-images) as a FloydHub Dataset so that we can use them throughout our various model training and model servicing jobs.

```bash
cd data
floyd data init cozmo-images
floyd data upload
```

## 2. Training our model on FloydHub

Make sure you are in our project's root directory, and then initialize a FloydHub project so that we can train our model on a fully-configured TensorFlow cloud GPU machine.
```bash
floyd init cozmo-tensorflow
```

Now we can kick off a deep learning training job on FloydHub. Couple things to note:

* We're mounting the dataset that Cozmo created with the `--data` flag at the `/data` directory on our FloydHub machine.
* I've edited this script (initially provided by the TensorFlow team) to write its output to the `/output` directory. This is important when you're using FloydHub, because FloydHub jobs always store their outputs in the `/output` directory). In our case, we'll be saving our retrained ImageNet model and the training labels to the `/output` folder.

```bash
floyd run \
  --gpu \
  --data whatrocks/datasets/cozmo-images:data \
  'python retrain.py --image_dir /data'
```

That's it! There's no need to configure anything on AWS or install TensorFlow or deal with GPU drivers or anything like that. 

Once your job is complete, you'll be able to see your newly retrained model in [the job's output directory](https://www.floydhub.com/whatrocks/projects/cozmo-tensorflow/8/output). 

I recommend converting your job's output into a standalone FloydHub Dataset to make it easier for you to mount it in future jobs (which we're going to be doing in the next step). You can do this by clicking the 'Create Dataset' button on the job's output page.

## 3. Connecting Cozmo to our trained model on FloydHub

We can test our newly retrained model by running another job on FloydHub that mounts (1) our trained model and (2) our images dataset, and uses the `label_image` script.
```bash
floyd run \
  --gpu \
  --data whatrocks/datasets/cozmo-imagenet:model \
  --data whatrocks/datasets/cozmo-images:data \
  'python label_image.py --graph=/model/output_graph.pb --image=/data/toothpaste/toothpaste-329.jpeg --labels=/model/output_labels.txt'
```

## 4. Testing our model on Cozmo

Coming soon!

## References

This project is an extension of @nheidloff's [Cozmo visual recognition project](https://github.com/nheidloff/visual-recognition-for-cozmo-with-tensorflow) and the [Google Code Labs TensorFlow for Poets project](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0).