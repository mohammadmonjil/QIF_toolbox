/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : T-2022.03-SP5
// Date      : Thu Mar  2 16:10:02 2023
/////////////////////////////////////////////////////////////


module const_output_2bit ( clk, reset, asset, data_out );
  output [1:0] data_out;
  input clk, reset, asset;
  wire   N9, N10, N12, N13, n9, n10, n11, n12, n13, n14, n15, n16;
  wire   [1:0] count;

  DFFSNQ_X1 \count_reg[0]  ( .D(N9), .CLK(clk), .SN(1'b1), .Q(count[0]) );
  DFFSNQ_X1 \count_reg[1]  ( .D(N10), .CLK(clk), .SN(1'b1), .Q(count[1]) );
  DFFSNQ_X1 \data_out_reg[1]  ( .D(N13), .CLK(clk), .SN(1'b1), .Q(data_out[1])
         );
  DFFSNQ_X1 \data_out_reg[0]  ( .D(N12), .CLK(clk), .SN(1'b1), .Q(data_out[0])
         );
  OR2_X1 U15 ( .A1(N10), .A2(N9), .Z(N13) );
  NAND2_X1 U16 ( .A1(n9), .A2(n10), .ZN(N12) );
  NAND2_X1 U17 ( .A1(N10), .A2(n11), .ZN(n10) );
  OR2_X1 U18 ( .A1(asset), .A2(count[0]), .Z(n11) );
  NAND2_X1 U19 ( .A1(N9), .A2(n12), .ZN(n9) );
  NAND2_X1 U20 ( .A1(n13), .A2(n14), .ZN(N10) );
  NAND2_X1 U21 ( .A1(n15), .A2(n12), .ZN(n14) );
  INV_X1 U22 ( .I(count[1]), .ZN(n12) );
  NOR2_X1 U23 ( .A1(reset), .A2(n16), .ZN(n15) );
  INV_X1 U24 ( .I(count[0]), .ZN(n16) );
  NAND2_X1 U25 ( .A1(count[1]), .A2(N9), .ZN(n13) );
  NOR2_X1 U26 ( .A1(count[0]), .A2(reset), .ZN(N9) );
endmodule

