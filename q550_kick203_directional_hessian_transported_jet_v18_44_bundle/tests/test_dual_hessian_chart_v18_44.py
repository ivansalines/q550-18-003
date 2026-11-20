"""Synthetic independent math tests; NOT original Q550 scientific results."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from dual_hessian_jet_math_v18_44 import *
from analytic_source_jet_math_v18_43 import coords,moving_coords_and_jet
from tangent_source_math_v18_39 import normal_frame

class DualHessianTests(unittest.TestCase):
    def setUp(self):
        rng=np.random.default_rng(1844)
        self.scale=np.exp(rng.normal(size=10))
        self.A=rng.normal(size=(10,10))*.02
        T=rng.normal(size=(10,10,10))*.1
        self.T=(T+T.swapaxes(1,2))/2
        self.y=rng.normal(size=11)*.05
        self.g=rng.normal(size=10)
        self.fy=None
    def f(self,t,y):
        z=y[:10]/self.scale
        fz=self.A@z+.5*np.einsum('ijk,j,k->i',self.T,z,z)+y[10]*z
        return np.r_[fz*self.scale,1.]
    def jac(self,y):
        z=y[:10]/self.scale
        B=self.A+np.einsum('ijk,k->ij',self.T,z)+y[10]*np.eye(10)
        J=np.zeros((11,11))
        J[:10,:10]=B*self.scale[:,None]/self.scale[None,:]
        J[:10,10]=self.scale*z
        return J
    def true_contraction(self):
        v=self.f(0,self.y)[:10]/self.scale
        return np.einsum('i,ijk,k->j',self.g,self.T,v)+self.g
    def test_pinned_analytic_jac_hessian(self):
        r=dot_B_transpose_g_from_jacobian(self.y,self.f(0,self.y),self.jac,self.scale,self.g,.002)
        np.testing.assert_allclose(r,self.true_contraction(),atol=3e-11,rtol=1e-9)
    def test_mixed_rhs_hessian_small_step(self):
        r=mixed_rhs_hessian_contraction(self.y,self.f(0,self.y),self.f,self.scale,self.g,.012)
        np.testing.assert_allclose(r,self.true_contraction(),atol=1e-10,rtol=1e-8)
    def test_mixed_rhs_hessian_large_step(self):
        r=mixed_rhs_hessian_contraction(self.y,self.f(0,self.y),self.f,self.scale,self.g,.035)
        np.testing.assert_allclose(r,self.true_contraction(),atol=1e-10,rtol=1e-8)
    def test_independent_jac_vs_rhs(self):
        r1=dot_B_transpose_g_from_jacobian(self.y,self.f(0,self.y),self.jac,self.scale,self.g,.002)
        r2=mixed_rhs_hessian_contraction(self.y,self.f(0,self.y),self.f,self.scale,self.g,.012)
        np.testing.assert_allclose(r1,r2,atol=1e-10)
    def test_zero_h_rejected(self):
        with self.assertRaises(ValueError):mixed_rhs_hessian_contraction(self.y,self.f(0,self.y),self.f,self.scale,self.g,0)
    def test_negative_h_rejected(self):
        with self.assertRaises(ValueError):mixed_rhs_hessian_contraction(self.y,self.f(0,self.y),self.f,self.scale,self.g,-.1)
    def test_jac_direction_normalized(self):
        speed=normalized_full_speed(self.f(0,self.y),self.scale)
        self.assertEqual(len(speed),11)
        self.assertAlmostEqual(speed[-1],1.)
    def test_source_jet_against_independent_time_shift(self):
        from residual_gradient_math_v18_37 import source_geometry
        q=np.zeros(10);q[0]=1.;q[1]=.13
        y=self.y.copy();fy=self.f(0,y);J=self.jac(y)
        g=source_geometry(y,fy,J,q,np.zeros(10),self.scale,0.,1,False,-1.)['g']
        contraction=mixed_rhs_hessian_contraction(y,fy,self.f,self.scale,g,.012)
        jet=source_jet_from_contraction(y,fy,J,q,np.zeros(10),self.scale,0.,1,False,-1.,contraction)
        h=1e-5
        def p_at(v):
            G=source_geometry(v,self.f(0.,v),self.jac(v),q,np.zeros(10),self.scale,0.,1,False,-1.)
            return G['perp']/np.linalg.norm(G['g'])
        shifted=(p_at(y+h*fy)-p_at(y-h*fy))/(2*h)
        np.testing.assert_allclose(jet['pdot'],shifted,rtol=4e-4,atol=3e-7)

    def test_zero_normal_source_tangency(self):
        rng=np.random.default_rng(90);n=unit(rng.normal(size=10)); b=unit(n+.01*rng.normal(size=10))
        pd=rng.normal(size=10);p=rng.normal(size=10);p-=n*(n@p)
        nd=rng.normal(size=10);nd-=n*(nd@n)
        pd-=n*((nd@p)+(n@pd))
        bd=rng.normal(size=10);bd-=b*(bd@b)
        source=dict(p=p,pdot=pd,n=n,ndot=nd)
        base=dict(n=b,ndot=bd)
        frame=normal_frame(n)
        out=exact_chart_jet(source,base,n,frame)
        eps=1e-7
        vvplus=coords(p+eps*pd,n+eps*nd,b+eps*bd,n,frame)
        vvminus=coords(p-eps*pd,n-eps*nd,b-eps*bd,n,frame)
        np.testing.assert_allclose(out['jet'],(vvplus-vvminus)/(2*eps),atol=3e-8,rtol=1e-6)
    def test_chart_equal_reference(self):
        n=np.zeros(10);n[0]=1.;p=np.zeros(10);p[1]=3;pd=np.zeros(10);pd[2]=4
        src=dict(p=p,pdot=pd,n=n,ndot=np.zeros(10))
        out=exact_chart_jet(src,src,n,normal_frame(n))
        self.assertAlmostEqual(float(out['v'][0]),3)
        self.assertAlmostEqual(float(out['jet'][1]),4)
        self.assertAlmostEqual(float(np.linalg.norm(out['connection_differential'])),0)
    def test_chart_decomposition_identity(self):
        n=np.zeros(10);n[0]=1.;p=np.zeros(10);p[1]=.03;pd=np.zeros(10);pd[2]=.09
        d=np.zeros(10);d[3]=.2
        src=dict(p=p,pdot=pd,n=n,ndot=d)
        out=exact_chart_jet(src,src,n,normal_frame(n))
        np.testing.assert_allclose(out['jet'],out['source_differential']+out['own_alignment_differential']+out['frame_transport_differential'],atol=1e-14)
    def test_antipodal_rejected(self):
        a=np.r_[1.,np.zeros(9)];b=-a
        with self.assertRaises(ValueError):minimal_rotation_with_derivative(a,b,np.zeros(10),np.zeros(10))
    def test_source_jet_exact_quadratic_chain(self):
        # Synthetic phaseblind linear C=z_0; r=F_z0 - mu*z0
        scale=np.ones(10);y=np.zeros(11);y[:10]=.1;y[10]=.2
        fy=self.f(0,self.y);J=self.jac(self.y)
        # F and J are in this synthetic scale; force use self.scale for consistency.
        q=np.r_[np.array([1.]),np.zeros(9)]
        mu=-1.
        contraction=dot_B_transpose_g_from_jacobian(self.y,fy,self.jac,self.scale,q,.002)
        out=source_jet_from_contraction(self.y,fy,J,q,np.zeros(10),self.scale,0.,1,False,mu,contraction)
        self.assertEqual(len(out['pdot']),10)
        self.assertTrue(np.isfinite(out['pdot']).all())

if __name__=='__main__':unittest.main()
