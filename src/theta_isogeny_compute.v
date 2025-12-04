
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


module theta_isogeny_compute    (input clk,rst,
                                input [254:0] TT1_A1,
                                input [254:0] TT1_B1,
                                input [254:0] TT1_A2,
                                input [254:0] TT1_B2,
                                input [254:0] TT1_A3,
                                input [254:0] TT1_B3,
                                input [254:0] TT1_A4,
                                input [254:0] TT1_B4,

                                input [254:0] TT2_A1,
                                input [254:0] TT2_B1,
                                input [254:0] TT2_A2,
                                input [254:0] TT2_B2,
                                input [254:0] TT2_A3,
                                input [254:0] TT2_B3,
                                input [254:0] TT2_A4,
                                input [254:0] TT2_B4,

                                output reg [254:0] PRECOMP_D1_re,
                                output reg [254:0] PRECOMP_D1_im,
                                output reg [254:0] PRECOMP_D2_re,
                                output reg [254:0] PRECOMP_D2_im,
                                output reg [254:0] PRECOMP_D3_re,
                                output reg [254:0] PRECOMP_D3_im,
                                output reg [254:0] PRECOMP_D4_re,
                                output reg [254:0] PRECOMP_D4_im,

                                output reg [254:0] NULL_POINT_D1_re,
                                output reg [254:0] NULL_POINT_D1_im,
                                output reg [254:0] NULL_POINT_D2_re,
                                output reg [254:0] NULL_POINT_D2_im,
                                output reg [254:0] NULL_POINT_D3_re,
                                output reg [254:0] NULL_POINT_D3_im,
                                output reg [254:0] NULL_POINT_D4_re,
                                output reg [254:0] NULL_POINT_D4_im
                                );


parameter LATENCY_THETA_ISOGENY_COMPUTE = 120;


reg [254:0] q = 255'd2261564242916331941866620800950935700259179388000792266395655937654553313279;

reg [254:0] TT1_A1_reg, TT1_B1_reg, TT1_A2_reg, TT1_B2_reg, TT1_A3_reg, TT1_B3_reg, TT1_A4_reg, TT1_B4_reg, TT2_A1_reg, TT2_B1_reg, TT2_A2_reg, TT2_B2_reg, TT2_A3_reg, TT2_B3_reg, TT2_A4_reg, TT2_B4_reg;

wire [254:0] TT1_D1_re_out, TT1_D1_im_out, TT1_D2_re_out, TT1_D2_im_out, TT1_D3_re_out, TT1_D3_im_out, TT1_D4_re_out, TT1_D4_im_out, TT2_D1_re_out, TT2_D1_im_out, TT2_D2_re_out, TT2_D2_im_out, TT2_D3_re_out, TT2_D3_im_out, TT2_D4_re_out, TT2_D4_im_out;

reg [254:0] TT1_D1_re_reg, TT1_D1_im_reg, TT1_D2_re_reg, TT1_D2_im_reg, TT1_D3_re_reg, TT1_D3_im_reg, TT1_D4_re_reg, TT1_D4_im_reg, TT2_D1_re_reg, TT2_D1_im_reg, TT2_D2_re_reg, TT2_D2_im_reg, TT2_D3_re_reg, TT2_D3_im_reg, TT2_D4_re_reg, TT2_D4_im_reg;

wire [254:0] t1_re_out, t1_im_out,  t2_re_out, t2_im_out,  t3_re_out, t3_im_out;

reg [254:0] t1_re_reg, t1_im_reg, t2_re_reg, t2_im_reg, t3_re_reg, t3_im_reg;  

wire [254:0] TT1_D1_re_reg_d30, TT1_D1_im_reg_d30, TT1_D2_re_reg_d30, TT1_D2_im_reg_d30;
wire [254:0] TT2_D1_re_reg_d30, TT2_D1_im_reg_d30, TT2_D2_re_reg_d30, TT2_D2_im_reg_d30, TT2_D3_re_reg_d30, TT2_D3_im_reg_d30, TT2_D4_re_reg_d30, TT2_D4_im_reg_d30;

reg [254:0] TT1_D1_re_reg_d30_in, TT1_D1_im_reg_d30_in, TT1_D2_re_reg_d30_in, TT1_D2_im_reg_d30_in;
reg [254:0] TT2_D1_re_reg_d30_in, TT2_D1_im_reg_d30_in, TT2_D2_re_reg_d30_in, TT2_D2_im_reg_d30_in, TT2_D3_re_reg_d30_in, TT2_D3_im_reg_d30_in, TT2_D4_re_reg_d30_in, TT2_D4_im_reg_d30_in;


wire [254:0] null_point_x_re_out, null_point_x_im_out, null_point_y_re_out, null_point_y_im_out, null_point_z_re_out, null_point_z_im_out, null_point_t_re_out, null_point_t_im_out;
wire [254:0] precomp_x_re_out, precomp_x_im_out, precomp_y_re_out, precomp_y_im_out;

reg [254:0] null_point_x_re_reg, null_point_x_im_reg, null_point_y_re_reg, null_point_y_im_reg, null_point_z_re_reg, null_point_z_im_reg, null_point_t_re_reg, null_point_t_im_reg;

reg [254:0] precomp_x_re_reg, precomp_x_im_reg, precomp_y_re_reg, precomp_y_im_reg, precomp_z_re_reg, precomp_z_im_reg, precomp_t_re_reg, precomp_t_im_reg;
wire [254:0] precomp_x_re_reg_d17, precomp_x_im_reg_d17, precomp_y_re_reg_d17, precomp_y_im_reg_d17, precomp_z_re_reg_d17, precomp_z_im_reg_d17, precomp_t_re_reg_d17, precomp_t_im_reg_d17;


wire [254:0] null_point_x_hdm_re_out, null_point_x_hdm_im_out, null_point_y_hdm_re_out, null_point_y_hdm_im_out, null_point_z_hdm_re_out, null_point_z_hdm_im_out, null_point_t_hdm_re_out, null_point_t_hdm_im_out;

always @(posedge clk or posedge rst) begin
    if (rst) begin
        TT1_A1_reg <= 0; 
        TT1_B1_reg <= 0; 
        TT1_A2_reg <= 0; 
        TT1_B2_reg <= 0; 
        TT1_A3_reg <= 0; 
        TT1_B3_reg <= 0; 
        TT1_A4_reg <= 0; 
        TT1_B4_reg <= 0; 

        TT2_A1_reg <= 0; 
        TT2_B1_reg <= 0; 
        TT2_A2_reg <= 0; 
        TT2_B2_reg <= 0; 
        TT2_A3_reg <= 0; 
        TT2_B3_reg <= 0; 
        TT2_A4_reg <= 0; 
        TT2_B4_reg <= 0; 
    end else begin
        TT1_A1_reg <= TT1_A1;
        TT1_B1_reg <= TT1_B1;
        TT1_A2_reg <= TT1_A2;
        TT1_B2_reg <= TT1_B2;
        TT1_A3_reg <= TT1_A3;
        TT1_B3_reg <= TT1_B3;
        TT1_A4_reg <= TT1_A4;
        TT1_B4_reg <= TT1_B4;

        TT2_A1_reg <= TT2_A1;
        TT2_B1_reg <= TT2_B1;
        TT2_A2_reg <= TT2_A2;
        TT2_B2_reg <= TT2_B2;
        TT2_A3_reg <= TT2_A3;
        TT2_B3_reg <= TT2_B3;
        TT2_A4_reg <= TT2_A4;
        TT2_B4_reg <= TT2_B4;
    end
end


// STAGE 1 //

fp2_to_squared_theta to_sqr_theta_unit1 (
        .clk(clk),
        .rst(rst),

        .A1(TT1_A1_reg),
        .B1(TT1_B1_reg),
        .A2(TT1_A2_reg),
        .B2(TT1_B2_reg),
        .A3(TT1_A3_reg),
        .B3(TT1_B3_reg),
        .A4(TT1_A4_reg),
        .B4(TT1_B4_reg),

        .D1_re(TT1_D1_re_out),
        .D1_im(TT1_D1_im_out),
        .D2_re(TT1_D2_re_out),
        .D2_im(TT1_D2_im_out),
        .D3_re(TT1_D3_re_out),
        .D3_im(TT1_D3_im_out),
        .D4_re(TT1_D4_re_out),
        .D4_im(TT1_D4_im_out)
    );

fp2_to_squared_theta to_sqr_theta_unit2 (
        .clk(clk),
        .rst(rst),

        .A1(TT2_A1_reg),
        .B1(TT2_B1_reg),
        .A2(TT2_A2_reg),
        .B2(TT2_B2_reg),
        .A3(TT2_A3_reg),
        .B3(TT2_B3_reg),
        .A4(TT2_A4_reg),
        .B4(TT2_B4_reg),
        
        .D1_re(TT2_D1_re_out),
        .D1_im(TT2_D1_im_out),
        .D2_re(TT2_D2_re_out),
        .D2_im(TT2_D2_im_out),
        .D3_re(TT2_D3_re_out),
        .D3_im(TT2_D3_im_out),
        .D4_re(TT2_D4_re_out),
        .D4_im(TT2_D4_im_out)
    );

always @(posedge clk) begin
    TT1_D1_re_reg <= TT1_D1_re_out;
    TT1_D1_im_reg <= TT1_D1_im_out;
    TT1_D2_re_reg <= TT1_D2_re_out;
    TT1_D2_im_reg <= TT1_D2_im_out;
    TT1_D3_re_reg <= TT1_D3_re_out;
    TT1_D3_im_reg <= TT1_D3_im_out;
    TT1_D4_re_reg <= TT1_D4_re_out;
    TT1_D4_im_reg <= TT1_D4_im_out;

    TT2_D1_re_reg <= TT2_D1_re_out;
    TT2_D1_im_reg <= TT2_D1_im_out;
    TT2_D2_re_reg <= TT2_D2_re_out;
    TT2_D2_im_reg <= TT2_D2_im_out;
    TT2_D3_re_reg <= TT2_D3_re_out;
    TT2_D3_im_reg <= TT2_D3_im_out;
    TT2_D4_re_reg <= TT2_D4_re_out;
    TT2_D4_im_reg <= TT2_D4_im_out;
end

// STAGE 1 //

// STAGE 2 //

fp2_mul fp2_mul_t1 (
        .clk(clk),
        .rst(rst),
        .y_re(TT1_D1_re_reg),
        .y_im(TT1_D1_im_reg),
        .z_re(TT2_D2_re_reg),
        .z_im(TT2_D2_im_reg),
        .x_re(t1_re_out), 
        .x_im(t1_im_out)
    );

fp2_mul fp2_mul_t2 (
        .clk(clk),
        .rst(rst),
        .y_re(TT1_D2_re_reg),
        .y_im(TT1_D2_im_reg),
        .z_re(TT2_D1_re_reg),
        .z_im(TT2_D1_im_reg),
        .x_re(t2_re_out), 
        .x_im(t2_im_out)
    );

fp2_mul fp2_mul_t3 (
        .clk(clk),
        .rst(rst),
        .y_re(TT2_D3_re_reg),
        .y_im(TT2_D3_im_reg),
        .z_re(TT2_D4_re_reg),
        .z_im(TT2_D4_im_reg),
        .x_re(t3_re_out), 
        .x_im(t3_im_out)
    );

always @(posedge clk ) begin
    t1_re_reg <= t1_re_out;
    t1_im_reg <= t1_im_out;
    t2_re_reg <= t2_re_out;
    t2_im_reg <= t2_im_out;
    t3_re_reg <= t3_re_out;
    t3_im_reg <= t3_im_out;
end

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT1_x_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT1_D1_re_reg  ),
    .data_out(TT1_D1_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT1_x_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT1_D1_im_reg  ),
    .data_out(TT1_D1_im_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT1_y_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT1_D2_re_reg  ),
    .data_out(TT1_D2_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT1_y_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT1_D2_im_reg  ),
    .data_out(TT1_D2_im_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_x_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D1_re_reg  ),
    .data_out(TT2_D1_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_x_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D1_im_reg  ),
    .data_out(TT2_D1_im_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_y_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D2_re_reg  ),
    .data_out(TT2_D2_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_y_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D2_im_reg  ),
    .data_out(TT2_D2_im_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_z_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D3_re_reg  ),
    .data_out(TT2_D3_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_z_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D3_im_reg  ),
    .data_out(TT2_D3_im_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_t_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D4_re_reg  ),
    .data_out(TT2_D4_re_reg_d30   )
);

shiftreg #(
    .SHIFT(30),
    .DATA (255      )
) shift_TT2_t_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (TT2_D4_im_reg  ),
    .data_out(TT2_D4_im_reg_d30   )
);

always @(posedge clk ) begin
    TT1_D1_re_reg_d30_in <= TT1_D1_re_reg_d30;
    TT1_D1_im_reg_d30_in <= TT1_D1_im_reg_d30;
    TT1_D2_re_reg_d30_in <= TT1_D2_re_reg_d30;
    TT1_D2_im_reg_d30_in <= TT1_D2_im_reg_d30;

    TT2_D1_re_reg_d30_in <= TT2_D1_re_reg_d30;
    TT2_D1_im_reg_d30_in <= TT2_D1_im_reg_d30;
    TT2_D2_re_reg_d30_in <= TT2_D2_re_reg_d30;
    TT2_D2_im_reg_d30_in <= TT2_D2_im_reg_d30;
    TT2_D3_re_reg_d30_in <= TT2_D3_re_reg_d30;
    TT2_D3_im_reg_d30_in <= TT2_D3_im_reg_d30;
    TT2_D4_re_reg_d30_in <= TT2_D4_re_reg_d30;
    TT2_D4_im_reg_d30_in <= TT2_D4_im_reg_d30;
end



// STAGE 2 //

fp2_mul fp2_mul_null_point_x (
        .clk(clk),
        .rst(rst),
        .y_re(TT2_D1_re_reg_d30_in),
        .y_im(TT2_D1_im_reg_d30_in),
        .z_re(t1_re_reg),
        .z_im(t1_im_reg),
        .x_re(null_point_x_re_out), 
        .x_im(null_point_x_im_out)
    );


fp2_mul fp2_mul_null_point_y (
        .clk(clk),
        .rst(rst),
        .y_re(TT2_D2_re_reg_d30_in),
        .y_im(TT2_D2_im_reg_d30_in),
        .z_re(t2_re_reg),
        .z_im(t2_im_reg),
        .x_re(null_point_y_re_out), 
        .x_im(null_point_y_im_out)
    );

fp2_mul fp2_mul_null_point_z (
        .clk(clk),
        .rst(rst),
        .y_re(TT2_D3_re_reg_d30_in),
        .y_im(TT2_D3_im_reg_d30_in),
        .z_re(t1_re_reg),
        .z_im(t1_im_reg),
        .x_re(null_point_z_re_out), 
        .x_im(null_point_z_im_out)
    );

fp2_mul fp2_mul_null_point_t (
        .clk(clk),
        .rst(rst),
        .y_re(TT2_D4_re_reg_d30_in),
        .y_im(TT2_D4_im_reg_d30_in),
        .z_re(t2_re_reg),
        .z_im(t2_im_reg),
        .x_re(null_point_t_re_out), 
        .x_im(null_point_t_im_out)
    );

fp2_mul fp2_mul_precomp_x (
        .clk(clk),
        .rst(rst),
        .y_re(t3_re_reg),
        .y_im(t3_im_reg),
        .z_re(TT1_D2_re_reg_d30_in),
        .z_im(TT1_D2_im_reg_d30_in),
        .x_re(precomp_x_re_out), 
        .x_im(precomp_x_im_out)
    );

fp2_mul fp2_mul_precomp_y (
        .clk(clk),
        .rst(rst),
        .y_re(t3_re_reg),
        .y_im(t3_im_reg),
        .z_re(TT1_D1_re_reg_d30_in),
        .z_im(TT1_D1_im_reg_d30_in),
        .x_re(precomp_y_re_out), 
        .x_im(precomp_y_im_out)
    );


always @(posedge clk ) begin
    null_point_x_re_reg <= null_point_x_re_out;
    null_point_x_im_reg <= null_point_x_im_out;
    null_point_y_re_reg <= null_point_y_re_out;
    null_point_y_im_reg <= null_point_y_im_out;
    null_point_z_re_reg <= null_point_z_re_out;
    null_point_z_im_reg <= null_point_z_im_out;
    null_point_t_re_reg <= null_point_t_re_out;
    null_point_t_im_reg <= null_point_t_im_out;

    precomp_x_re_reg <= precomp_x_re_out;
    precomp_x_im_reg <= precomp_x_im_out;
    precomp_y_re_reg <= precomp_y_re_out;
    precomp_y_im_reg <= precomp_y_im_out;
    precomp_z_re_reg <= null_point_t_re_out;
    precomp_z_im_reg <= null_point_t_im_out;
    precomp_t_re_reg <= null_point_z_re_out;
    precomp_t_im_reg <= null_point_z_im_out;

end

// STAGE 2 //

// STAGE 3 //

fp2_hadamard hadamard_unit (
        .clk(clk),
        .rst(rst),
        .x_re(null_point_x_re_reg),
        .x_im(null_point_x_im_reg),
        .y_re(null_point_y_re_reg),
        .y_im(null_point_y_im_reg),
        .z_re(null_point_z_re_reg),
        .z_im(null_point_z_im_reg),
        .t_re(null_point_t_re_reg), 
        .t_im(null_point_t_im_reg),
        
        .out_x_re(null_point_x_hdm_re_out),
        .out_x_im(null_point_x_hdm_im_out),
        .out_y_re(null_point_y_hdm_re_out),
        .out_y_im(null_point_y_hdm_im_out),
        .out_z_re(null_point_z_hdm_re_out),
        .out_z_im(null_point_z_hdm_im_out),
        .out_t_re(null_point_t_hdm_re_out), 
        .out_t_im(null_point_t_hdm_im_out)
    );

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_x_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_x_re_reg  ),
    .data_out(precomp_x_re_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_x_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_x_im_reg  ),
    .data_out(precomp_x_im_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_y_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_y_re_reg  ),
    .data_out(precomp_y_re_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_y_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_y_im_reg  ),
    .data_out(precomp_y_im_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_z_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_z_re_reg  ),
    .data_out(precomp_z_re_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_z_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_z_im_reg  ),
    .data_out(precomp_z_im_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_t_re (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_t_re_reg  ),
    .data_out(precomp_t_re_reg_d17   )
);

shiftreg #(
    .SHIFT(17),
    .DATA (255      )
) shift_precomp_t_im (
    .clk     (clk           ),
    .reset   (1'b0          ),
    .data_in (precomp_t_im_reg  ),
    .data_out(precomp_t_im_reg_d17   )
);


// STAGE 3 //





// LAST STAGE //

always @(posedge clk ) begin
    PRECOMP_D1_re <= precomp_x_re_reg_d17;
    PRECOMP_D1_im <= precomp_x_im_reg_d17;
    PRECOMP_D2_re <= precomp_y_re_reg_d17;
    PRECOMP_D2_im <= precomp_y_im_reg_d17;
    PRECOMP_D3_re <= precomp_z_re_reg_d17;
    PRECOMP_D3_im <= precomp_z_im_reg_d17;
    PRECOMP_D4_re <= precomp_t_re_reg_d17;
    PRECOMP_D4_im <= precomp_t_im_reg_d17;

    NULL_POINT_D1_re <= null_point_x_hdm_re_out;
    NULL_POINT_D1_im <= null_point_x_hdm_im_out;
    NULL_POINT_D2_re <= null_point_y_hdm_re_out;
    NULL_POINT_D2_im <= null_point_y_hdm_im_out;
    NULL_POINT_D3_re <= null_point_z_hdm_re_out;
    NULL_POINT_D3_im <= null_point_z_hdm_im_out;
    NULL_POINT_D4_re <= null_point_t_hdm_re_out;
    NULL_POINT_D4_im <= null_point_t_hdm_im_out;
    

end
          
endmodule


