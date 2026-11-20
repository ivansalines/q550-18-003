"""Synthetic mathematical tests only; no claim of running original Q550 on this host."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from coupled_scaling_math_v18_38 import tangent_to_normal,signed_initial_sources,signed_tilt,response_fit,normalized_pairs

class CoupledTests(unittest.TestCase):
 def test_tangent_orthogonal(self):
  g=np.array([2.,3.,-1.]);u=tangent_to_normal(g,[1.,0.,2.]);self.assertAlmostEqual(float(u@g),0.,places=14)
 def test_tangent_unit(self):
  u=tangent_to_normal([1.,2.,3.],[0.,1.,4.]);self.assertAlmostEqual(np.linalg.norm(u),1.)
 def test_parallel_probe_rejected(self):
  with self.assertRaises(ValueError):tangent_to_normal([1.,0.],[2.,0.])
 def test_signed_sources(self):
  z=dict(g=np.array([2.,0.]),perp=np.array([0.,6.]),r=4.)
  a,b=signed_initial_sources(z,[0.,1.]);self.assertAlmostEqual(a,2.);self.assertAlmostEqual(b,3.)
 def test_source_scale_positive(self):
  z=dict(g=np.array([2.,0.]),perp=np.array([0.,6.]),r=4.)
  zz=dict(g=3*z['g'],perp=3*z['perp'],r=3*z['r'])
  self.assertTrue(np.allclose(signed_initial_sources(z,[0.,1.]),signed_initial_sources(zz,[0.,1.])))
 def test_signed_tilt_small(self):
  a=signed_tilt([1.,0.,0.],[1.,1e-8,0.],[0.,1.,0.]);self.assertAlmostEqual(a,1e-8,places=14)
 def test_signed_tilt_anti_parallel_gauge(self):
  a=signed_tilt([1.,0.,0.],[-1.,-1e-8,0.],[0.,1.,0.]);self.assertAlmostEqual(a,1e-8,places=14)
 def test_linear_response_holdout(self):
  rows=[dict(alpha=x,z=5+3*x) for x in (-1,-1/3,0,1/3,1)]
  fit=response_fit(rows,'z');self.assertAlmostEqual(fit['odd_slope'],3.);self.assertLess(fit['holdout_relative_error'],1e-14)
 def test_curvature_failure_is_visible(self):
  rows=[dict(alpha=x,z=5+3*x+2*x*x) for x in (-1,-1/3,0,1/3,1)]
  fit=response_fit(rows,'z');self.assertGreater(fit['holdout_relative_error'],.3)
 def test_missing_symmetry_rejected(self):
  with self.assertRaises(ValueError):response_fit([dict(alpha=0.,z=1.)],'z')
 def test_zero_var_correlation(self):
  vals=[dict(level_rate=1.,signed_tilt_rate=x) for x in (1.,2.,3.)]
  self.assertIsNone(normalized_pairs(vals)['correlation'])
 def test_nonzero_correlation(self):
  vals=[dict(level_rate=x,signed_tilt_rate=-2*x) for x in (1.,2.,3.)]
  self.assertAlmostEqual(normalized_pairs(vals)['correlation'],-1.)
if __name__=='__main__':unittest.main()
