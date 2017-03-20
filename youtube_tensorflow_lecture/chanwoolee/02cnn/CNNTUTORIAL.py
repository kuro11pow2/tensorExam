import tensorflow as tf
import os
from PIL import Image

IMAGE_WIDTH = 49
IMAGE_HEIGHT = 61

image_dir = os.getcwd() + './Face00003.png'
filename_list = [image_dir]

filename_queue = tf.train.string_input_producer(filename_list)

reader = tf.WholeFileReader()
key, value = reader.read(filename_queue)

x = tf.placeholder(tf.float32, shape=[None, IMAGE_WIDTH, IMAGE_HEIGHT])
y_ = tf.placeholder(tf.float32, shape=[None, 1])

W_hidden1 = tf.Variable(tf.truncated_normal([5, 5, 1, 32]))
B_hidden1 = tf.Variable(tf.zeros(32))

x_image = tf.reshape(x, [-1, IMAGE_WIDTH, IMAGE_HEIGHT, 1])
conv1 = tf.nn.conv2d(x_image, W_hidden1, strides=[1, 1, 1, 1], padding='SAME')
hidden1 = tf.nn.relu(conv1 + B_hidden1)

W_hidden2 = tf.Variable(tf.truncated_normal([5,5,32,64]))  #64개쓸거다.
B_hidden2 = tf.Variable(tf.truncated_normal([64]))

conv2 = tf.nn.conv2d(hidden1, W_hidden2, strides=[1,1,1,1], padding='SAME')
hidden2 = tf.nn.relu(conv2)

image_decoded = tf.image.decode_png(value)

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    img = sess.run(image_decoded)
    print(img)

    coord.request_stop()
    coord.join(threads)
