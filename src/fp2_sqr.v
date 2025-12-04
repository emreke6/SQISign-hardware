
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


module fp2_sqr  (input clk,rst,
                 input [254:0] A1,
                 input [254:0] B1,
                 output reg [254:0] D1,
                 output reg [254:0] D2);


parameter LATENCY_FP2_SQR = 0 + 5 + 1 + 9 + 1;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg [254:0] A1_reg, B1_reg, im_part_pre_im_reg, sum_reg, diff_reg;

wire [254:0] D1_out, D2_out, sum_, diff_, im_part_pre_im_out, im_part_out, re_part_out;



always @(posedge clk or posedge rst) begin
    if (rst) begin
        A1_reg <= 0; 
        B1_reg <= 0; 
    end else begin
        A1_reg <= A1;
        B1_reg <= B1;
    end
end


// STAGE 1 //


fp_add fp_add_unit1 (
        .clk(clk),
        .rst(rst),
        .A(A1_reg),
        .B(B1_reg),
        .D(sum_)
    );

fp_sub fp_sub_unit1 (
        .clk(clk),
        .rst(rst),
        .A(A1_reg),
        .B(B1_reg),
        .D(diff_)
    );

fp_mul fp_mul_unit (
        .clk(clk),
        .rst(rst),
        .A(A1_reg),
        .B(B1_reg),
        .D(im_part_pre_im_out)
    );

always @(negedge clk ) begin
    im_part_pre_im_reg <= im_part_pre_im_out;
    sum_reg <= sum_;
    diff_reg <= diff_;

end

// STAGE 1 //


// STAGE 2 //

fp_mul fp_mul_unit2 (
        .clk(clk),
        .rst(rst),
        .A(sum_reg),
        .B(diff_reg),
        .D(re_part_out)
    );

fp_add fp_add_unit2 (
        .clk(clk),
        .rst(rst),
        .A(im_part_pre_im_reg),
        .B(im_part_pre_im_reg),
        .D(im_part_out)
    );



// STAGE 2 //



always @(posedge clk) begin
    D1 <= re_part_out;
    D2 <= im_part_out;
end
          
endmodule


