import unittest
import numpy as np
from second_derivative_noise_math_v18_42 import chord_metrics,centered_accel,window_diagnostics,loglog_slope,convergence_ratio

class WindowNoiseTests(unittest.TestCase):
    def raw(self,s,quadratic=0):
        s=np.asarray(s)
        return np.stack([np.ones_like(s),.6*s+quadratic*s*s,.1*s,np.zeros_like(s)],axis=-1)
    def test_affine_chord_is_zero(self):
        v=self.raw(np.linspace(0,1,129))
        self.assertLess(chord_metrics(v,1)['chord_max_rel'],1e-14)
    def test_quadratic_window_chord_scales_two(self):
        v=self.raw(np.linspace(0,1,129),.3)
        w=window_diagnostics(v)
        slope=loglog_slope([x['window_fraction'] for x in w],[x['chord_max_abs'] for x in w])
        self.assertAlmostEqual(slope,2,places=10)
    def test_quadratic_second_derivatives(self):
        def f(x):return self.raw(x,.3)
        for h in (.01,.005,.002):
            r=centered_accel(f,.4,h)
            self.assertAlmostEqual(r['accel3_norm'],.6,places=8)
            self.assertAlmostEqual(r['accel5_norm'],.6,places=8)
            self.assertAlmostEqual(r['accel_poly4_norm'],.6,places=8)
    def test_quartic_five_point_exact(self):
        def f(x):return np.array([1.,.3*x**4,x,0.])
        r=centered_accel(f,.5,.01)
        self.assertAlmostEqual(r['accel5_norm'],.9,places=6)
        self.assertAlmostEqual(r['accel_poly4_norm'],.9,places=6)
    def test_three_point_quartic_differs(self):
        def f(x):return np.array([1.,.3*x**4,x,0.])
        r=centered_accel(f,.5,.05)
        self.assertGreater(r['accel3_5_disagreement_rel'],1e-4)
    def test_affine_normal_accel_zero(self):
        def f(x):return np.array([1.,.8*x,.4*x,0.])
        r=centered_accel(f,.5,.01)
        self.assertLess(r['accel5_transverse_norm'],1e-10)
    def test_nonzero_offplane(self):
        s=np.linspace(0,1,129)
        v=np.stack([np.ones_like(s),s,.15*s*(1-s),np.zeros_like(s)],axis=1)
        self.assertGreater(chord_metrics(v,1)['plane_max_frac'],.01)
    def test_bad_array(self):
        with self.assertRaises(ValueError):chord_metrics(np.zeros((3,9)),1)
    def test_bad_window(self):
        with self.assertRaises(ValueError):chord_metrics(self.raw(np.linspace(0,1,129)),0)
    def test_windows_lengths(self):
        w=window_diagnostics(self.raw(np.linspace(0,1,129),.01))
        self.assertEqual([z['uniform_subintervals'] for z in w],[128,64,32,16])
    def test_invalid_window_grid(self):
        with self.assertRaises(ValueError):window_diagnostics(np.zeros((128,9)))
    def test_step_positive(self):
        with self.assertRaises(ValueError):centered_accel(lambda x:self.raw(x),.5,-.1)
    def test_slope_linear(self):
        self.assertAlmostEqual(loglog_slope([1,.5,.25],[2,1,.5]),1)
    def test_underresolved_slope(self):
        self.assertTrue(np.isnan(loglog_slope([1,.5,.25],[0,0,1])))
    def test_convergence_ratio(self):
        self.assertAlmostEqual(convergence_ratio([2,0],[1,0]),.5)
    def test_epsilon_noise_amplifies(self):
        def f(h):
            v=lambda i:np.array([1.,(.8*(.5+i*h))+(1e-12 if i==0 else 0),0.,0.])
            return np.linalg.norm((v(1)-2*v(0)+v(-1))/h**2)
        self.assertGreater(f(1e-4),f(1e-2)*9000)

if __name__=='__main__':unittest.main()
