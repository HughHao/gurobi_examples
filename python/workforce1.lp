\ Model assignment
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  10 x[Amy,Tue2] + 10 x[Amy,Wed3] + 10 x[Amy,Fri5] + 10 x[Amy,Sun7]
   + 10 x[Amy,Tue9] + 10 x[Amy,Wed10] + 10 x[Amy,Thu11] + 10 x[Amy,Fri12]
   + 10 x[Amy,Sat13] + 10 x[Amy,Sun14] + 12 x[Bob,Mon1] + 12 x[Bob,Tue2]
   + 12 x[Bob,Fri5] + 12 x[Bob,Sat6] + 12 x[Bob,Mon8] + 12 x[Bob,Thu11]
   + 12 x[Bob,Sat13] + 10 x[Cathy,Wed3] + 10 x[Cathy,Thu4]
   + 10 x[Cathy,Fri5] + 10 x[Cathy,Sun7] + 10 x[Cathy,Mon8]
   + 10 x[Cathy,Tue9] + 10 x[Cathy,Wed10] + 10 x[Cathy,Thu11]
   + 10 x[Cathy,Fri12] + 10 x[Cathy,Sat13] + 10 x[Cathy,Sun14]
   + 8 x[Dan,Tue2] + 8 x[Dan,Wed3] + 8 x[Dan,Fri5] + 8 x[Dan,Sat6]
   + 8 x[Dan,Mon8] + 8 x[Dan,Tue9] + 8 x[Dan,Wed10] + 8 x[Dan,Thu11]
   + 8 x[Dan,Fri12] + 8 x[Dan,Sat13] + 8 x[Dan,Sun14] + 8 x[Ed,Mon1]
   + 8 x[Ed,Tue2] + 8 x[Ed,Wed3] + 8 x[Ed,Thu4] + 8 x[Ed,Fri5]
   + 8 x[Ed,Sun7] + 8 x[Ed,Mon8] + 8 x[Ed,Tue9] + 8 x[Ed,Thu11]
   + 8 x[Ed,Sat13] + 8 x[Ed,Sun14] + 9 x[Fred,Mon1] + 9 x[Fred,Tue2]
   + 9 x[Fred,Wed3] + 9 x[Fred,Sat6] + 9 x[Fred,Mon8] + 9 x[Fred,Tue9]
   + 9 x[Fred,Fri12] + 9 x[Fred,Sat13] + 9 x[Fred,Sun14] + 11 x[Gu,Mon1]
   + 11 x[Gu,Tue2] + 11 x[Gu,Wed3] + 11 x[Gu,Fri5] + 11 x[Gu,Sat6]
   + 11 x[Gu,Sun7] + 11 x[Gu,Mon8] + 11 x[Gu,Tue9] + 11 x[Gu,Wed10]
   + 11 x[Gu,Thu11] + 11 x[Gu,Fri12] + 11 x[Gu,Sat13] + 11 x[Gu,Sun14]
Subject To
 Mon1: x[Bob,Mon1] + x[Ed,Mon1] + x[Fred,Mon1] + x[Gu,Mon1] = 3
 Tue2: x[Amy,Tue2] + x[Bob,Tue2] + x[Dan,Tue2] + x[Ed,Tue2] + x[Fred,Tue2]
   + x[Gu,Tue2] = 2
 Wed3: x[Amy,Wed3] + x[Cathy,Wed3] + x[Dan,Wed3] + x[Ed,Wed3]
   + x[Fred,Wed3] + x[Gu,Wed3] = 4
 Thu4: x[Cathy,Thu4] + x[Ed,Thu4] = 4
 Fri5: x[Amy,Fri5] + x[Bob,Fri5] + x[Cathy,Fri5] + x[Dan,Fri5] + x[Ed,Fri5]
   + x[Gu,Fri5] = 5
 Sat6: x[Bob,Sat6] + x[Dan,Sat6] + x[Fred,Sat6] + x[Gu,Sat6] = 6
 Sun7: x[Amy,Sun7] + x[Cathy,Sun7] + x[Ed,Sun7] + x[Gu,Sun7] = 5
 Mon8: x[Bob,Mon8] + x[Cathy,Mon8] + x[Dan,Mon8] + x[Ed,Mon8]
   + x[Fred,Mon8] + x[Gu,Mon8] = 2
 Tue9: x[Amy,Tue9] + x[Cathy,Tue9] + x[Dan,Tue9] + x[Ed,Tue9]
   + x[Fred,Tue9] + x[Gu,Tue9] = 2
 Wed10: x[Amy,Wed10] + x[Cathy,Wed10] + x[Dan,Wed10] + x[Gu,Wed10] = 3
 Thu11: x[Amy,Thu11] + x[Bob,Thu11] + x[Cathy,Thu11] + x[Dan,Thu11]
   + x[Ed,Thu11] + x[Gu,Thu11] = 4
 Fri12: x[Amy,Fri12] + x[Cathy,Fri12] + x[Dan,Fri12] + x[Fred,Fri12]
   + x[Gu,Fri12] = 6
 Sat13: x[Amy,Sat13] + x[Bob,Sat13] + x[Cathy,Sat13] + x[Dan,Sat13]
   + x[Ed,Sat13] + x[Fred,Sat13] + x[Gu,Sat13] = 7
 Sun14: x[Amy,Sun14] + x[Cathy,Sun14] + x[Dan,Sun14] + x[Ed,Sun14]
   + x[Fred,Sun14] + x[Gu,Sun14] = 5
Bounds
 x[Amy,Tue2] <= 1
 x[Amy,Wed3] <= 1
 x[Amy,Fri5] <= 1
 x[Amy,Sun7] <= 1
 x[Amy,Tue9] <= 1
 x[Amy,Wed10] <= 1
 x[Amy,Thu11] <= 1
 x[Amy,Fri12] <= 1
 x[Amy,Sat13] <= 1
 x[Amy,Sun14] <= 1
 x[Bob,Mon1] <= 1
 x[Bob,Tue2] <= 1
 x[Bob,Fri5] <= 1
 x[Bob,Sat6] <= 1
 x[Bob,Mon8] <= 1
 x[Bob,Thu11] <= 1
 x[Bob,Sat13] <= 1
 x[Cathy,Wed3] <= 1
 x[Cathy,Thu4] <= 1
 x[Cathy,Fri5] <= 1
 x[Cathy,Sun7] <= 1
 x[Cathy,Mon8] <= 1
 x[Cathy,Tue9] <= 1
 x[Cathy,Wed10] <= 1
 x[Cathy,Thu11] <= 1
 x[Cathy,Fri12] <= 1
 x[Cathy,Sat13] <= 1
 x[Cathy,Sun14] <= 1
 x[Dan,Tue2] <= 1
 x[Dan,Wed3] <= 1
 x[Dan,Fri5] <= 1
 x[Dan,Sat6] <= 1
 x[Dan,Mon8] <= 1
 x[Dan,Tue9] <= 1
 x[Dan,Wed10] <= 1
 x[Dan,Thu11] <= 1
 x[Dan,Fri12] <= 1
 x[Dan,Sat13] <= 1
 x[Dan,Sun14] <= 1
 x[Ed,Mon1] <= 1
 x[Ed,Tue2] <= 1
 x[Ed,Wed3] <= 1
 x[Ed,Thu4] <= 1
 x[Ed,Fri5] <= 1
 x[Ed,Sun7] <= 1
 x[Ed,Mon8] <= 1
 x[Ed,Tue9] <= 1
 x[Ed,Thu11] <= 1
 x[Ed,Sat13] <= 1
 x[Ed,Sun14] <= 1
 x[Fred,Mon1] <= 1
 x[Fred,Tue2] <= 1
 x[Fred,Wed3] <= 1
 x[Fred,Sat6] <= 1
 x[Fred,Mon8] <= 1
 x[Fred,Tue9] <= 1
 x[Fred,Fri12] <= 1
 x[Fred,Sat13] <= 1
 x[Fred,Sun14] <= 1
 x[Gu,Mon1] <= 1
 x[Gu,Tue2] <= 1
 x[Gu,Wed3] <= 1
 x[Gu,Fri5] <= 1
 x[Gu,Sat6] <= 1
 x[Gu,Sun7] <= 1
 x[Gu,Mon8] <= 1
 x[Gu,Tue9] <= 1
 x[Gu,Wed10] <= 1
 x[Gu,Thu11] <= 1
 x[Gu,Fri12] <= 1
 x[Gu,Sat13] <= 1
 x[Gu,Sun14] <= 1
End
