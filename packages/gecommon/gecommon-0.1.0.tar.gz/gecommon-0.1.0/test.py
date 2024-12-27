from gecommon import Parallel
from gecommon import CachedERRANT

from gecommon import CachedERRANT
errant = CachedERRANT()
edits = errant.extract_edits('This is a sample sentences .', 'These are sample sentences .')
print(edits)
print([e.__dict__ for e in edits])

gec = Parallel.from_demo()
print(gec.ged_labels_token())

# def check_equal(s1, s2):
#     i = 1
#     for ss1, ss2 in zip(s1, s2):
#         i += 1
#         print(i, ss1, ss2)
#         assert ss1 == ss2

# def load_m2_test(m2, src, trg):
#     print('Loading M2 test')
#     gec = Parallel.from_m2(m2)
#     trgs = open(trg).read().rstrip().split('\n')
#     srcs = open(src).read().rstrip().split('\n')
#     print('Check source')
#     assert len(gec.srcs) == len(srcs)
#     check_equal(gec.srcs, srcs)
#     print('Check target')
#     print(trgs[883])
#     assert len(gec.trgs) == len(trgs)
#     print(trgs[883])
#     check_equal(gec.trgs, trgs)

# load_m2_test(
#     m2='/cl/nldata/GEC/fce/m2/fce.dev.gold.bea19.m2',
#     src='/cl/nldata/GEC/fce/unofficial/dev.src',
#     trg='/cl/nldata/GEC/fce/unofficial/dev.trg'
# )

# load_m2_test(
#     m2='/cl/nldata/GEC/fce/m2/fce.train.gold.bea19.m2',
#     src='/cl/nldata/GEC/fce/unofficial/train.src',
#     trg='/cl/nldata/GEC/fce/unofficial/train.trg'
# )