import numpy as np
import trajpy.trajpy as tj
import unittest


class TestFeatures(unittest.TestCase):
 
    @classmethod
    def setUpClass(cls):
        np.random.seed(0)

    def test_efficiency(self):
        """
            test if the efficiency is being computed correctly for three cases
            1) linear trajectory 2) random steps and 3) oscillatory.
        """

        x1 = np.linspace(0, 100, 100)
        x2 = np.random.rand(100)
        x3 = np.cos(np.pi * np.linspace(0, 100, 1000))

        r = tj.Trajectory()

        self.assertAlmostEqual(r.efficiency_(x1), 1.0, places=2)
        self.assertAlmostEqual(r.efficiency_(x2), 0.0, places=2)
        self.assertAlmostEqual(r.straightness_(x3), 0.0, places=1)

    def test_fractal_dimension(self):
        """
            test if the fractal dimension is being computed correctly
        """

        x1 = np.linspace(0, 100, 100)
        x2 = np.random.rand(100)

        r = tj.Trajectory()

        self.assertAlmostEqual(r.fractal_dimension_(x1), 1.0, places=2)
        self.assertGreaterEqual(r.fractal_dimension_(x2), 3.0)

    def test_gyration_radius_and_asymmetry(self):
        """
            testing the radius of gyration for some basic cases
            circle: Rg = R/2
        """
        length = 20
        circle = np.zeros((length, 2))
        radius = 10
        circle_gyr = np.array([[radius, 0.], [0., radius]])/2

        x1 = np.linspace(0, 100, 1000)
        x2 = np.cos(np.pi * np.linspace(0, 100, 1000))
        x1x2 = np.array([x1, x2]).transpose()

        for n in range(0, length):
            circle[n] = radius * np.array([np.cos(np.pi * n/10), np.sin(np.pi * n/10)])

        r = tj.Trajectory()
        gyration_radius = r.gyration_radius_(circle)

        asymmetry_oscillatory = r.asymmetry_(r.gyration_radius_(x1x2))
        asymmetry_circle = r.asymmetry_(gyration_radius)

        self.assertAlmostEqual(asymmetry_oscillatory, 0.60, places=1)
        self.assertAlmostEqual(asymmetry_circle, 0.0, places=1)
        self.assertEqual(np.round(gyration_radius, 2).all(), np.round(circle_gyr, 2).all())


    def test_straightness(self):
        """
            testing the straightness function for three cases
            x1 - linear; x2 - oscillatory; x1x2 - mixed components
        """

        x1 = np.linspace(0, 100, 1000)
        x2 = np.cos(np.pi * np.linspace(0, 100, 1000))
        x1x2 = np.array([x1, x2]).transpose()

        r = tj.Trajectory()

        self.assertAlmostEqual(r.straightness_(x1), 1.0, places=2)
        self.assertAlmostEqual(r.straightness_(x2), 0.0, places=2)
        self.assertAlmostEqual(r.straightness_(x1x2), 0.43, places=1)


if __name__ == '__main__':
    unittest.main()
