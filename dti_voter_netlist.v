//-----------------------------------------------------------------------------------------------------------
//    Copyright (C) 2023 by Dolphin Technology
//    All right reserved.
//
//    Copyright Notification
//    No part may be reproduced except as authorized by written permission.
//
//    Module: dti_voter
//    Company: Dolphin Technology
//    Author: tung
//    Date: 2023/07/11
//-----------------------------------------------------------------------------------------------------------


module dti_voter ( in0, in1, in2, out );
  input in0, in1, in2;
  output out;
  wire   n1;

  dti_12g_aoi222rexp5 U2 ( .A1(in1), .A2(in2), .B1(in1), .B2(in0), .C1(in2), 
        .C2(in0), .Z(n1) );
  dti_12g_invxp3 U3 ( .A(n1), .Z(out) );
endmodule

