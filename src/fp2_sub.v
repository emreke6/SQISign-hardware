
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


module fp2_sub  (input clk,rst,
                 input [254:0] A1,
                 input [254:0] B1,
                 input [254:0] A2,
                 input [254:0] B2,
                 output reg [254:0] D1, 
                 output reg [254:0] D2);


parameter LATENCY_FP2_SUB = 6;

reg [254:0] A1_reg, A2_reg, B1_reg, B2_reg;

wire [254:0] D1_out, D2_out;



always @(posedge clk or posedge rst) begin
    if (rst) begin
       A1_reg <= 0; 
       A2_reg <= 0; 
       B1_reg <= 0; 
       B2_reg <= 0; 
    end else begin
        A1_reg <= A1;
        A2_reg <= A2;
        B1_reg <= B1;
        B2_reg <= B2;
    end
end



fp_sub fp_sub_unit1 (
        .clk(clk),
        .rst(rst),
        .A(A1_reg),
        .B(A2_reg),
        .D(D1_out)
    );

fp_sub fp_sub_unit2 (
        .clk(clk),
        .rst(rst),
        .A(B1_reg),
        .B(B2_reg),
        .D(D2_out)
    );



always @(posedge clk) begin
    D1 <= D1_out;
    D2 <= D2_out;
end
          
endmodule


