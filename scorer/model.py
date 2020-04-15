# Base code by the github user kamalkraj
# available at https://github.com/kamalkraj/Tensorflow-Paper-Implementation
# this is an implementation of Lenet http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf
# The basic idea to combine three classifiers, one for each view, was extracted from Zhu et al. https://www.sfu.ca/~cza68/papers/zhu_sig17_scsr.pdf

import numpy as np
import tensorflow.compat.v1 as tf
from chair_dataset import ChairDataset
import os

tf.logging.set_verbosity(tf.logging.INFO)

def cnn_model_fn(features, labels, mode, params):
    # Input layer, change 56 to whatever the dimensions of the input images are
    dimension = params['dimension']
    input_layer = tf.reshape(features['x'], [-1, dimension, dimension, 1])

    # Conv Layer #1
    conv1 = tf.layers.conv2d(inputs=input_layer, filters=32, kernel_size=[5, 5], padding='same', activation=tf.nn.relu)

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Conv Layer #2
    conv2 = tf.layers.conv2d(inputs=pool1, filters=64, kernel_size=[5, 5], padding='same', activation=tf.nn.relu)

    # Pooling Layer #2
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 14 * 14 * 64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=2)

    predictions = {"classes": tf.argmax(input=logits, axis=1),
                "probabilities": tf.nn.softmax(logits, name="softmax_tensor")}

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    eval_metrics_ops = {"accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}

    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metrics_ops)


def train(dimension, images, labels, model_output_dir):
    #how many samples will be part of the train slice, the rest will be test data
    train_slice = 0.8

    imagesTop = images[0]
    imagesFront = images[1]
    imagesLeft = images[2]
    imagesRight = images[3]
    
    labelsTop = labels[0]
    labelsFront = labels[1]
    labelsLeft = labels[2]
    labelsRight = labels[3]
    

    #first we calculate the ID that will split the dataset between training samples and test samples
    dataset_length = len(imagesTop)
    sliceId = int(dataset_length * train_slice)

    train_images = []
    train_labels = []
    #we get the train images and labels
    train_images.append(imagesTop[:sliceId])
    train_images.append(imagesFront[:sliceId])
    train_images.append(imagesLeft[:sliceId])
    train_images.append(imagesRight[:sliceId])

    train_labels.append(labelsTop[:sliceId])
    train_labels.append(labelsFront[:sliceId])
    train_labels.append(labelsLeft[:sliceId])
    train_labels.append(labelsRight[:sliceId])

    test_images = []
    test_labels = []
    #then the rest are test images and labels
    test_images.append(imagesTop[sliceId:])
    test_images.append(imagesFront[sliceId:])
    test_images.append(imagesLeft[sliceId:])
    test_images.append(imagesRight[sliceId:])

    test_labels.append(labelsTop[sliceId:])
    test_labels.append(labelsFront[sliceId:])
    test_labels.append(labelsLeft[sliceId:])
    test_labels.append(labelsRight[sliceId:])

    train_images = np.array(train_images)
    train_labels = np.array(train_labels)
    test_images = np.array(test_images)
    test_labels = np.array(test_labels)


    test_evaluations = [[],[],[]]

    for view in ["Top","Front","Left", "Right"]:
        id = ["Top", "Front", "Left", "Right"].index(view)

        model_dir = os.path.join(model_output_dir, view)

        classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir=model_dir, params={'dimension': dimension})

        tensors_to_log = {"probabilities": "softmax_tensor"}

        train_input_fn = tf.estimator.inputs.numpy_input_fn( x={"x": train_images[id]},
                                                            y=train_labels[id],
                                                            batch_size=100,
                                                            num_epochs=None,
                                                            shuffle=True)

        logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

        classifier.train(input_fn=train_input_fn, steps=10000) #, hooks=[logging_hook])

        eval_input_fn = tf.estimator.inputs.numpy_input_fn( x={"x": test_images[id]},
                                                            y=test_labels[id],
                                                            num_epochs=1,
                                                            shuffle=False)
        eval_results = classifier.evaluate(input_fn=eval_input_fn)
        print(eval_results)


