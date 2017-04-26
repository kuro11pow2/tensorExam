import tensorflow as tf
from random import randint

dims = 8
pos = randint(0, dims - 1)

logits = tf.random_uniform([dims], maxval=3, dtype=tf.float32)
labels = tf.one_hot(pos, dims)

print(labels, pos)
res1 = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels)
res2 = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=pos)

with tf.Session() as sess:
    a, b = sess.run([res1, res2])
    print(a, b)
    print(a == b)
