import unittest
import grpc
import numpy as np
from lanfacesdk.model_1 import FaceModel

def channel():
    return grpc.insecure_channel('192.168.1.19:51052')

class TestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_1(self):
        model = FaceModel('tests/images/tfz.jpeg', channel)

        self.assertEqual(model.lens(), 1)

        feature = list(model.features())[0]
        self.assertEqual(len(feature), 4)

        # 特征值，numpy类型
        #print(type(feature[0]),  type(np.ndarray))
        self.assertEqual(isinstance(feature[0], np.ndarray), True)

        # 人脸框
        self.assertEqual(len(feature[1]), 4)
        for i in feature[1]:
            self.assertEqual(type(i), int)

    def test_2(self):
        model = FaceModel('tests/images/tfz.jpeg', '192.168.1.16:8001')

        self.assertEqual(model.lens(), 1)
        
