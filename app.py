from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
import argparse
import sys
import time
import numpy as np
import tensorflow as tf

ALLOWED_EXTENSIONS = set(['jpeg'])
app = Flask(__name__)

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    
    return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
        input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    # only supporting .jpeg right now
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3, name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    return result

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

@app.route('/<path:path>', methods=["POST"])
def analyze_photo(path):
    """
    Take the input image.
    Return the model's analysis of the image.
    """

    # check if the post request has the file part
    if 'file' not in request.files:
        return BadRequest("File not present in request")
    file = request.files['file']
    if file.filename == '':
        return BadRequest("Filename is not present in request")
    if not allowed_file(file.filename):
        return BadRequest("Invalid file type")
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        print("Looking good so far")
        print(filename)

        input_filepath = os.path.join(filename)
        file.save(input_filepath)
        
        model_file="/model/output_graph.pb"
        label_file="/model/output_labels.txt"
        input_height = 299
        input_width = 299
        input_mean = 128
        input_std = 128

        graph = load_graph(model_file)
        t = read_tensor_from_image_file(input_filepath,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)

        input_layer = "Mul"
        output_layer = "final_result"
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name)
        output_operation = graph.get_operation_by_name(output_name)

        with tf.Session(graph=graph) as sess:
            start = time.time()
            results = sess.run(output_operation.outputs[0],
                              {input_operation.outputs[0]: t})
            end = time.time()
        
        results = np.squeeze(results)
        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)

        seconds = round(end-start, 3)
        print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

        resp = {}
        resp["seconds"] = seconds
        answer = {}
        for i in top_k:
            # print(labels[i], results[i])
            answer[labels[i]] = float(results[i])

        resp["answer"] = answer

        os.remove(input_filepath)

        response = jsonify(resp)
        response.status_code = 200
        return response

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0')