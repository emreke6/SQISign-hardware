
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/21/2024 10:40:22 AM
// Design Name: 
// Module Name: intmul32_64_top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module fp2_ptwise_sq    (input clk,rst,
                        input [254:0] A1,
                        input [254:0] B1,
                        input [254:0] A2,
                        input [254:0] B2,
                        input [254:0] A3,
                        input [254:0] B3,
                        input [254:0] A4,
                        input [254:0] B4,
                        output reg [254:0] D1_re,
                        output reg [254:0] D1_im,
                        output reg [254:0] D2_re,
                        output reg [254:0] D2_im,
                        output reg [254:0] D3_re,
                        output reg [254:0] D3_im,
                        output reg [254:0] D4_re,
                        output reg [254:0] D4_im);


parameter LATENCY_FP2_PTWISE_SQUARE = 0 + 5 + 1 + 9 + 1 + 2;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg [254:0] A1_reg, B1_reg, A2_reg, B2_reg, A3_reg, B3_reg, A4_reg, B4_reg;

wire [254:0] D1_re_out, D1_im_out, D2_re_out, D2_im_out, D3_re_out, D3_im_out, D4_re_out, D4_im_out;



always @(posedge clk or posedge rst) begin
    if (rst) begin
        A1_reg <= 0; 
        B1_reg <= 0; 
        A2_reg <= 0; 
        B2_reg <= 0; 
        A3_reg <= 0; 
        B3_reg <= 0; 
        A4_reg <= 0; 
        B4_reg <= 0; 
    end else begin
        A1_reg <= A1;
        B1_reg <= B1;
        A2_reg <= A2;
        B2_reg <= B2;
        A3_reg <= A3;
        B3_reg <= B3;
        A4_reg <= A4;
        B4_reg <= B4;
    end
end


// STAGE 1 //


fp2_sqr sp2_sqr_unit1(
    .clk(clk),
    .rst(rst),
    .A1(A1_reg),
    .B1(B1_reg),
    .D1(D1_re_out),
    .D2(D1_im_out)
);

fp2_sqr sp2_sqr_unit2(
    .clk(clk),
    .rst(rst),
    .A1(A2_reg),
    .B1(B2_reg),
    .D1(D2_re_out),
    .D2(D2_im_out)
);

fp2_sqr sp2_sqr_unit3(
    .clk(clk),
    .rst(rst),
    .A1(A3_reg),
    .B1(B3_reg),
    .D1(D3_re_out),
    .D2(D3_im_out)
);

fp2_sqr sp2_sqr_unit4(
    .clk(clk),
    .rst(rst),
    .A1(A4_reg),
    .B1(B4_reg),
    .D1(D4_re_out),
    .D2(D4_im_out)
);

// STAGE 1 //


always @(posedge clk) begin
    D1_re <= D1_re_out;
    D1_im <= D1_im_out;
    D2_re <= D2_re_out;
    D2_im <= D2_im_out;
    D3_re <= D3_re_out;
    D3_im <= D3_im_out;
    D4_re <= D4_re_out;
    D4_im <= D4_im_out;
end
          
endmodule


