
`timescale 1ns / 1ps

module fp2_hadamard  (input clk,rst,
                 input [254:0] x_re,
                 input [254:0] x_im,
                 input [254:0] y_re,
                 input [254:0] y_im,
                 input [254:0] z_re,
                 input [254:0] z_im,
                 input [254:0] t_re,
                 input [254:0] t_im,
                 output reg [254:0] out_x_re,
                 output reg [254:0] out_x_im,
                 output reg [254:0] out_y_re,
                 output reg [254:0] out_y_im,
                 output reg [254:0] out_z_re,
                 output reg [254:0] out_z_im,
                 output reg [254:0] out_t_re,
                 output reg [254:0] out_t_im);


parameter LATENCY_FP2_HADAMARD = 0 + 7 + 1 + 7 + 1;

reg [254:0] x_re_reg, x_im_reg, y_re_reg, y_im_reg, z_re_reg, z_im_reg, t_re_reg, t_im_reg;

wire [254:0] t1_re_out, t1_im_out, t2_re_out, t2_im_out, t3_re_out, t3_im_out, t4_re_out, t4_im_out;

reg [254:0] t1_re_reg, t1_im_reg, t2_re_reg, t2_im_reg, t3_re_reg, t3_im_reg, t4_re_reg, t4_im_reg;

wire [254:0] out1_re_out, out1_im_out, out2_re_out, out2_im_out, out3_re_out, out3_im_out, out4_re_out, out4_im_out;



always @(posedge clk or posedge rst) begin
    if (rst) begin
        x_re_reg <= 0; 
        x_im_reg <= 0;
        y_re_reg <= 0; 
        y_im_reg <= 0; 
        z_re_reg <= 0; 
        z_im_reg <= 0; 
        t_re_reg <= 0; 
        t_im_reg <= 0; 
    end else begin
        x_re_reg <= x_re;
        x_im_reg <= x_im;
        y_re_reg <= y_re;
        y_im_reg <= y_im;
        z_re_reg <= z_re;
        z_im_reg <= z_im;
        t_re_reg <= t_re;
        t_im_reg <= t_im;
    end
end


// STEP 1 //
fp2_add fp2_add_unit1 (
        .clk(clk),
        .rst(rst),
        .A1(x_re_reg),
        .B1(x_im_reg),
        .A2(y_re_reg),
        .B2(y_im_reg),
        .D1(t1_re_out),
        .D2(t1_im_out)
    );

fp2_sub fp2_sub_unit1 (
        .clk(clk),
        .rst(rst),
        .A1(x_re_reg),
        .B1(x_im_reg),
        .A2(y_re_reg),
        .B2(y_im_reg),
        .D1(t2_re_out),
        .D2(t2_im_out)
    );

fp2_add fp2_add_unit2 (
        .clk(clk),
        .rst(rst),
        .A1(z_re_reg),
        .B1(z_im_reg),
        .A2(t_re_reg),
        .B2(t_im_reg),
        .D1(t3_re_out),
        .D2(t3_im_out)
    );

fp2_sub fp2_sub_unit2 (
        .clk(clk),
        .rst(rst),
        .A1(z_re_reg),
        .B1(z_im_reg),
        .A2(t_re_reg),
        .B2(t_im_reg),
        .D1(t4_re_out),
        .D2(t4_im_out)
    );


always @(posedge clk) begin
    t1_re_reg <= t1_re_out;
    t1_im_reg <= t1_im_out;
    t2_re_reg <= t2_re_out;
    t2_im_reg <= t2_im_out;
    t3_re_reg <= t3_re_out;
    t3_im_reg <= t3_im_out;
    t4_re_reg <= t4_re_out;
    t4_im_reg <= t4_im_out;

end

// STEP 1 //


// STEP 2 //


fp2_add fp2_add_unit3 (
    .clk(clk),
    .rst(rst),
    .A1(t1_re_reg),
    .B1(t1_im_reg),
    .A2(t3_re_reg),
    .B2(t3_im_reg),
    .D1(out1_re_out),
    .D2(out1_im_out)
);

fp2_add fp2_add_unit4 (
    .clk(clk),
    .rst(rst),
    .A1(t2_re_reg),
    .B1(t2_im_reg),
    .A2(t4_re_reg),
    .B2(t4_im_reg),
    .D1(out2_re_out),
    .D2(out2_im_out)
);

fp2_sub fp2_sub_unit3 (
    .clk(clk),
    .rst(rst),
    .A1(t1_re_reg),
    .B1(t1_im_reg),
    .A2(t3_re_reg),
    .B2(t3_im_reg),
    .D1(out3_re_out),
    .D2(out3_im_out)
);

fp2_sub fp2_sub_unit4 (
    .clk(clk),
    .rst(rst),
    .A1(t2_re_reg),
    .B1(t2_im_reg),
    .A2(t4_re_reg),
    .B2(t4_im_reg),
    .D1(out4_re_out),
    .D2(out4_im_out)
);



// STEP 2 //

always @(posedge clk) begin
    out_x_re <= out1_re_out;
    out_x_im <= out1_im_out;
    out_y_re <= out2_re_out;
    out_y_im <= out2_im_out;
    out_z_re <= out3_re_out;
    out_z_im <= out3_im_out;
    out_t_re <= out4_re_out;
    out_t_im <= out4_im_out;

end


endmodule


