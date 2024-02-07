import tensorflow as tf

# Assuming tensor is your 3D TensorFlow tensor with shape (2, 3, 3)
tensor = tf.constant([[[0, 1, 2],
                       [3, 0, 4],
                       [0, 5, 0]],
                      [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]], dtype=tf.float32)

# Check if all elements along axis-0 are zero
mask = tf.reduce_all(tf.equal(tensor, 0), axis=0)
mask = tf.equal(mask, False)
# Convert True values to 0 and False values to 1
mask = tf.cast(mask, dtype=tensor.dtype)
print(mask)
