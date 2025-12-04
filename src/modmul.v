
`timescale 1ns / 1ps


module fp_mul(input clk,rst,
              input [254:0] A,
              input [254:0] B,
              output reg [254:0] D);


parameter LATENCY_MUL = 9;

reg [254:0] A_reg, B_reg;
reg [509:0] INTMUL_RES_reg;
wire [509:0] INTMUL_RES;
wire [254:0] MODRED_RES; 
 
always @(posedge clk or posedge rst) begin
    if(rst) begin
        A_reg <= 0;
        B_reg <= 0;
    end
    else begin
        A_reg <= A;
        B_reg <= B;
    end
end

intmul intmul_design (
    .clk(clk),
    .rst(rst),
    .A(A_reg),
    .B(B_reg),
    .D(INTMUL_RES)
);

always @(posedge clk ) begin
    INTMUL_RES_reg <= INTMUL_RES;
end

 modred modred_design (
    .clk(clk),
    .rst(rst),
    .A(INTMUL_RES_reg),
    .D(MODRED_RES)
);


always @(posedge clk) begin
    D <= MODRED_RES;
end
          
endmodule


