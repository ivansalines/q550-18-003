import unittest,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from tangent_source_math_v18_39 import normal_frame,minimal_rotation,common_vector,tilt_vector,vector_holdout,source_level_coherence,rotation_angle
from residual_gradient_math_v18_37 import unit
class FullSourceTests(unittest.TestCase):
    def test_orthonormal_nine_plane(self):
        n=unit(np.arange(1.,11.));A=normal_frame(n)
        self.assertLess(np.linalg.norm(A.T@A-np.eye(9)),1e-13)
        self.assertLess(np.linalg.norm(A.T@n),1e-13)
    def test_nearly_axis_householder(self):
        n=np.eye(10)[0];A=normal_frame(n)
        self.assertLess(np.linalg.norm(A.T@n),1e-13)
    def test_minimal_rotation_is_orthogonal(self):
        a=unit(np.arange(1.,11.));b=unit(np.arange(10.,0.,-1.))
        M=minimal_rotation(a,b)
        self.assertLess(np.linalg.norm(M.T@M-np.eye(10)),1e-12)
        self.assertLess(np.linalg.norm(M@a-b),1e-12)
    def test_rotation_identical(self):
        a=unit(np.arange(1.,11.));M=minimal_rotation(a,a)
        self.assertLess(np.linalg.norm(M@a-a),1e-13)
    def test_antiparallel_fails_closed(self):
        a=np.eye(10)[0]
        with self.assertRaises(ValueError):minimal_rotation(a,-a)
    def test_common_source_captures_whole_tangent(self):
        a=unit(np.arange(1.,11.));b=unit(np.arange(10.,0.,-1.));v=np.roll(a,2);v-=a*(a@v)
        A=normal_frame(b);z=common_vector(v,a,b,A)
        self.assertAlmostEqual(float(np.linalg.norm(z)),float(np.linalg.norm(v)),places=12)
    def test_zero_tilt(self):
        a=unit(np.arange(1.,11.));self.assertLess(np.linalg.norm(tilt_vector(a,a)),1e-13)
    def test_tiny_angle_stable(self):
        a=np.eye(10)[0];b=a.copy();b[3]=1.e-11
        z=tilt_vector(a,b)
        self.assertAlmostEqual(float(z[3]),1.e-11,delta=2e-16)
    def test_parallel_tilt_has_sign(self):
        a=np.eye(10)[0];b=a.copy();b[2]=-1.e-6
        self.assertLess(tilt_vector(a,b)[2],0)
    def test_rotation_angle(self):
        a=np.array([1.,0.,0.]);b=np.array([0.,1.,0.]);self.assertAlmostEqual(rotation_angle(a,b),90,places=10)
    def test_rotation_angle_antiparallel(self):
        self.assertAlmostEqual(rotation_angle(np.array([1.,0.]),np.array([-1.,0.])),180,places=8)
    def test_linear_holdout_vector(self):
        rows=[dict(alpha=a,v=[1+2*a,3-a,0]) for a in (-1,-1/3,0,1/3,1)]
        f=vector_holdout(rows,'v');self.assertLess(f['holdout_relative_error'],1e-12)
        self.assertLess(abs(f['inner_outer_odd_turn_deg']),1e-5)
    def test_curved_holdout_failure(self):
        rows=[dict(alpha=a,v=[a+5*a**3,2*a-4*a**3]) for a in (-1,-1/3,0,1/3,1)]
        self.assertGreater(vector_holdout(rows,'v')['holdout_relative_error'],.3)
    def test_missing_symmetric_pair(self):
        rows=[dict(alpha=a,v=[a,1]) for a in (-1,-1/3,0,1)]
        with self.assertRaises(ValueError):vector_holdout(rows,'v')
    def test_centered_coherence_perfect(self):
        x=np.array([-1.,-.33,0.,.33,1.]);v=np.array([x,2*x]).T
        self.assertAlmostEqual(source_level_coherence(x,v),1,places=12)
    def test_centered_coherence_undefined(self):
        self.assertIsNone(source_level_coherence([0,0,0,0,0],np.ones((5,9))))
    def test_projection_can_flip_without_full_reversal(self):
        a=np.array([1.,.01,0.]);b=np.array([1.,-.01,0.]);u=np.array([0.,1.,0.])
        self.assertLess((a@u)*(b@u),0)
        self.assertLess(rotation_angle(a,b),2)
if __name__=='__main__':unittest.main()
