"""Regression and synthetic control: gradient source, small-angle and joint level/tilt."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from residual_gradient_math_v18_37 import (source_geometry,numerical_residual_gradient,projective_angle,unit,continuous_normal_rhs)
from manifold_math_v18_32 import features,features_flow,features_material_gradient

class ResidualGradient(unittest.TestCase):
 def setUp(self):
  self.center=np.zeros(10);self.scale=np.ones(10);self.theta0=0.
  # y0,y1 quadratic term z1^2, and z0*sin(theta)
  self.q=np.zeros(10+55+20);self.q[0]=1.;self.q[1]=.25;self.q[10+10]=.5 # arbitrary quadratic
  self.q[65]=.12;self.q[66]=-.18;self.q[75]=.09
  self.y=np.r_[np.array([.2,-.3]),np.zeros(8),.45]
  self.J=np.zeros((11,11));self.J[0,1]=1.;self.J[1,0]=-.3
  self.J[2,2]=-.1
 def f(self,t,y):
  v=np.zeros(11);v[0]=y[1];v[1]=-.3*y[0];v[2]=-.1*y[2];v[10]=1.2
  return v
 def geo(self,y=None):
  if y is None:y=self.y
  return source_geometry(y,self.f(0.,y),self.J,self.q,self.center,self.scale,self.theta0,2,True,-1.)
 def test_gradient_source_matches_independent_field_difference(self):
  a=self.geo()['gr'];b=numerical_residual_gradient(self.y,self.f,self.q,self.center,self.scale,self.theta0,2,True,-1.,1e-4)
  self.assertLess(np.linalg.norm(a-b),1e-8)
 def test_grad_of_candidate_direct_difference(self):
  got=self.geo()['g']; h=1e-5
  for i in (0,1,2,9):
   yp=self.y.copy();ym=self.y.copy();yp[i]+=h;ym[i]-=h
   diff=(features(yp,self.center,self.scale,self.theta0,2,True)@self.q-features(ym,self.center,self.scale,self.theta0,2,True)@self.q)/(2*h)
   self.assertAlmostEqual(got[i],diff,places=8)
 def test_finite_difference_step_refinement(self):
  a=self.geo()['gr'];b=numerical_residual_gradient(self.y,self.f,self.q,self.center,self.scale,self.theta0,2,True,-1.,5e-5)
  self.assertLess(np.max(abs(a-b)),2e-8)
 def test_parallel_perp_recombine(self):
  g=self.geo();nu=unit(g['g'])
  self.assertLess(np.linalg.norm(g['gr']-g['parallel']*nu-g['perp']),1e-15)
  self.assertLess(abs(nu@g['perp']),1e-15)
 def test_parallel_and_transverse_both_exist(self):
  g=self.geo()
  self.assertGreater(abs(g['parallel']),1e-3)
  self.assertGreater(np.linalg.norm(g['perp']),1e-3)
 def test_small_angle_does_not_quantize_to_zero(self):
  a=np.r_[1.,np.zeros(9)]; b=np.r_[1.,1e-10,np.zeros(8)]
  self.assertAlmostEqual(projective_angle(a,b),np.degrees(1e-10),delta=1e-15)
 def test_sign_gauge_invariance(self):
  a=np.r_[1.,2.,np.zeros(8)];b=np.r_[.1,1.,np.zeros(8)]
  self.assertAlmostEqual(projective_angle(a,b),projective_angle(-3*a,5*b),places=12)
 def test_unoriented_pi_sign(self):
  a=np.r_[1.,np.zeros(9)]
  self.assertLess(projective_angle(a,-a),1e-10)
 def test_zero_source_identity(self):
  B=self.J[:10,:10];m=np.arange(10,dtype=float)+1.;e=np.zeros(10)
  dm,de=continuous_normal_rhs(B,-1.,m,e,np.zeros(10))
  self.assertTrue(np.allclose(dm,-B.T@m));self.assertTrue(np.allclose(de,np.zeros(10)))
 def test_source_forcing_identity_local(self):
  t=1e-7;g=self.geo();grad=g['g'];gr=g['gr'];B=g['B'];mu=-1.
  # derivative directly of spatial gradient along model trajectory
  yp=self.y+t*self.f(0.,self.y);ym=self.y-t*self.f(0.,self.y)
  gp=self.geo(yp)['g'];gm=self.geo(ym)['g'];dg=(gp-gm)/(2*t)
  predicted=(-B.T+mu*np.eye(10))@grad+gr
  self.assertLess(np.linalg.norm(dg-predicted),2e-7)
 def test_level_source_identity_local(self):
  t=1e-7;y=self.y;g=self.geo(); yp=y+t*self.f(0.,y);ym=y-t*self.f(0.,y)
  cc=(self.geo(yp)['C']-self.geo(ym)['C'])/(2*t)
  self.assertLess(abs(cc-(-1.*g['C']+g['r'])),1e-7)

if __name__=='__main__':unittest.main()
