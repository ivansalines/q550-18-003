"""Regression for valid no-exit Q550 support windows and early crossings."""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from flow_normal_math_v18_36 import first_exit
from support_censor_v18_38 import checked_support_horizon,common_inside_time,summarize_exits

class SupportCensorTests(unittest.TestCase):
    def test_no_exit_is_censored_not_fatal(self):
        ts=np.linspace(0.,1e-5,100)
        status,exit_t=first_exit(ts,np.full_like(ts,.5),1.,lambda t:.5)
        self.assertEqual(status,'NO_EXIT_OBSERVED');self.assertIsNone(exit_t)
        self.assertEqual(checked_support_horizon(status,exit_t,1e-5),1e-5)
    def test_mixed_cross_and_censor(self):
        window=1e-5
        ts=np.linspace(0.,window,51)
        status,exitt=first_exit(ts,.5+1e5*ts,1.,lambda t:.5+1e5*t)
        self.assertEqual(status,'CROSSED_AFTER_START')
        self.assertAlmostEqual(exitt,5e-6,places=12)
        t=common_inside_time([checked_support_horizon(status,exitt,window),window],window)
        self.assertAlmostEqual(t,2.5e-6,places=12)
        summary=summarize_exits([(status,exitt),('NO_EXIT_OBSERVED',None)],[exitt,window])
        self.assertEqual(summary['observed_exit_count'],1)
        self.assertEqual(summary['right_censored_count'],1)
        self.assertEqual(summary['min_observed_exit_delta_xi'],exitt)
    def test_all_censored_still_has_valid_common_time(self):
        w=1e-5;h=[w]*5
        self.assertEqual(common_inside_time(h,w),.5*w)
        z=summarize_exits([('NO_EXIT_OBSERVED',None)]*5,h)
        self.assertEqual(z['min_observed_exit_delta_xi'],'')
        self.assertEqual(z['max_observed_exit_delta_xi'],'')
        self.assertEqual(z['right_censored_count'],5)
    def test_initially_outside_fails_closed(self):
        ts=np.linspace(0.,1e-5,40)
        status,t=first_exit(ts,np.full_like(ts,1.1),1.,lambda t:1.1)
        self.assertEqual(status,'OUTSIDE_AT_START')
        with self.assertRaises(RuntimeError):checked_support_horizon(status,t,1e-5)
    def test_incompatible_exit_time_is_rejected(self):
        with self.assertRaises(ValueError):checked_support_horizon('NO_EXIT_OBSERVED',9e-6,1e-5)
        with self.assertRaises(ValueError):checked_support_horizon('CROSSED_AFTER_START',None,1e-5)
        with self.assertRaises(ValueError):checked_support_horizon('CROSSED_AFTER_START',2e-5,1e-5)
    def test_common_horizon_validation(self):
        with self.assertRaises(ValueError):common_inside_time([0.,1e-5],1e-5)
        with self.assertRaises(ValueError):common_inside_time([1.1e-5],1e-5)
    def test_uncaught_status_fails_closed(self):
        with self.assertRaises(ValueError):summarize_exits([('SOMETHING',None)],[1e-5])

if __name__=='__main__':unittest.main()
