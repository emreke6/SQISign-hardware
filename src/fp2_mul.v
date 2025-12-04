
`timescale 1ns / 1ps

module fp2_mul  (input clk,rst,
                 input [254:0] y_re,
                 input [254:0] y_im,
                 input [254:0] z_re,
                 input [254:0] z_im,
                 output reg [254:0] x_re, 
                 output reg [254:0] x_im);


parameter LATENCY_FP2_MUL = 0 + 5 + 1 + 9 + 1 + 5 + 1 + 5 + 1 + 1;

reg [254:0] y_re_reg, y_im_reg, z_re_reg, z_im_reg, y_re_d5_reg, y_im_d5_reg, z_re_d5_reg, z_im_d5_reg;
reg [254:0] karat_add1_out_reg, karat_add2_out_reg, t0_reg, t1_reg, x_re_precomp_reg, x_im_precomp_reg, x_im_precomp_reg_d1;
reg [254:0] t1_d5_reg, x_re_precomp_reg_d5_reg;

wire [254:0] karat_add1_out, karat_add2_out, t0_out, t1_out, x_re_precomp_out, x_im_precomp_out;
wire [254:0] t1_d5, x_re_precomp_reg_d5, x_re_precomp_reg_d7, x_re_out, x_im_out;

wire [254:0] y_re_d5, y_im_d5, z_re_d5, z_im_d5;



always @(posedge clk or posedge rst) begin
    if (rst) begin
        y_re_reg <= 0; 
        y_im_reg <= 0; 
        z_re_reg <= 0; 
        z_im_reg <= 0; 
    end else begin
        y_re_reg <= y_re;
        y_im_reg <= y_im;
        z_re_reg <= z_re;
        z_im_reg <= z_im;
    end
end


// KARATSUBA STEP 1 //


fp_add fp_add_unit1 (
        .clk(clk),
        .rst(rst),
        .A(y_re_reg),
        .B(y_im_reg),
        .D(karat_add1_out)
    );

fp_add fp_add_unit2 (
        .clk(clk),
        .rst(rst),
        .A(z_re_reg),
        .B(z_im_reg),
        .D(karat_add2_out)
    );


shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_y_re (
    .clk     (clk       ),
    .reset   (1'b0      ),
    .data_in (y_re_reg  ),
    .data_out(y_re_d5   )
);

shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_y_im (
    .clk     (clk       ),
    .reset   (1'b0      ),
    .data_in (y_im_reg  ),
    .data_out(y_im_d5   )
);

shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_z_re (
    .clk     (clk       ),
    .reset   (1'b0      ),
    .data_in (z_re_reg  ),
    .data_out(z_re_d5   )
);

shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_z_im (
    .clk     (clk       ),
    .reset   (1'b0      ),
    .data_in (z_im_reg  ),
    .data_out(z_im_d5   )
);

always @(posedge clk) begin
    karat_add1_out_reg <= karat_add1_out;
    karat_add2_out_reg <= karat_add2_out;
    y_re_d5_reg <= y_re_d5;
    y_im_d5_reg <= y_im_d5;
    z_re_d5_reg <= z_re_d5;
    z_im_d5_reg <= z_im_d5;

end

// KARATSUBA STEP 1 //


// KARATSUBA STEP 2 //

fp_mul t0_mul (
    .clk(clk),
    .rst(rst),
    .A(karat_add1_out_reg),
    .B(karat_add2_out_reg),
    .D(t0_out)
);

fp_mul t1_mul (
    .clk(clk),
    .rst(rst),
    .A(y_im_d5_reg),
    .B(z_im_d5_reg),
    .D(t1_out)
);

fp_mul x_re_precomp_mul (
    .clk(clk),
    .rst(rst),
    .A(y_re_d5_reg),
    .B(z_re_d5_reg),
    .D(x_re_precomp_out)
);

always @(posedge clk) begin
    t0_reg <= t0_out;
    t1_reg <= t1_out;
    x_re_precomp_reg <= x_re_precomp_out;
end


// KARATSUBA STEP 2 //

// KARATSUBA STEP 3 //

fp_sub fp_sub_unit1 (
        .clk(clk),
        .rst(rst),
        .A(t0_reg),
        .B(t1_reg),
        .D(x_im_precomp_out)
    );


shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_t1 (
    .clk     (clk       ),
    .reset   (1'b0      ),
    .data_in (t1_reg    ),
    .data_out(t1_d5     )
);

shiftreg #(
    .SHIFT(5),
    .DATA (255      )
) shift_x_precomp (
    .clk     (clk                   ),
    .reset   (1'b0                  ),
    .data_in (x_re_precomp_reg      ),
    .data_out(x_re_precomp_reg_d5   )
);

always @(posedge clk) begin
    x_im_precomp_reg <= x_im_precomp_out;
    x_re_precomp_reg_d5_reg <= x_re_precomp_reg_d5;
    t1_d5_reg <= t1_d5;
end


// KARATSUBA STEP 3 //

// KARATSUBA STEP 4 //

fp_sub fp_sub_x_re (
        .clk(clk),
        .rst(rst),
        .A(x_re_precomp_reg_d5_reg),
        .B(t1_d5_reg),
        .D(x_re_out)
    );

fp_sub fp_sub_x_im (
        .clk(clk),
        .rst(rst),
        .A(x_im_precomp_reg),
        .B(x_re_precomp_reg_d5_reg),
        .D(x_im_out)
    );

always @(posedge clk) begin
    x_re <= x_re_out;
    x_im <= x_im_out;
end

// KARATSUBA STEP 4 //









          
endmodule


