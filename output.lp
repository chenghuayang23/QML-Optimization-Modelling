\ Model ProductsManufactuing
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  2000 X[0,0] + 2000 X[0,1] + 2500 X[0,2] + 2500 X[0,3] + 2500 X[0,4]
   + 3000 X[0,5] + 3000 X[0,6] + 3000 X[0,7] + 2500 X[0,8] + 2500 X[0,9]
   + 2000 X[0,10] + 2000 X[0,11] + 2000 X[1,0] + 2000 X[1,1] + 2500 X[1,2]
   + 2500 X[1,3] + 2500 X[1,4] + 3000 X[1,5] + 3000 X[1,6] + 3000 X[1,7]
   + 2500 X[1,8] + 2500 X[1,9] + 2000 X[1,10] + 2000 X[1,11] + 2000 X[2,0]
   + 2000 X[2,1] + 2500 X[2,2] + 2500 X[2,3] + 2500 X[2,4] + 3000 X[2,5]
   + 3000 X[2,6] + 3000 X[2,7] + 2500 X[2,8] + 2500 X[2,9] + 2000 X[2,10]
   + 2000 X[2,11] + 6 R[0,0] + 6 R[0,1] + 6 R[0,2] + 6 R[0,3] + 6 R[0,4]
   + 6 R[0,5] + 6 R[0,6] + 6 R[0,7] + 6 R[0,8] + 6 R[0,9] + 6 R[0,10]
   + 6 R[0,11] + 8 R[1,0] + 8 R[1,1] + 8 R[1,2] + 8 R[1,3] + 8 R[1,4]
   + 8 R[1,5] + 8 R[1,6] + 8 R[1,7] + 8 R[1,8] + 8 R[1,9] + 8 R[1,10]
   + 8 R[1,11] + 10 R[2,0] + 10 R[2,1] + 10 R[2,2] + 10 R[2,3] + 10 R[2,4]
   + 10 R[2,5] + 10 R[2,6] + 10 R[2,7] + 10 R[2,8] + 10 R[2,9] + 10 R[2,10]
   + 10 R[2,11]
Subject To
 con1[0,0]-: - 15 X[0,0] + R[0,0] = -750
 con1[0,1]-: - 15 X[0,1] - R[0,0] + R[0,1] = -650
 con1[0,2]-: - 15 X[0,2] - R[0,1] + R[0,2] = -600
 con1[0,3]-: - 15 X[0,3] - R[0,2] + R[0,3] = -500
 con1[0,4]-: - 15 X[0,4] - R[0,3] + R[0,4] = -130.3
 con1[0,5]-: - 15 X[0,5] - R[0,4] + R[0,5] = -650
 con1[0,6]-: - 15 X[0,6] - R[0,5] + R[0,6] = -600
 con1[0,7]-: - 15 X[0,7] - R[0,6] + R[0,7] = -750
 con1[0,8]-: - 15 X[0,8] - R[0,7] + R[0,8] = -650
 con1[0,9]-: - 15 X[0,9] - R[0,8] + R[0,9] = -600
 con1[0,10]-: - 15 X[0,10] - R[0,9] + R[0,10] = -500
 con1[0,11]-: - 15 X[0,11] - R[0,10] + R[0,11] = -550
 con1[1,0]-: - 20 X[1,0] + R[1,0] = -550
 con1[1,1]-: - 20 X[1,1] - R[1,0] + R[1,1] = -500
 con1[1,2]-: - 20 X[1,2] - R[1,1] + R[1,2] = -450
 con1[1,3]-: - 20 X[1,3] - R[1,2] + R[1,3] = -275
 con1[1,4]-: - 20 X[1,4] - R[1,3] + R[1,4] = -350
 con1[1,5]-: - 20 X[1,5] - R[1,4] + R[1,5] = -300
 con1[1,6]-: - 20 X[1,6] - R[1,5] + R[1,6] = -500
 con1[1,7]-: - 20 X[1,7] - R[1,6] + R[1,7] = -600
 con1[1,8]-: - 20 X[1,8] - R[1,7] + R[1,8] = -500
 con1[1,9]-: - 20 X[1,9] - R[1,8] + R[1,9] = -400.6
 con1[1,10]-: - 20 X[1,10] - R[1,9] + R[1,10] = -300
 con1[1,11]-: - 20 X[1,11] - R[1,10] + R[1,11] = -250
 con1[2,0]-: - 10 X[2,0] + R[2,0] = -550
 con1[2,1]-: - 10 X[2,1] - R[2,0] + R[2,1] = -500
 con1[2,2]-: - 10 X[2,2] - R[2,1] + R[2,2] = -500
 con1[2,3]-: - 10 X[2,3] - R[2,2] + R[2,3] = -320.5
 con1[2,4]-: - 10 X[2,4] - R[2,3] + R[2,4] = -300
 con1[2,5]-: - 10 X[2,5] - R[2,4] + R[2,5] = -150.2
 con1[2,6]-: - 10 X[2,6] - R[2,5] + R[2,6] = -225
 con1[2,7]-: - 10 X[2,7] - R[2,6] + R[2,7] = -500
 con1[2,8]-: - 10 X[2,8] - R[2,7] + R[2,8] = -450
 con1[2,9]-: - 10 X[2,9] - R[2,8] + R[2,9] = -350
 con1[2,10]-: - 10 X[2,10] - R[2,9] + R[2,10] = -300
 con1[2,11]-: - 10 X[2,11] - R[2,10] + R[2,11] = -350
 con2[0]-: X[0,0] - X[0,1] + X[1,0] - X[1,1] + X[2,0] - X[2,1] = 0
 con2[3]-: X[0,3] - X[0,4] + X[1,3] - X[1,4] + X[2,3] - X[2,4] = 0
 con2[6]-: X[0,6] - X[0,7] + X[1,6] - X[1,7] + X[2,6] - X[2,7] = 0
 con2[9]-: X[0,9] - X[0,10] + X[1,9] - X[1,10] + X[2,9] - X[2,10] = 0
 con2[1]-: X[0,1] - X[0,2] + X[1,1] - X[1,2] + X[2,1] - X[2,2] = 0
 con2[4]-: X[0,4] - X[0,5] + X[1,4] - X[1,5] + X[2,4] - X[2,5] = 0
 con2[7]-: X[0,7] - X[0,8] + X[1,7] - X[1,8] + X[2,7] - X[2,8] = 0
 con2[10]-: X[0,10] - X[0,11] + X[1,10] - X[1,11] + X[2,10] - X[2,11] = 0
Bounds
Generals
 X[0,0] X[0,1] X[0,2] X[0,3] X[0,4] X[0,5] X[0,6] X[0,7] X[0,8] X[0,9]
 X[0,10] X[0,11] X[1,0] X[1,1] X[1,2] X[1,3] X[1,4] X[1,5] X[1,6] X[1,7]
 X[1,8] X[1,9] X[1,10] X[1,11] X[2,0] X[2,1] X[2,2] X[2,3] X[2,4] X[2,5]
 X[2,6] X[2,7] X[2,8] X[2,9] X[2,10] X[2,11]
End
