//-----------------------------------------------------------------------------------------------------------
//    Copyright (C) 2023 by Dolphin Technology
//    All right reserved.
//
//    Copyright Notification
//    No part may be reproduced except as authorized by written permission.
//
//    Module: rt_qos_controller
//    Company: Dolphin Technology
//    Author: tung
//    Date: 2023/07/11
//-----------------------------------------------------------------------------------------------------------

module rt_dyn_pri_fsm ( acq_thresh_hi, acq_thresh_lo, clk, reset_n, dyn_pri, 
        dyn_update );
  input acq_thresh_hi, acq_thresh_lo, clk, reset_n;
  output dyn_pri, dyn_update;
  wire   \current_state[0] , \next_state[0] , n2, n1, n3, n4;
  assign dyn_pri = \current_state[0] ;

  dti_12g_ffqa01x1 \current_state_reg[0]  ( .D(\next_state[0] ), .CK(clk), 
        .RN(reset_n), .Q(\current_state[0] ) );
  dti_12g_ffqa11x1 dyn_update_cld_reg ( .D(n2), .CK(clk), .RN(reset_n), .SN(n1), .Q(dyn_update) );
  dti_12g_tierailx1 U3 ( .HI(n1) );
  dti_12g_muxi21xp5 U4 ( .D0(n3), .D1(acq_thresh_lo), .S(\current_state[0] ), 
        .Z(\next_state[0] ) );
  dti_12g_nor2xp13 U5 ( .A(n4), .B(\current_state[0] ), .Z(n2) );
  dti_12g_nor2xp13 U6 ( .A(dyn_update), .B(acq_thresh_hi), .Z(n4) );
  dti_12g_invxp5 U7 ( .A(acq_thresh_hi), .Z(n3) );
endmodule


module rt_lat_ctl_fsm ( acr_latency_clr, acr_latency_load, acr_route_free, clk, 
        lat_tercnt_flag, reg_acq_lat_barrier_enable_rt, reset_n, 
        acr_lat_hi_assert, lat_count_en, lat_high, lat_load_en, lat_update );
  input acr_latency_clr, acr_latency_load, acr_route_free, clk,
         lat_tercnt_flag, reg_acq_lat_barrier_enable_rt, reset_n;
  output acr_lat_hi_assert, lat_count_en, lat_high, lat_load_en, lat_update;
  wire   n13, n14, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n15, n16,
         n17, n18;
  wire   [1:0] next_state;
  wire   [1:0] current_state;

  dti_12g_ffqa01x1 lat_update_cld_reg ( .D(n14), .CK(clk), .RN(reset_n), .Q(
        lat_update) );
  dti_12g_ffqa01x1 acr_lat_hi_assert_cld_reg ( .D(n13), .CK(clk), .RN(reset_n), 
        .Q(acr_lat_hi_assert) );
  dti_12g_ffqa01x2 \current_state_reg[1]  ( .D(next_state[1]), .CK(clk), .RN(
        reset_n), .Q(current_state[1]) );
  dti_12g_ffqa01x2 \current_state_reg[0]  ( .D(next_state[0]), .CK(clk), .RN(
        reset_n), .Q(current_state[0]) );
  dti_12g_ckinvx1 U3 ( .A(acr_latency_load), .Z(n12) );
  dti_12g_invxp5 U4 ( .A(n1), .Z(n8) );
  dti_12g_invx1 U5 ( .A(reg_acq_lat_barrier_enable_rt), .Z(n2) );
  dti_12g_or2hpx1 U6 ( .A(lat_high), .B(n11), .Z(next_state[0]) );
  dti_12g_and2hpx4 U7 ( .A(n5), .B(current_state[0]), .Z(lat_load_en) );
  dti_12g_nor2px2 U8 ( .A(n1), .B(n7), .Z(lat_high) );
  dti_12g_nand2px1 U9 ( .A(current_state[1]), .B(n3), .Z(n6) );
  dti_12g_invxp5 U10 ( .A(lat_tercnt_flag), .Z(n10) );
  dti_12g_invxp5 U11 ( .A(lat_update), .Z(n15) );
  dti_12g_nor2hpx1 U12 ( .A(n2), .B(acr_latency_clr), .Z(n3) );
  dti_12g_oai12remx1 U13 ( .B1(lat_high), .B2(n15), .A(n17), .Z(n14) );
  dti_12g_ao12x1 U14 ( .B1(n8), .B2(n12), .A(lat_load_en), .Z(next_state[1])
         );
  dti_12g_bufxp11 U15 ( .A(n6), .Z(n1) );
  dti_12g_nand2xp5 U16 ( .A(n18), .B(n17), .Z(n13) );
  dti_12g_nand2xp5 U17 ( .A(n16), .B(acr_lat_hi_assert), .Z(n18) );
  dti_12g_oai12xp13 U18 ( .B1(acr_route_free), .B2(acr_latency_load), .A(
        lat_high), .Z(n16) );
  dti_12g_nand3xp13 U19 ( .A(lat_count_en), .B(lat_tercnt_flag), .C(n12), .Z(
        n17) );
  dti_12g_nor2px2 U20 ( .A(n6), .B(current_state[0]), .Z(lat_count_en) );
  dti_12g_nand3i1x1 U21 ( .A(acr_latency_clr), .B(acr_latency_load), .C(
        reg_acq_lat_barrier_enable_rt), .Z(n9) );
  dti_12g_invx1 U22 ( .A(n3), .Z(n4) );
  dti_12g_nor2px1 U23 ( .A(current_state[1]), .B(n4), .Z(n5) );
  dti_12g_invx1 U24 ( .A(current_state[0]), .Z(n7) );
  dti_12g_oai22x1 U25 ( .A1(n1), .A2(n10), .B1(n9), .B2(current_state[0]), .Z(
        n11) );
endmodule


module rt_pri_update_2 ( dyn_pri, lat_high, reg_max_priority_rt, ext_qos, 
        reg_ext_priority_rt, reg_realtime_enable_rt, lat_update, dyn_update, 
        pri, pri_update );
  input [1:0] ext_qos;
  output [2:0] pri;
  input dyn_pri, lat_high, reg_max_priority_rt, reg_ext_priority_rt,
         reg_realtime_enable_rt, lat_update, dyn_update;
  output pri_update;
  wire   n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13;

  dti_12g_nor2xp5 U1 ( .A(lat_high), .B(n1), .Z(n7) );
  dti_12g_invxp3 U2 ( .A(reg_realtime_enable_rt), .Z(n2) );
  dti_12g_oai12remx1 U3 ( .B1(lat_high), .B2(ext_qos[1]), .A(
        reg_realtime_enable_rt), .Z(n9) );
  dti_12g_oai12remx1 U4 ( .B1(lat_high), .B2(reg_max_priority_rt), .A(
        reg_realtime_enable_rt), .Z(n8) );
  dti_12g_invxp3 U5 ( .A(lat_high), .Z(n13) );
  dti_12g_oai12xp3 U6 ( .B1(reg_realtime_enable_rt), .B2(n13), .A(n12), .Z(
        pri[0]) );
  dti_12g_oai12xp5 U7 ( .B1(n7), .B2(reg_realtime_enable_rt), .A(n6), .Z(
        pri[1]) );
  dti_12g_nand2xp5 U8 ( .A(n5), .B(n4), .Z(n6) );
  dti_12g_aoi12rexp5 U9 ( .B1(n3), .B2(n7), .A(n2), .Z(pri[2]) );
  dti_12g_nand2xp5 U10 ( .A(n9), .B(ext_qos[0]), .Z(n10) );
  dti_12g_nand2xp5 U11 ( .A(n8), .B(dyn_pri), .Z(n11) );
  dti_12g_oai12remx1 U12 ( .B1(lat_high), .B2(dyn_pri), .A(
        reg_realtime_enable_rt), .Z(n5) );
  dti_12g_nor2i1x1 U13 ( .A(reg_max_priority_rt), .B(reg_ext_priority_rt), .Z(
        n4) );
  dti_12g_and2xp5 U14 ( .A(ext_qos[1]), .B(reg_ext_priority_rt), .Z(n1) );
  dti_12g_nand2xp3 U15 ( .A(dyn_pri), .B(n4), .Z(n3) );
  dti_12g_mux21x1 U16 ( .D0(n11), .D1(n10), .S(reg_ext_priority_rt), .Z(n12)
         );
endmodule


module rt_pri_update_1 ( dyn_pri, lat_high, reg_max_priority_rt, ext_qos, 
        reg_ext_priority_rt, reg_realtime_enable_rt, lat_update, dyn_update, 
        pri, pri_update );
  input [1:0] ext_qos;
  output [2:0] pri;
  input dyn_pri, lat_high, reg_max_priority_rt, reg_ext_priority_rt,
         reg_realtime_enable_rt, lat_update, dyn_update;
  output pri_update;
  wire   n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13;

  dti_12g_nor2xp5 U1 ( .A(lat_high), .B(n1), .Z(n7) );
  dti_12g_oai12remx1 U2 ( .B1(lat_high), .B2(reg_max_priority_rt), .A(
        reg_realtime_enable_rt), .Z(n8) );
  dti_12g_oai12remx1 U3 ( .B1(lat_high), .B2(ext_qos[1]), .A(
        reg_realtime_enable_rt), .Z(n9) );
  dti_12g_invx1 U4 ( .A(reg_realtime_enable_rt), .Z(n2) );
  dti_12g_invxp3 U5 ( .A(lat_high), .Z(n13) );
  dti_12g_oai12xp3 U6 ( .B1(reg_realtime_enable_rt), .B2(n13), .A(n12), .Z(
        pri[0]) );
  dti_12g_oai12xp5 U7 ( .B1(n7), .B2(reg_realtime_enable_rt), .A(n6), .Z(
        pri[1]) );
  dti_12g_nand2xp5 U8 ( .A(n9), .B(ext_qos[0]), .Z(n10) );
  dti_12g_aoi12rexp5 U9 ( .B1(n3), .B2(n7), .A(n2), .Z(pri[2]) );
  dti_12g_nand2xp5 U10 ( .A(n5), .B(n4), .Z(n6) );
  dti_12g_nand2xp5 U11 ( .A(n8), .B(dyn_pri), .Z(n11) );
  dti_12g_oai12remx1 U12 ( .B1(lat_high), .B2(dyn_pri), .A(
        reg_realtime_enable_rt), .Z(n5) );
  dti_12g_nor2i1x1 U13 ( .A(reg_max_priority_rt), .B(reg_ext_priority_rt), .Z(
        n4) );
  dti_12g_and2xp5 U14 ( .A(ext_qos[1]), .B(reg_ext_priority_rt), .Z(n1) );
  dti_12g_nand2xp3 U15 ( .A(dyn_pri), .B(n4), .Z(n3) );
  dti_12g_or2xp3 U16 ( .A(lat_update), .B(dyn_update), .Z(pri_update) );
  dti_12g_mux21x1 U17 ( .D0(n11), .D1(n10), .S(reg_ext_priority_rt), .Z(n12)
         );
endmodule


module dti_bictr_rcnto_up_WIDTH8 ( clk, reset_n, load_en, count_en, count_to, 
        tercnt_flag );
  input [7:0] count_to;
  input clk, reset_n, load_en, count_en;
  output tercnt_flag;
  wire   n19, n20, n21, n22, n23, n24, n25, n26, n27, n1, n2, n3, n4, n5, n6,
         n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n28, n29,
         n30, n31, n32, n33, n34, n35, n36, n37, n38, n39, n40, n41, n42, n43,
         n44, n45, n46, n47, n48, n49, n50, n51, n52, n53, n54, n55, n56, n57,
         n58, n59, n60, n61, n62, n63, n64, n65, n66, n67, n68, n69, n70, n71,
         n72;
  wire   [7:0] count_to_ff;
  wire   [7:0] count_ff;

  dti_12g_ffqa01x1 \count_ff_reg[7]  ( .D(n19), .CK(clk), .RN(reset_n), .Q(
        count_ff[7]) );
  dti_12g_ffqa01x1 \count_ff_reg[6]  ( .D(n20), .CK(clk), .RN(reset_n), .Q(
        count_ff[6]) );
  dti_12g_ffqa01x1 tercnt_flag_reg ( .D(n27), .CK(clk), .RN(reset_n), .Q(
        tercnt_flag) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[7]  ( .D(count_to[7]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[7]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[6]  ( .D(count_to[6]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[6]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[5]  ( .D(count_to[5]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[5]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[4]  ( .D(count_to[4]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[4]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[3]  ( .D(count_to[3]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[3]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[1]  ( .D(count_to[1]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[1]) );
  dti_12g_ffqena10xp9 \count_to_ff_reg[0]  ( .D(count_to[0]), .CE(load_en), 
        .CK(clk), .SN(reset_n), .Q(count_to_ff[0]) );
  dti_12g_ffqa01x2 \count_ff_reg[0]  ( .D(n26), .CK(clk), .RN(reset_n), .Q(
        count_ff[0]) );
  dti_12g_ffqa01x2 \count_ff_reg[1]  ( .D(n25), .CK(clk), .RN(reset_n), .Q(
        count_ff[1]) );
  dti_12g_ffqa01x1 \count_ff_reg[4]  ( .D(n22), .CK(clk), .RN(reset_n), .Q(
        count_ff[4]) );
  dti_12g_ffqa01x2 \count_ff_reg[3]  ( .D(n23), .CK(clk), .RN(reset_n), .Q(
        count_ff[3]) );
  dti_12g_ffqa01x2 \count_ff_reg[2]  ( .D(n24), .CK(clk), .RN(reset_n), .Q(
        count_ff[2]) );
  dti_12g_ffqa10x1 \count_to_ff_reg[2]  ( .D(n72), .CK(clk), .SN(reset_n), .Q(
        count_to_ff[2]) );
  dti_12g_ffqa01x2 \count_ff_reg[5]  ( .D(n21), .CK(clk), .RN(reset_n), .Q(
        count_ff[5]) );
  dti_12g_xnor2bxp5 U3 ( .A(n54), .B(n1), .Z(n56) );
  dti_12g_nor2xp5 U4 ( .A(n48), .B(n47), .Z(n49) );
  dti_12g_bufxp11 U5 ( .A(count_ff[5]), .Z(n1) );
  dti_12g_oai22x1 U6 ( .A1(n33), .A2(n66), .B1(n32), .B2(n69), .Z(n20) );
  dti_12g_muxi21xp11 U7 ( .D0(n69), .D1(n63), .S(n62), .Z(n65) );
  dti_12g_xor3x2 U8 ( .A(n1), .B(n6), .C(n54), .Z(n5) );
  dti_12g_aoi12rex1 U9 ( .B1(count_ff[0]), .B2(n70), .A(count_ff[2]), .Z(n37)
         );
  dti_12g_xor2x1 U10 ( .A(n62), .B(count_to_ff[0]), .Z(n39) );
  dti_12g_xor2x2 U11 ( .A(count_to_ff[1]), .B(n67), .Z(n35) );
  dti_12g_nand2px2 U12 ( .A(n35), .B(n29), .Z(n16) );
  dti_12g_nand2x1 U13 ( .A(n65), .B(n64), .Z(n26) );
  dti_12g_nand3x4 U14 ( .A(n15), .B(n40), .C(n5), .Z(n17) );
  dti_12g_xnor2x1 U15 ( .A(count_to_ff[2]), .B(n38), .Z(n40) );
  dti_12g_nor2px2 U16 ( .A(n4), .B(n16), .Z(n15) );
  dti_12g_ckinvx1 U17 ( .A(n66), .Z(n71) );
  dti_12g_nor2x1 U18 ( .A(load_en), .B(n28), .Z(n29) );
  dti_12g_invx1 U19 ( .A(n3), .Z(n32) );
  dti_12g_oai22xp5 U20 ( .A1(n66), .A2(n53), .B1(n52), .B2(n69), .Z(n24) );
  dti_12g_nand2xp5 U21 ( .A(n46), .B(n45), .Z(n47) );
  dti_12g_oai22rex1 U22 ( .A1(n69), .A2(n61), .B1(n12), .B2(n66), .Z(n23) );
  dti_12g_nand2px1 U23 ( .A(n64), .B(count_en), .Z(n66) );
  dti_12g_invx1 U24 ( .A(n69), .Z(n2) );
  dti_12g_invx1 U25 ( .A(count_en), .Z(n28) );
  dti_12g_invx1 U26 ( .A(n1), .Z(n55) );
  dti_12g_ckinvx1 U27 ( .A(count_to_ff[5]), .Z(n6) );
  dti_12g_nor2x1 U28 ( .A(count_to[5]), .B(count_to[4]), .Z(n45) );
  dti_12g_nor2x1 U29 ( .A(count_to[7]), .B(count_to[6]), .Z(n46) );
  dti_12g_nor2x1 U30 ( .A(count_to[3]), .B(count_to[2]), .Z(n44) );
  dti_12g_nand2x1 U31 ( .A(n2), .B(n70), .Z(n13) );
  dti_12g_invxp5 U32 ( .A(n67), .Z(n68) );
  dti_12g_invxp5 U33 ( .A(n11), .Z(n61) );
  dti_12g_bufx1 U34 ( .A(count_ff[0]), .Z(n62) );
  dti_12g_bufx2 U35 ( .A(count_ff[6]), .Z(n3) );
  dti_12g_nand3i1x1 U36 ( .A(count_to[1]), .B(n44), .C(count_to[0]), .Z(n48)
         );
  dti_12g_nor2mx2 U37 ( .A(n60), .B(n37), .Z(n38) );
  dti_12g_xnor2x1 U38 ( .A(n11), .B(n60), .Z(n12) );
  dti_12g_xnor2x1 U39 ( .A(count_ff[1]), .B(count_ff[0]), .Z(n67) );
  dti_12g_nor3px2 U40 ( .A(n7), .B(n34), .C(n58), .Z(n54) );
  dti_12g_oai22x1 U41 ( .A1(n66), .A2(n56), .B1(n55), .B2(n69), .Z(n21) );
  dti_12g_xor2bxp3 U42 ( .A(n51), .B(n7), .Z(n53) );
  dti_12g_bufxp5 U43 ( .A(count_ff[3]), .Z(n11) );
  dti_12g_oai22x1 U44 ( .A1(n66), .A2(n59), .B1(n58), .B2(n69), .Z(n22) );
  dti_12g_nand2x1 U45 ( .A(n71), .B(n68), .Z(n14) );
  dti_12g_aoi22rehpx1 U46 ( .A1(n49), .A2(load_en), .B1(tercnt_flag), .B2(n2), 
        .Z(n50) );
  dti_12g_oai22x1 U47 ( .A1(n66), .A2(n30), .B1(n10), .B2(n69), .Z(n19) );
  dti_12g_xor2bxp11 U48 ( .A(count_ff[7]), .B(n41), .Z(n30) );
  dti_12g_xor3x1 U49 ( .A(count_ff[3]), .B(count_to_ff[3]), .C(n60), .Z(n4) );
  dti_12g_invx1 U50 ( .A(load_en), .Z(n64) );
  dti_12g_nand2x1 U51 ( .A(n14), .B(n13), .Z(n25) );
  dti_12g_nor2hpx4 U52 ( .A(n7), .B(n34), .Z(n57) );
  dti_12g_bufx2 U53 ( .A(count_ff[1]), .Z(n70) );
  dti_12g_xnor2x2 U54 ( .A(n9), .B(n41), .Z(n18) );
  dti_12g_xor2xp5 U55 ( .A(n58), .B(n57), .Z(n59) );
  dti_12g_nand2px2 U56 ( .A(count_ff[1]), .B(count_ff[0]), .Z(n7) );
  dti_12g_oai12rehpx2 U57 ( .B1(n8), .B2(n17), .A(n50), .Z(n27) );
  dti_12g_nand4x4 U58 ( .A(n36), .B(n18), .C(n43), .D(n39), .Z(n8) );
  dti_12g_nand2px2 U59 ( .A(n57), .B(n31), .Z(n42) );
  dti_12g_xor2x1 U60 ( .A(n10), .B(count_to_ff[7]), .Z(n9) );
  dti_12g_invx2 U61 ( .A(count_ff[7]), .Z(n10) );
  dti_12g_nor2hpx2 U62 ( .A(n7), .B(n52), .Z(n60) );
  dti_12g_invx2 U63 ( .A(count_ff[2]), .Z(n52) );
  dti_12g_nand2hpx4 U64 ( .A(count_ff[3]), .B(count_ff[2]), .Z(n34) );
  dti_12g_ckmux21x1 U65 ( .D0(count_to_ff[2]), .D1(count_to[2]), .S(load_en), 
        .Z(n72) );
  dti_12g_and2x2 U66 ( .A(count_ff[5]), .B(count_ff[4]), .Z(n31) );
  dti_12g_nand3x4 U67 ( .A(n57), .B(n31), .C(n3), .Z(n41) );
  dti_12g_invx1 U68 ( .A(count_en), .Z(n63) );
  dti_12g_nand2i1x2 U69 ( .A(load_en), .B(n63), .Z(n69) );
  dti_12g_xor2xp5 U70 ( .A(n3), .B(n42), .Z(n33) );
  dti_12g_invx2 U71 ( .A(count_ff[4]), .Z(n58) );
  dti_12g_xnor3bx4 U72 ( .A(count_ff[4]), .B(count_to_ff[4]), .C(n57), .Z(n36)
         );
  dti_12g_xor3x1 U73 ( .A(n3), .B(count_to_ff[6]), .C(n42), .Z(n43) );
  dti_12g_invx1 U74 ( .A(n52), .Z(n51) );
endmodule


module rt_pri_update_0 ( dyn_pri, lat_high, reg_max_priority_rt, ext_qos, 
        reg_ext_priority_rt, reg_realtime_enable_rt, lat_update, dyn_update, 
        pri, pri_update );
  input [1:0] ext_qos;
  output [2:0] pri;
  input dyn_pri, lat_high, reg_max_priority_rt, reg_ext_priority_rt,
         reg_realtime_enable_rt, lat_update, dyn_update;
  output pri_update;
  wire   n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13;

  dti_12g_nor2xp5 U1 ( .A(lat_high), .B(n1), .Z(n7) );
  dti_12g_nor2i1xp3 U2 ( .A(reg_max_priority_rt), .B(reg_ext_priority_rt), .Z(
        n4) );
  dti_12g_oai12remx1 U3 ( .B1(lat_high), .B2(ext_qos[1]), .A(
        reg_realtime_enable_rt), .Z(n9) );
  dti_12g_oai12remx1 U4 ( .B1(lat_high), .B2(reg_max_priority_rt), .A(
        reg_realtime_enable_rt), .Z(n8) );
  dti_12g_invx1 U5 ( .A(reg_realtime_enable_rt), .Z(n2) );
  dti_12g_invxp3 U6 ( .A(lat_high), .Z(n13) );
  dti_12g_oai12xp3 U7 ( .B1(reg_realtime_enable_rt), .B2(n13), .A(n12), .Z(
        pri[0]) );
  dti_12g_oai12xp5 U8 ( .B1(n7), .B2(reg_realtime_enable_rt), .A(n6), .Z(
        pri[1]) );
  dti_12g_nand2xp5 U9 ( .A(n5), .B(n4), .Z(n6) );
  dti_12g_nand2xp5 U10 ( .A(n9), .B(ext_qos[0]), .Z(n10) );
  dti_12g_nand2xp5 U11 ( .A(n8), .B(dyn_pri), .Z(n11) );
  dti_12g_aoi12rexp5 U12 ( .B1(n3), .B2(n7), .A(n2), .Z(pri[2]) );
  dti_12g_oai12remx1 U13 ( .B1(lat_high), .B2(dyn_pri), .A(
        reg_realtime_enable_rt), .Z(n5) );
  dti_12g_and2xp5 U14 ( .A(ext_qos[1]), .B(reg_ext_priority_rt), .Z(n1) );
  dti_12g_nand2xp3 U15 ( .A(dyn_pri), .B(n4), .Z(n3) );
  dti_12g_or2xp3 U16 ( .A(lat_update), .B(dyn_update), .Z(pri_update) );
  dti_12g_mux21x1 U17 ( .D0(n11), .D1(n10), .S(reg_ext_priority_rt), .Z(n12)
         );
endmodule


module rt_qos_controller ( acq_thresh_hi, acq_thresh_lo, acr_bank_qos, 
        acr_bank_qos_req, acr_cas_qos_next, acr_latency_clr, acr_latency_load, 
        acr_route_free, clk, reg_pri_cfg_rt, reset_n, acr_lat_hi_assert, 
        acr_pri, acr_pri_req, acr_update, cas_pri, cas_pri_update );
  input [1:0] acr_bank_qos;
  input [1:0] acr_bank_qos_req;
  input [1:0] acr_cas_qos_next;
  input [11:0] reg_pri_cfg_rt;
  output [2:0] acr_pri;
  output [2:0] acr_pri_req;
  output [2:0] cas_pri;
  input acq_thresh_hi, acq_thresh_lo, acr_latency_clr, acr_latency_load,
         acr_route_free, clk, reset_n;
  output acr_lat_hi_assert, acr_update, cas_pri_update;
  wire   dyn_pri, dyn_update, lat_tercnt_flag, lat_count_en, lat_high,
         lat_load_en, lat_update, n2;

  rt_dyn_pri_fsm rt_dyn_pri_fsm ( .acq_thresh_hi(acq_thresh_hi), 
        .acq_thresh_lo(acq_thresh_lo), .clk(clk), .reset_n(reset_n), .dyn_pri(
        dyn_pri), .dyn_update(dyn_update) );
  rt_lat_ctl_fsm rt_lat_ctl_fsm ( .acr_latency_clr(acr_latency_clr), 
        .acr_latency_load(acr_latency_load), .acr_route_free(acr_route_free), 
        .clk(clk), .lat_tercnt_flag(lat_tercnt_flag), 
        .reg_acq_lat_barrier_enable_rt(reg_pri_cfg_rt[3]), .reset_n(reset_n), 
        .acr_lat_hi_assert(acr_lat_hi_assert), .lat_count_en(lat_count_en), 
        .lat_high(lat_high), .lat_load_en(lat_load_en), .lat_update(lat_update) );
  rt_pri_update_2 rt_acr_pri_new ( .dyn_pri(dyn_pri), .lat_high(lat_high), 
        .reg_max_priority_rt(reg_pri_cfg_rt[2]), .ext_qos(acr_bank_qos), 
        .reg_ext_priority_rt(reg_pri_cfg_rt[1]), .reg_realtime_enable_rt(
        reg_pri_cfg_rt[0]), .lat_update(n2), .dyn_update(n2), .pri(acr_pri) );
  rt_pri_update_1 rt_acr_pri_update ( .dyn_pri(dyn_pri), .lat_high(lat_high), 
        .reg_max_priority_rt(reg_pri_cfg_rt[2]), .ext_qos(acr_bank_qos_req), 
        .reg_ext_priority_rt(reg_pri_cfg_rt[1]), .reg_realtime_enable_rt(
        reg_pri_cfg_rt[0]), .lat_update(lat_update), .dyn_update(dyn_update), 
        .pri(acr_pri_req), .pri_update(acr_update) );
  rt_pri_update_0 rt_cas_pri_update ( .dyn_pri(dyn_pri), .lat_high(lat_high), 
        .reg_max_priority_rt(reg_pri_cfg_rt[2]), .ext_qos(acr_cas_qos_next), 
        .reg_ext_priority_rt(reg_pri_cfg_rt[1]), .reg_realtime_enable_rt(
        reg_pri_cfg_rt[0]), .lat_update(lat_update), .dyn_update(dyn_update), 
        .pri(cas_pri), .pri_update(cas_pri_update) );
  dti_bictr_rcnto_up_WIDTH8 rt_lat_count ( .clk(clk), .reset_n(reset_n), 
        .load_en(lat_load_en), .count_en(lat_count_en), .count_to(
        reg_pri_cfg_rt[11:4]), .tercnt_flag(lat_tercnt_flag) );
  dti_12g_tierailx1 U2 ( .LO(n2) );
endmodule

