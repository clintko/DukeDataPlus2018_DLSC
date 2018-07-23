import tensorflow as tf
import data_helper
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import math

def getData(filepath):
    data = data_helper.loadTSV(filepath)
    return data

def train(filepath, model_path, learning_rate, batch_size, epoch):
    # load data
    myMatrix = getData(filepath)
    input_length = myMatrix.shape[1]
    print(input_length)
    # start time
    start = time.time()

    # create model path if not existed
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    # open console
    console = open(model_path + 'train_console.txt', "w")

    # set layer neural numbers
    layer1_num = 256
    layer2_num = 100
    layer3_num = 10

    # set input
    x = tf.placeholder("float", shape=[None, input_length])

    # set weights and bias
    weights = setWeight(input_length, layer1_num, layer2_num, layer3_num)
    bias = setBias(input_length, layer1_num, layer2_num, layer3_num)

    # set up model
    latent_space = encoder(x, weights, bias)
    y_pred = decoder(latent_space, weights, bias)
    y_true = x

    # define loss function and optimizer
    loss = tf.reduce_mean(tf.pow(y_true - y_pred, 2))
    optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(loss)

    # initialize variable
    init = tf.global_variables_initializer()

    # set epoch num
    train_matrix = getTrainData(myMatrix)
    it_num = train_matrix.shape[0]//batch_size

    # set plot data
    plot_x = range(0, epoch)
    plot_loss = []

    # start training
    with tf.Session() as sess:
        sess.run(init)
        for _ in range(0, epoch):
            epoch_loss = 0
            for i in range(0, it_num):
                batch_x = train_matrix[(i * batch_size):((i + 1) * batch_size)]
                r, l = sess.run([optimizer, loss], feed_dict={x: batch_x})
                epoch_loss += l
            epoch_loss = epoch_loss / it_num
            if _ % 100 == 0:
                print("at epoch {} the loss is {}\n".format(_, epoch_loss))
                console.write("at epoch {} the loss is {}\n".format(_, epoch_loss))
            plot_loss.append(epoch_loss)

        # plot loss vs, epoch
        fig = plt.figure()
        plt.plot(plot_x, plot_loss, "r-")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.title("loss VS. epoch")
        fig.savefig(model_path + "loss_epoch.png")

        # save the model
        saver = tf.train.Saver()
        save_path = saver.save(sess, model_path + "model.ckpt")

        # test
        test_matrix = getTestData(myMatrix)
        l_test = sess.run(loss, feed_dict={x: test_matrix})
        print("After training, the test loss is {}\n".format(l_test))
        console.write("After training, the test loss is {}\n".format(l_test))
        console.write("The model is saved in path: %s\n" % save_path)

    # end time
    end = time.time()
    console.write("it takes {} minutes to train\n".format((end-start)/60))

def encoder(x, weights, bias):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   bias['encoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']),
                                   bias['encoder_b2']))
    # Encoder Hidden layer with sigmoid activation #3
    layer_3 = tf.nn.sigmoid(tf.add(tf.matmul(layer_2, weights['encoder_h3']),
                                   bias['encoder_b3']))

 #   layer_4 = tf.nn.sigmoid(tf.add(tf.matmul(layer_3, weights['encoder_h4']),
  #                                 bias['encoder_b4']))

    return layer_3

def decoder(x, weights, bias):
    # Encoder Hidden layer with sigmoid activation #1
   # layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
  #                                 bias['decoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h2']),
                                   bias['decoder_b2']))
    # Encoder Hidden layer with sigmoid activation #3
    layer_3 = tf.nn.sigmoid(tf.add(tf.matmul(layer_2, weights['decoder_h3']),
                                   bias['decoder_b3']))

    layer_4 = tf.nn.sigmoid(tf.add(tf.matmul(layer_3, weights['decoder_h4']),
                                   bias['decoder_b4']))

    return layer_4

def setWeight(input_length, layer1_num, layer2_num, layer3_num):
    return {
        "encoder_h1": tf.Variable(tf.random_normal([input_length, layer1_num])),
        "encoder_h2": tf.Variable(tf.random_normal([layer1_num, layer2_num])),
        "encoder_h3": tf.Variable(tf.random_normal([layer2_num, layer3_num])),
        "decoder_h2": tf.Variable(tf.random_normal([layer3_num, layer2_num])),
        "decoder_h3": tf.Variable(tf.random_normal([layer2_num, layer1_num])),
        "decoder_h4": tf.Variable(tf.random_normal([layer1_num, input_length]))
    }

def setBias(input_length, layer1_num, layer2_num, layer3_num):
    return {
        "encoder_b1": tf.Variable(tf.random_normal([layer1_num])),
        "encoder_b2": tf.Variable(tf.random_normal([layer2_num])),
        "encoder_b3": tf.Variable(tf.random_normal([layer3_num])),
        "decoder_b1": tf.Variable(tf.random_normal([layer3_num])),
        "decoder_b2": tf.Variable(tf.random_normal([layer2_num])),
        "decoder_b3": tf.Variable(tf.random_normal([layer1_num])),
        "decoder_b4": tf.Variable(tf.random_normal([input_length]))
    }

def getTrainData(matrix):
    return np.concatenate((matrix[0:100:2], matrix[100:850]), axis=0)

def getTestData(matrix):
    return np.concatenate((matrix[1:101:2], matrix[850:]), axis=0)

def getLatentSpace(filepath, target_path, model_dir):
    # load data
    myMatrix = getData(filepath)
    myMatrix = myMatrix.astype("float32")
    input_length = myMatrix.shape[1]

    # set layer nums
    layer1_num = 256
    layer2_num = 100
    layer3_num = 10

    # set weight and bias
    weights = setWeight(input_length, layer1_num, layer2_num, layer3_num)
    bias = setBias(input_length, layer1_num, layer2_num, layer3_num)

    # load model
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, model_dir + "model.ckpt")
        latentSpace = encoder(myMatrix, weights, bias)
        np.savetxt(target_path + "latentSpace.txt", latentSpace.eval(), delimiter="\t")

if __name__ == "__main__":
    #train("./Website/data/Gland/filtered.txt", "./model/labelled_data/", learning_rate=0.01, batch_size=100, epoch=1000)
    getLatentSpace('./Website/data/Gland/filtered.txt', "./Website/data/Gland/auto/", './model/labelled_data/')
