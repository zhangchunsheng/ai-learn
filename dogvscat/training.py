import os
import numpy as np
import tensorflow as tf
import input_data
import model

N_CLASSES = 2
IMG_W = 30
IMG_H = 30
BATCH_SIZE = 16
CAPACITY = 2000
MAX_STEP = 15000 # with current parameters, it is suggested to use MAX_STEP>10k
learning_rate = 0.0001 # with current parameters, it is suggested to use learning rate<0.0001

def run_training():
    # with tf.Graph().as_default():
    train_dir = './data/train/'
    logs_train_dir = './logs/'

    train, train_label = input_data.get_files(train_dir);

    train_batch, train_label_batch = input_data.get_batch(train,
                                                          train_label,
                                                          IMG_W,
                                                          IMG_H,
                                                          BATCH_SIZE,
                                                          CAPACITY)
    train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
    train_loss = model.losses(train_logits, train_label_batch)
    train_op = model.training(train_loss, learning_rate)
    train__acc = model.evaluation(train_logits, train_label_batch)

    summary_op = tf.summary.merge_all()
    sess = tf.Session()
    train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph)
    saver = tf.train.Saver();

    sess.run(tf.global_variables_initializer());
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                break;
            _, tra_loss, tra_acc = sess.run([train_op, train_loss, train__acc])

            if step % 50 == 0:
                print('Step %d, train loss = %.2f, trainng accuracy = %.2f%%' % (step, tra_loss, tra_acc))
                summary_str = sess.run(summary_op)
                train_writer.add_summary(summary_str, step)

            if step % 2000 == 0 or (step + 1) == MAX_STEP:
                checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)
    except tf.errors.OutOfRangeError:
        print('Done traing -- epoch limit reached')
    finally:
        coord.request_stop()

    coord.join(threads)
    sess.close()

# run_training();

from PIL import Image
import matplotlib.pyplot as plt

def get_one_image(train):
    '''

    :param train:
    :return:
        array
    '''
    n = len(train)
    ind = np.random.randint(0, n)
    img_dir = train[ind]

    image = Image.open(dir)
    #plt.imshow(image)
    plt.imsave("/mnt/ai/git/ai-image-detection/data/test.png", image);
    image = image.resize([200, 200])
    image = np.array(image)
    return image

def evaluate_one_image():
    train_dir = "./data/train/"
    train, train_label = input_data.get_files(train_dir)
    image_array = get_one_image(train)

    with tf.Graph().as_default():
        BATCH_SIZE = 1
        N_CLASSES = 2

        image = tf.cast(image_array, tf.float32)
        image = tf.reshape(image, [1, 200, 200, 3])
        logit = model.inference(image, BATCH_SIZE, N_CLASSES)
        logit = tf.nn.softmax(logit)

        x = tf.placeholder(tf.float32, shape=[200, 200, 3])
        logs_train_dir = "./logs";
        saver = tf.train.Saver()

        with tf.Session() as sess:
            print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(logs_train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print("Loading success, global step is %s" % global_step)
            else:
                print("No checkpoint file found")

            prediction = sess.run(logit, feed_dict={x: image_array})
            max_index = np.argmax(prediction)
            if(max_index == 0):
                print("This is a cat with possibility %0.6f" % prediction[:,0])
            else:
                print("This is a dot with possibility %0.6f" % prediction[:,1])

evaluate_one_image();