import unittest
import numpy as np
from shamboflow.engine.activations import signmoid, relu, tanh, leakyrelu, softmax

class TestActivation(unittest.TestCase) :

    def test_relu(self) :
        x = np.array([-2, 3, 4, -4])
        x_res = np.array([0, 3, 4, 0])

        np.testing.assert_array_equal(relu(x), x_res)

    def test_sigmoid(self) :
        x = np.array([-2, 3, 4, -4])
        x_res = np.array([0.119203, 0.952574, 0.982014, 0.017986])

        np.testing.assert_array_almost_equal(signmoid(x), x_res)

unittest.main()