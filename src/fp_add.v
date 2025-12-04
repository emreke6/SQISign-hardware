
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


module fp_add  (input clk,rst,
                 input [254:0] A,
                 input [254:0] B,
                 output reg [254:0] D);


parameter LATENCY_ADD = 4;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg [254:0] sum, sum_new, sum_new2;


reg [254:0] A_reg, B_reg;


always @(posedge clk or posedge rst) begin
    if (rst) begin
        A_reg <= 0; 
        B_reg <= 0; 
    end else begin
        A_reg <= A;
        B_reg <= B; 
    end
end


always @(posedge clk or posedge rst) begin
    if (rst) begin
       sum <= 0; 
    end else begin
        sum <= A_reg + B_reg;
    end
end


always @(posedge clk or posedge rst) begin
    if(rst) begin
        sum_new <= 0;
    end
    else begin
        if (sum[254:251] >= 1'd1) begin
            sum_new <= sum - q;
        end else begin
            sum_new <= sum;
        end
    end
end


always @(posedge clk or posedge rst) begin
    if(rst) begin
        sum_new2 <= 0;
    end
    else begin
        if (sum_new[254:251] >= 1'd1) begin
            sum_new2 <= sum_new - q;
        end else begin
            sum_new2 <= sum_new;
        end
    end
end


always @(posedge clk) begin
    D <= sum_new2;
end
          
endmodule


