'''
Algorithm: Neural Network with dynamic activation functions
Date: Thursday November 5th, 2020
Autor: Ramiro Mendez, based in Carlos Santana Model
'''
import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from IPython.display import clear_output
from sklearn.datasets import make_circles   # Dataset

# Neural layers
from neural_layer import Neural_Layer

'''
Anonymous function (commented) 
    Sigmoid activation function and derivate
    index 0 actual function
    index 1 derivation function
'''
sigm = (lambda x: 1 / (1 + np.e ** (-x)),
        lambda x: x * (1 - x))

'''
Anonymous function (commented) 
    Relu activation function and derivate
'''
# relu = lambda x: np.maximum(0,x)

'''
Cost Function (anonymous commented) 
    Least Mean Square function and derivate
    Returns difference between output and desired 
'''
lms_cost = (lambda output, desired: np.mean((output - desired) ** 2),
            lambda output, desired: (output - desired))

'''
Neural Network topology
    Returns nn  Neural network array with layers inside
    topology    Vector to instantiate n neurons per layer in NN
    act_f       Activation function

    For item in array 'topology' creates actual layer 
    Instantiates 'n' inputs to the next one and 'act_f' per layer
'''


def create_nn(topology, act_f):
    nn = []
    for i, connections in enumerate(topology[:-1]):
        nn.append(Neural_Layer(connections, topology[i+1], act_f))
    return nn


'''
Training
    neural_network  Vector of layers [(obj), (obj1),...]
    samples         Vector of inputs [(x1, x2), (x1, x2),...]  
    desired         Vector of desired output (Classification)[1, 0, 1, ...]
    lms_cost        Least Men Square, Cost Function > Returns error
    lr              Learning Rate
    train           Specifies if Executes training(True) or just prediction(False)
'''


def train(neural_network, samples, desired, lms_cost, lr=0.05, train=True):
    '''
    Forward pass -> 
        Gets samples and desired, passes through layers
        Applies weighted sum (samples * weights + bias)
        Weighted sum to Activation function

        z       Stores value of weighted sum
        a       Stores value of activation function of z
        output  Vector that stores output of every layer
                Weighted sum and activation function per layer
    '''
    # Just for first layer
    output = [(None, samples)]

    for _, layer in enumerate(neural_network):
        # @ it is used to matrix multiplication
        # Gets the value of activation function in last pair of values (output of previous layer)
        z = output[-1][1] @ layer.weights + layer.bias
        a = layer.activation_f[0](z)
        output.append((z, a))

    '''
    Backward pass <-
        Back propagation:
            Partials derivates for steepest descent
            Propagates error backwards (delta)

        Steepest descent
    '''
    if train:
        #  Back Propagation
        '''
        delta   error per layer
        '''
        deltas = []

        for i in reversed(range(0, len(neural_network))):
            z = output[i+1][0]
            a = output[i+1][1]

            if i == len(neural_network) - 1:
                # Calculates last layer delta
                deltas.insert(0, lms_cost[1](a, desired)
                              * neural_network[i].activation_f[1](a))
            else:
                # Calculates delta based in previous layer
                deltas.insert(0, deltas[0] @ _weights.T * neural_network[i].activation_f[1](a))

            _weights = neural_network[i].weights
            # Steepest descent
            neural_network[i].bias = neural_network[i].bias - (np.mean(deltas[0], axis=0, keepdims=True) * lr)
            neural_network[i].weights = neural_network[i].weights - output[i][1].T @ deltas[0] * lr
    return output[-1][1]

if __name__ == "__main__":
    # Create dataset
    # n   stands for number of samples to train with
    # p   number of inputs per sample, characteristics of every sample
    n = 500
    p = 2

    '''
    make_circles
        n_samples : int or two-element tuple, optional (default=100)
            If int, it is the total number of points generated. 
            For odd numbers, the inner circle will have one point more than the outer circle. 
            If two-element tuple, number of points in outer circle and inner circle.

        noise : double or None (default=None)
            Standard deviation of Gaussian noise added to the data.

        factor : 0 < double < 1 (default=.8)
            Scale factor between inner and outer circle.    
    '''
    # Samples it's a matrix that gets inputs per sample
    # Desired it's a vector that stores clasification per sample
    samples, desired = make_circles(n_samples=n, factor=0.45, noise=0.05)
    desired = desired[:, np.newaxis]

    '''
    topology        Stores number of neurons per layer in neural network
                    Final is 1 because classification is binary, based in 0 or 1
    '''
    topology = [p, 4, 8, 1]
    neural_network = create_nn(topology, sigm)
    loss = []

    for i in range(2500):
        # Training
        pY = train(neural_network, samples, desired, lms_cost)

        if i % 10 == 0:
            print(pY)

            loss.append(lms_cost[0](pY, desired))

            res = 50

            _x0 = np.linspace(-1.5, 1.5, res)
            _x1 = np.linspace(-1.5, 1.5, res)

            _Y =  np.zeros((res, res))

            for i0, x0 in enumerate(_x0):
                for i1, x1 in enumerate(_x1):
                    _Y[i0,i1] = train(neural_network, np.array([[x0, x1]]), desired, lms_cost, train=False)[0][0]
            
            plt.pcolormesh(_x0, _x1, _Y, cmap="coolwarm")
            plt.axis("equal")

            # Samples in first class, in this case class  '0'`
            plt.scatter(samples[desired[:,0] == 0, 0],
                        samples[desired[:,0] == 0, 1], color="skyblue")

            # Samples in first class, in this case class  '1'
            plt.scatter(samples[desired[:,0] == 1, 0],
                        samples[desired[:,0] == 1, 1], color="red")
            
            clear_output(wait=True)
            plt.show()
            plt.pause(0.01)
            plt.ion()
            # plt.plot(range(len(loss)), loss)
            # plt.show()
            # time.sleep(0.2)
