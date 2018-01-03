# cozmo-tensorflow
Cozmo the Robot does things with TensorFlow


## Setup

Install the [Cozmo SDK](http://cozmosdk.anki.com/docs/)
```bash
virtualenv ~/.env/cozmo -p python3
source ~/.env/cozmo/bin/activate
pip install -r requirements.txt
```


## Ask Cozmo to help generate a dataset

Let's ask Cozmo to take pictures of something, let's say a rock
```bash
python3 cozmo-paparazzi.py rock
```