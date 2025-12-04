
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


module fp2_to_squared_theta    (input clk,rst,
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


parameter LATENCY_FP2_TO_SQUARED_THETA = 0 + (0 + 5 + 1 + 9 + 1 + 2) + (0 + 7 + 1 + 7 + 1) + 4 ;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg [254:0] A1_reg, B1_reg, A2_reg, B2_reg, A3_reg, B3_reg, A4_reg, B4_reg;

wire [254:0] D1_re_out, D1_im_out, D2_re_out, D2_im_out, D3_re_out, D3_im_out, D4_re_out, D4_im_out;

reg [254:0] D1_re_sq_reg, D1_im_sq_reg, D2_re_sq_reg, D2_im_sq_reg, D3_re_sq_reg, D3_im_sq_reg, D4_re_sq_reg, D4_im_sq_reg;

wire [254:0] D1_re_sq_out, D1_im_sq_out, D2_re_sq_out, D2_im_sq_out, D3_re_sq_out, D3_im_sq_out, D4_re_sq_out, D4_im_sq_out;



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

fp2_ptwise_sq fp2_ptwise_sq_unit (
    .clk(clk),
    .rst(rst),
    .A1(A1_reg),
    .B1(B1_reg),
    .A2(A2_reg),
    .B2(B2_reg),
    .A3(A3_reg),
    .B3(B3_reg),
    .A4(A4_reg),
    .B4(B4_reg),

    .D1_re(D1_re_sq_out),
    .D1_im(D1_im_sq_out),
    .D2_re(D2_re_sq_out),
    .D2_im(D2_im_sq_out),
    .D3_re(D3_re_sq_out),
    .D3_im(D3_im_sq_out),
    .D4_re(D4_re_sq_out),
    .D4_im(D4_im_sq_out)
);



always @(posedge clk ) begin
    D1_re_sq_reg <= D1_re_sq_out;
    D1_im_sq_reg <= D1_im_sq_out;
    D2_re_sq_reg <= D2_re_sq_out;
    D2_im_sq_reg <= D2_im_sq_out;
    D3_re_sq_reg <= D3_re_sq_out;
    D3_im_sq_reg <= D3_im_sq_out;
    D4_re_sq_reg <= D4_re_sq_out;
    D4_im_sq_reg <= D4_im_sq_out;
end

// STAGE 1 //

// STAGE 2 //

fp2_hadamard hadamard_unit (
        .clk(clk),
        .rst(rst),
        .x_re(D1_re_sq_reg),
        .x_im(D1_im_sq_reg),
        .y_re(D2_re_sq_reg),
        .y_im(D2_im_sq_reg),
        .z_re(D3_re_sq_reg),
        .z_im(D3_im_sq_reg),
        .t_re(D4_re_sq_reg), 
        .t_im(D4_im_sq_reg),
        
        .out_x_re(D1_re_out),
        .out_x_im(D1_im_out),
        .out_y_re(D2_re_out),
        .out_y_im(D2_im_out),
        .out_z_re(D3_re_out),
        .out_z_im(D3_im_out),
        .out_t_re(D4_re_out), 
        .out_t_im(D4_im_out)
    );



// STAGE 2 //


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


