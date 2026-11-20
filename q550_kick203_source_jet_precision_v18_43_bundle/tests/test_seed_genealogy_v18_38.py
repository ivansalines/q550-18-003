"""Regression tests for v18.38.1: seed count must come from ORIGINAL v18.36."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from seed_genealogy_v18_38 import index_archived_attempts,verify_regenerated_attempts

REF=('surface',3.5,0)
def row(i=1,step=.01,radius=.1):
    return dict(id='surface',anchor_xi='3.5',branch='0',try_index=str(i),valid_projection='True',scaled_step=str(step),scaled_radius=str(radius),in_support='True')

class RealSchemaRegression(unittest.TestCase):
    def test_v18_37_summary_does_not_need_attempt_count(self):
        v37=dict(id='surface',anchor_xi='3.5',branch='0',first_exit_delta_xi=1e-6)
        self.assertNotIn('number_of_seed_attempts',v37)
        v36={REF:dict(id='surface',anchor_xi='3.5',branch='0',number_of_seed_attempts='1')}
        self.assertTrue(verify_regenerated_attempts(REF,[dict(row(),valid_projection=True,in_support=True)],v36,index_archived_attempts([row()])))
    def test_missing_original_case_is_rejected(self):
        with self.assertRaises(RuntimeError):verify_regenerated_attempts(REF,[row()],{},index_archived_attempts([row()]))
    def test_wrong_regeneration_count_is_rejected(self):
        with self.assertRaises(RuntimeError):verify_regenerated_attempts(REF,[],{REF:dict(number_of_seed_attempts=1)},index_archived_attempts([row()]))
    def test_corrupt_attempt_trace_is_rejected(self):
        with self.assertRaises(RuntimeError):verify_regenerated_attempts(REF,[row(step=.05)],{REF:dict(number_of_seed_attempts=1)},index_archived_attempts([row()]))
    def test_bad_flag_is_rejected(self):
        with self.assertRaises(RuntimeError):verify_regenerated_attempts(REF,[dict(row(),in_support=False)],{REF:dict(number_of_seed_attempts=1)},index_archived_attempts([row()]))
    def test_duplicate_attempts_are_rejected(self):
        with self.assertRaises(RuntimeError):index_archived_attempts([row(),row()])
    def test_nonconsecutive_attempts_are_rejected(self):
        with self.assertRaises(RuntimeError):index_archived_attempts([row(2)])

if __name__=='__main__':unittest.main()
