import unittest,sys
from pathlib import Path
import numpy as np
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'scripts')]
from residual_gradient_math_v18_37 import unit
from tangent_source_math_v18_39 import normal_frame,minimal_rotation
from gauge_temporal_math_v18_40 import *
class MathGaugeTests(unittest.TestCase):
    def setUp(self):
        self.n0=unit(np.array([1.,.3,.2,.1,0.,0.,0.,0.,0.,.07]))
        self.n1=unit(np.array([.9,.35,.12,-.2,.08,.0,.0,.0,.0,.1]))
        self.F0=normal_frame(self.n0)
    def test_direct_transport_normal(self):
        F=direct_frame(self.n0,self.n1,self.F0)
        self.assertLess(np.linalg.norm(F.T@self.n1),1.e-12)
    def test_direct_orthonormal(self):
        F=direct_frame(self.n0,self.n1,self.F0)
        self.assertLess(np.linalg.norm(F.T@F-np.eye(9)),1.e-12)
    def test_incremental_normal(self):
        ns=[unit((1-t)*self.n0+t*self.n1) for t in np.linspace(0,1,17)]
        frames=path_frames(ns,self.F0)
        self.assertLess(np.linalg.norm(frames[-1].T@ns[-1]),1e-12)
    def test_incremental_preserves_norm(self):
        ns=[unit((1-t)*self.n0+t*self.n1) for t in np.linspace(0,1,17)]
        F=path_frames(ns,self.F0)[-1]
        self.assertLess(np.linalg.norm(F.T@F-np.eye(9)),1e-12)
    def test_bridge_normal(self):
        ns=[unit((1-t)*self.n0+t*self.n1) for t in np.linspace(0,1,9)]
        Fs=path_frames(ns,self.F0)
        fm=bridge_frame(ns,Fs,.37,unit(.63*self.n0+.37*self.n1))
        self.assertLess(np.linalg.norm(fm.T@unit(.63*self.n0+.37*self.n1)),1e-12)
    def test_chart_coordinate_reconstruction(self):
        F=direct_frame(self.n0,self.n1,self.F0);C=normal_frame(self.n1)
        v=F@np.arange(1.,10.)
        z=align_coordinate(C.T@v,C,F)
        self.assertLess(np.linalg.norm(z-F.T@v),1e-12)
    def test_twisted_chart_reconstruction(self):
        F=direct_frame(self.n0,self.n1,self.F0);Q=tangent_twist(.35);Ft=F@Q
        x=np.arange(1.,10.)
        self.assertLess(np.linalg.norm(align_coordinate(Q.T@x,Ft,F)-x),1e-12)
    def test_twist_orthogonal(self):
        for t in np.linspace(0,1,21):
            Q=tangent_twist(t)
            self.assertLess(np.linalg.norm(Q.T@Q-np.eye(9)),1.e-13)
    def test_small_turn_atan2(self):
        a=np.array([1.,0.,0.]);b=np.array([1.,1.e-10,0.])
        self.assertAlmostEqual(stable_turn(a,b),np.degrees(1.e-10),delta=1.e-14)
    def test_flip_angle(self):
        self.assertAlmostEqual(stable_turn([1.,0.],[-1.,0.]),180.,places=9)
    def test_orthogonal_angle(self):
        self.assertAlmostEqual(stable_turn([1.,0.],[0.,1.]),90.,places=9)
    def test_degenerate_rejected(self):
        self.assertIsNone(stable_turn(np.zeros(9),np.ones(9)))
    def test_projection_false_flip(self):
        v=np.array([.001,1.]);w=np.array([-.001,1.])
        self.assertLess(stable_turn(v,w),.12)
        self.assertLess(v[0]*w[0],0)
    def test_time_arc_resolution(self):
        vectors=[np.array([np.cos(t),np.sin(t)]) for t in np.linspace(0,np.pi/2,33)]
        for stride in (1,2,4,8):self.assertAlmostEqual(angular_travel(vectors,stride),90.,delta=1e-8)
    def test_backtracking_path(self):
        theta=np.r_[np.linspace(0,1,17),np.linspace(1,0,16)]
        vec=[np.array([np.cos(x),np.sin(x)]) for x in theta]
        self.assertAlmostEqual(stable_turn(vec[0],vec[-1]),0.,delta=1e-8)
        self.assertGreater(angular_travel(vec,1),100)
    def test_frame_coordinate_invariance_with_moving_twist(self):
        vectors=[np.array([1.,0.,0.,0.,0.,0.,0.,0.,0.])]*2
        self.assertLess(stable_turn(vectors[0],vectors[1]),1.e-8)
        Q=tangent_twist(.35)
        raw=stable_turn(vectors[0],Q.T@vectors[1])
        self.assertGreater(raw,0.1)
        self.assertLess(stable_turn(vectors[0],Q@(Q.T@vectors[1])),1.e-8)
    def test_odd_response(self):
        h=round(1/3,10)
        by={-h:[0.,1.],h:[2.,1.]}
        self.assertAlmostEqual(odd_response(by)[0],3.)
    def test_travel_sampling_nonnegative(self):
        vec=[np.array([1.,0.]) for i in range(33)]
        self.assertAlmostEqual(angular_travel(vec,4),0.)
if __name__=='__main__':unittest.main()

class TemporalReplaySmoke(unittest.TestCase):
    def test_synthetic_time_scan_and_gauge_closure(self):
        from gauge_temporal_math_v18_40 import temporal_case_audit
        class FakeSolution:
            def __init__(self,alpha):self.alpha=alpha
            def sol(self,t):
                z=np.zeros(11);z[1]=self.alpha;z[2]=self.alpha*t/1.e-6
                return z
        def geom(y):
            g=np.zeros(10);g[0]=1.
            p=np.zeros(10);p[1]=y[1];p[2]=y[2]
            return dict(g=g,perp=p,r=float(y[1]*.1),C=0.)
        trials=[(a,np.zeros(11),0.,FakeSolution(a),'NO_EXIT_OBSERVED',None,1.e-5)
                for a in (-1.,-1./3.,0.,1./3.,1.)]
        q=np.zeros(10);q[0]=1.
        n0=np.eye(10)[0];F0=normal_frame(n0)
        ans=temporal_case_audit('synthetic','synthetic',3.5,0,trials,geom,np.ones(10),q,
            np.zeros(10),0.,{'degree':1,'phase':False},-1.,n0,F0,1.e-6,np.eye(10)[1],
            1.,1.,{},dict(full_odd_source_transport_turn_deg=45.))
        self.assertEqual(len(ans['temporal']),14)
        self.assertEqual(len(ans['resolution']),4)
        self.assertAlmostEqual(ans['family']['endpoint_turn_direct_deg'],45.,places=7)
        self.assertLess(ans['max_chart_alignment'],1e-12)
        self.assertLess(ans['max_twist_alignment'],1e-12)
        self.assertLess(ans['family']['endpoint_path8_vs_path64_difference_deg'],1e-10)
