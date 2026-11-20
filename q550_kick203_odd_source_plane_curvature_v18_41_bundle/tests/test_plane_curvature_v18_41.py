"""Synthetic mathematics only; no tests substitute for the original Q550 ODE."""
import sys,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'scripts'),str(R/'reference')]
from response_plane_math_v18_41 import plane_fit,angular_path,curve_curvature,summarize_response
from gauge_temporal_math_v18_40 import stable_turn,tangent_twist
from tangent_source_math_v18_39 import normal_frame
import original_response_plane_v18_41_math as audit

class MathTests(unittest.TestCase):
    def u(self,degree=62,n=128):
        t=np.linspace(0.,1.,n+1);theta=np.deg2rad(degree)*t
        return np.stack([np.cos(theta),np.sin(theta),np.zeros(len(t)),np.zeros(len(t))],axis=1)
    def test_great_circle_endpoint(self):
        info=plane_fit(self.u());self.assertAlmostEqual(info['endpoint_turn_deg'],62.,places=10)
    def test_great_circle_planarity(self):
        self.assertLess(np.max(plane_fit(self.u())['plane_deviation']),1e-14)
    def test_great_circle_path(self):
        self.assertAlmostEqual(angular_path(self.u()),62.,places=8)
    def test_great_circle_geo_curvature(self):
        v=self.u();d=curve_curvature(v,128)
        self.assertLess(np.nanmedian(d['geodesic']),1e-8)
    def test_true_out_of_plane_perturbation(self):
        t=np.linspace(0.,1.,129);v=self.u();v[:,2]+=.15*np.sin(np.pi*t)
        self.assertGreater(np.max(plane_fit(v)['plane_deviation']),.1)
    def test_nonplanar_even_if_endpoint_matches(self):
        v=self.u();v[32:96,2]=.25
        self.assertGreater(np.max(plane_fit(v)['plane_deviation']),.2)
    def test_affine_raw_large_angle(self):
        t=np.linspace(0.,1.,129);start=np.array([1.,0.,0.,0.]);end=np.array([0.,.7,0.,0.])
        v=(1-t[:,None])*start+t[:,None]*end
        f=plane_fit(v);self.assertAlmostEqual(f['endpoint_turn_deg'],90,places=8)
        self.assertLess(max(f['raw_chord_deviation']),1e-14)
    def test_non_affine_with_planarity(self):
        v=self.u();f=plane_fit(v)
        self.assertLess(max(f['plane_deviation']),1e-14)
        self.assertGreater(max(f['raw_chord_deviation'])/f['raw_chord_scale'],.02)
    def test_path_can_exceed_endpoint(self):
        t=np.linspace(0.,1.,129);theta=np.deg2rad(45)*(t+.2*np.sin(2*np.pi*t))
        v=np.stack([np.cos(theta),np.sin(theta),np.zeros(len(t)),np.zeros(len(t))],axis=1)
        self.assertGreater(angular_path(v),stable_turn(v[0],v[-1])+1.)
    def test_coordinate_rotation_invariant_if_realigned(self):
        v=self.u();Q=tangent_twist(.21,4)
        rotated=v@Q
        self.assertAlmostEqual(max(plane_fit(v)['plane_deviation']),max(plane_fit(rotated)['plane_deviation']),places=12)
    def test_synthetic_antipodal_plane_rejected(self):
        v=self.u(0);v[-1]=-v[0]
        with self.assertRaises(ValueError):plane_fit(v)
    def test_synthetic_zero_odd_source_rejected(self):
        v=self.u();v[7]=0
        with self.assertRaises(ValueError):plane_fit(v)
    def test_nonuniform_grid_rejected(self):
        with self.assertRaises(ValueError):curve_curvature(self.u(),12)
    def test_summary_has_nested_geometry(self):
        s=summarize_response(self.u(),128)
        self.assertEqual(s['count_reverse_plane_phase_steps'],0)
        self.assertGreaterEqual(s['curvature_resolved_nodes'],124)
    def test_synthetic_audit_end_to_end(self):
        class Sol:
            def __init__(self,a):self.a=a
            def sol(self,t):
                y=np.zeros(11);y[0]=self.a;y[1]=t;return y
        n=np.zeros(10);n[-1]=1.
        w=np.zeros(10);w[0]=1.;u=np.zeros(10);u[1]=1.
        def geom(y):return dict(g=n,perp=np.array([.15*y[0],.15*y[0]*y[1],0,0,0,0,0,0,0,0.]))
        def grads(*args):return n[None,:]
        cases=[(a,np.zeros(11),0.,Sol(a),'CROSSED_AFTER_START',2.,2.) for a in (-1.,-1./3.,0.,1./3.,1.)]
        with patch.object(audit,'features_material_gradient',grads):
            result=audit.response_plane_case_audit('synthetic','SYNTHETIC',3.5,0,cases,geom,np.ones(10),
                np.ones(1),np.zeros(10),0.,dict(degree=1,phase=False),n,normal_frame(n),1.,45.,45.)
        self.assertEqual(len(result['profile']),129)
        self.assertEqual(len(result['resolutions']),4)
        self.assertLess(result['family']['max_plane_deviation_fraction'],1e-11)
        self.assertLess(result['family']['max_raw_chord_error_rel'],1e-11)
        self.assertLess(result['family']['endpoint_angle_replay_error_deg'],1e-10)

if __name__=='__main__':unittest.main()
