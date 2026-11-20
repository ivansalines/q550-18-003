"""Independent analytical/finite-jet checks with synthetic polynomial Q550-style models."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analytic_source_jet_math_v18_43 import (material_source_jet,moving_coords_and_jet,
    five_point_d1,five_point_d2,curvature,coords,normalized_jac)
from residual_gradient_math_v18_37 import source_geometry,unit
from tangent_source_math_v18_39 import normal_frame

A=np.diag(np.linspace(-.4,.6,10))+np.eye(10,k=1)*.025
J=np.zeros((11,11));J[:10,:10]=A

def f(t,y):
    ans=np.zeros(11);ans[:10]=A@np.asarray(y[:10])+np.arange(1,11)*.031;ans[10]=1.
    return ans

def jac(y):return J

def setup(phase=False):
    q=np.zeros(65+(20 if phase else 0))
    q[:10]=np.linspace(.4,1.3,10)
    q[10]=.15;q[12]=-.12;q[20]=.04
    if phase:q[65:75]=np.linspace(.01,.05,10);q[75:85]=.07
    y=np.r_[np.linspace(.1,.6,10),.22]
    return y,q,np.zeros(10),np.ones(10)

class SourceJetTests(unittest.TestCase):
    def test_first_jet_polynomial_chain(self):
        y,q,c,s=setup(False)
        z=material_source_jet(y,f,jac,q,c,s,0.,2,False,-1.)
        fy=f(0,y);dt=1.e-6
        vals=[]
        for m in (-2,-1,1,2):
            yy=y+m*dt*fy
            gg=source_geometry(yy,f(0,yy),J,q,c,s,0.,2,False,-1.)
            vals.append(gg['perp']/np.linalg.norm(gg['g']))
        der=five_point_d1(*vals,dt)
        self.assertLess(np.linalg.norm(z['pdot']-der),2e-8)
    def test_phase_derivative(self):
        y,q,c,s=setup(True)
        z=material_source_jet(y,f,jac,q,c,s,0.,2,True,-1.)
        fy=f(0,y);dt=1.e-6
        vals=[]
        for m in (-2,-1,1,2):
            yy=y+m*dt*fy
            gg=source_geometry(yy,f(0,yy),J,q,c,s,0.,2,True,-1.)
            vals.append(gg['perp']/np.linalg.norm(gg['g']))
        self.assertLess(np.linalg.norm(z['pdot']-five_point_d1(*vals,dt)),2e-8)
    def test_tangent_jet_identity(self):
        y,q,c,s=setup(True)
        z=material_source_jet(y,f,jac,q,c,s,0.,2,True,-1.)
        self.assertLess(abs(z['n']@z['p']),1e-11)
        self.assertLess(abs(z['n']@z['pdot']+z['ndot']@z['p']),1e-11)
    def test_directional_step_zero_linear_B(self):
        y,q,c,s=setup(True)
        d=[material_source_jet(y,f,jac,q,c,s,0.,2,True,-1.,scaled_target=h)['pdot'] for h in (1e-3,5e-4,1.25e-4)]
        self.assertLess(max(np.linalg.norm(v-d[0]) for v in d),1e-10)
    def test_chart_derivative_including_frame(self):
        y,q,c,s=setup(True)
        zz=material_source_jet(y,f,jac,q,c,s,0.,2,True,-1.)
        other=y.copy();other[:10]+=.03
        oo=material_source_jet(other,f,jac,q,c,s,0.,2,True,-1.)
        n0=zz['n'];fr=normal_frame(n0)
        v,vj,_,_=moving_coords_and_jet(oo,zz,n0,fr)
        dt=1e-5
        pos=coords(oo['p']+dt*oo['pdot'],oo['n']+dt*oo['ndot'],zz['n']+dt*zz['ndot'],n0,fr)
        neg=coords(oo['p']-dt*oo['pdot'],oo['n']-dt*oo['ndot'],zz['n']-dt*zz['ndot'],n0,fr)
        self.assertLess(np.linalg.norm(vj-(pos-neg)/(2*dt)),2e-8)
        self.assertEqual(v.shape,(9,))
    def test_five_point_first_linear(self):
        v=lambda t:np.array([2+3*t,1-t])
        self.assertLess(np.linalg.norm(five_point_d1(*[v(t) for t in (-.1,-.05,.05,.1)],.05)-np.array([3,-1])),1e-13)
    def test_five_point_second_quadratic(self):
        v=lambda t:np.array([1+2*t+4*t*t,t*t])
        self.assertLess(np.linalg.norm(five_point_d2(*[v(t) for t in (-.2,-.1,0,.1,.2)],.1)-np.array([8.,2.])),2e-13)
    def test_curvature_uses_first_derivative_norm(self):
        self.assertAlmostEqual(curvature(np.array([1.,0.,0.]),np.array([0.,2.,0.])),2.)
        self.assertEqual(curvature(np.array([1.,0.]),np.array([3.,0.])),0.)
    def test_first_jet_not_an_exact_second_jet(self):
        # Design guard: module intentionally DOES NOT assert a symbolic ODE Hessian.
        y,q,c,s=setup(True)
        x=material_source_jet(y,f,jac,q,c,s,0.,2,True,-1.)
        self.assertIn('directional_h',x)
        self.assertGreater(x['directional_h'],0.)

if __name__=='__main__':unittest.main()
