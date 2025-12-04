
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


module fp_sub  (input clk,rst,
                 input [254:0] A,
                 input [254:0] B,
                 output reg [254:0] D);


parameter LATENCY_SUB = 4;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg signed [255:0] sub, sub_new, sub_new2;

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
       sub <= 0; 
    end else begin
        sub <= A_reg - B_reg;
    end
end


always @(posedge clk or posedge rst) begin
    if(rst) begin
        sub_new <= 0;
    end
    else begin
        if (sub[255] == 1'b1) begin
            sub_new <= sub + q;
        end else begin
            sub_new <= sub;
        end
    end
end


always @(posedge clk or posedge rst) begin
    if(rst) begin
        sub_new2 <= 0;
    end
    else begin
        if (sub_new[255] == 1'b1) begin
            sub_new2 <= sub_new + q;
        end else begin
            sub_new2 <= sub_new;
        end
    end
end


always @(posedge clk) begin
    D <= $unsigned(sub_new2);
end
          
endmodule


