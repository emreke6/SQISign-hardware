`timescale 1ns/1ps

module fp2_to_squared_theta_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A1, A2, A3, A4;
    reg [254:0] B1, B2, B3, B4;
    wire [254:0] D1_re, D1_im, D2_re, D2_im, D3_re, D3_im, D4_re, D4_im;

    reg [254:0] RES1_re, RES1_im, RES2_re, RES2_im, RES3_re, RES3_im, RES4_re, RES4_im;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    fp2_to_squared_theta dut (
        .clk(clk),
        .rst(rst),
        .A1(A1),
        .B1(B1),
        .A2(A2),
        .B2(B2),
        .A3(A3),
        .B3(B3),
        .A4(A4),
        .B4(B4),
        .D1_re(D1_re),
        .D1_im(D1_im),
        .D2_re(D2_re),
        .D2_im(D2_im),
        .D3_re(D3_re),
        .D3_im(D3_im),
        .D4_re(D4_re),
        .D4_im(D4_im)
    );

    // ----------------------------------------------------
    // Clock generation (100 MHz → 10 ns period)
    // ----------------------------------------------------
    initial clk = 1;
    always #5 clk = ~clk;

    // ----------------------------------------------------
    // Reset logic
    // ----------------------------------------------------
    initial begin
        rst = 1;
        #20;
        rst = 0;
    end

    // ----------------------------------------------------
    // Stimulus
    // ----------------------------------------------------
    initial begin
        $display("==== STARTING fp2_to_squared_theta TESTBENCH ====");

        // Wait for reset deassertion
        @(negedge rst);

        // -------------------------
        // Test Vector 1
        // -------------------------
        
        @(posedge clk);
        
        
        A1 = 255'h3807ed85e85d8b3fbd5a293a18bb42f0912b8e383d833a9a269d132d5a5167b;
        B1 = 255'h127ba0471a1f3d76c58bca5bc731dd6f91ae57c60ea264fecde8b73482c3495;

        A2 = 255'h34e0b04174d94060cacc82cd69eee90e724fe81f8a43b14ccd8904ef5a965f9;
        B2 = 255'h37574a8b477caf2a5f274ab5c718332ee00fefa49e0c5518b2de38c133d33ea;

        A3 = 255'h8111a16abe13a48154940b369725839e90f4e986d3692ece9da0dd08b7eecc;
        B3 = 255'h269e99eea8bad8ba640c41182bc1ec23a2ce0c9b3123cbf4fc2afedb809cc36;

        A4 = 255'h12529317b325618341efef6b793653845c98a3f48661ccf0ac5106d9ffb2a93;
        B4 = 255'hd6fab372f6072170523a390c5c7e35a27a919f9e28777a4432021b36894cb6;
        
        

        @(posedge clk);

        A1 = 255'h38bf2b416940f343d38497ea608af494449e54e00a6579da613515f8e883cee;
        B1 = 255'h131d0edffd4160a190e4c80078a385f59c54579575448a12154612aa655a544;

        A2 = 255'h4a3420f6dd1c5a22a76d988b1cdca1f1ca913e23622150822e10c4e4b52971c;
        B2 = 255'h8b5d5d46ffff5c5b7b00cb022c09d8af6d8f6eea791f928a654bf985415de9;

        A3 = 255'h3922c3166bde56c2bf193bac104830f3966ae6b0dd290cbd62444db903b0c18;
        B3 = 255'h1bd03610beb29944f7f755af7807da11751ee1031c6605711455af250fdab58;

        A4 = 255'h3f9f671b384cbde907a94d6e5c1a6d8707d9e55b45dc6c73c015873d24a7671;
        B4 = 255'h154e3fdf82be4d68fd647f59e9d31709a736232727416e7ea68a7711184bb97;
        

        repeat(dut.LATENCY_FP2_TO_SQUARED_THETA - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1_re = 255'h34799a6e4a1eb2782f992a1589f22054499081ab327cfa443d7b819bc0d30c8;
        RES1_im = 255'h3a9f12ecc70faca1183ef64af660b7fac8a8aa52e4ca4955b283c255fc31282;
        $display("[T1] A=%h, B=%h, D1_re=%h", A1, B1, D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", A1, B1, D1_im);
        $display("CONTROL x_im %d", D1_re == RES1_re);
        $display("CONTROL x_re %d", D1_im == RES1_im);

        RES2_re = 255'h366cf39f0562cb4eae22bf35461c7626c2e6faf458335c9fad9b20df27d3cff;
        RES2_im = 255'h4e5a17f9bc7e77fb2c574101ed41cdbacb6a4955757ce89884fa4e8d4368ec8;
        $display("[T1] A=%h, B=%h, D2_re=%h", A2, B2, D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", A2, B2, D2_im);
        $display("CONTROL y_im %d", D2_re == RES2_re);
        $display("CONTROL y_re %d", D2_im == RES2_im);

        RES3_re = 255'heb440a8a2962099eb946fbab77058479c1fe471268f8de35335bf2ec0136d;
        RES3_im = 255'h38522385c9fb751fe8ef80fd47846e1de69f5e576b6b1f6787279ee7deb2fe5;
        $display("[T1] A=%h, B=%h, D3_re=%h", A3, B3, D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", A3, B3, D3_im);
        $display("CONTROL z_im %d", D3_re == RES3_re);
        $display("CONTROL z_re %d", D3_im == RES3_im);

        RES4_re = 255'h349f6c39c5e988967de6ec13d3306cfabb30bba9158f10bdde24ed6ccfe4b51;
        RES4_im = 255'h1b7b29f444ea783cd27ee3f26d1b3442625536a04a9ffc5fb8affeff9311479;
        $display("[T1] A=%h, B=%h, D4_re=%h", A4, B4, D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", A4, B4, D4_im);
        $display("CONTROL t_im %d", D4_re == RES4_re);
        $display("CONTROL t_re %d", D4_im == RES4_im);

        @(posedge clk);
        #1;

        RES1_re = 255'h5b8106b995a9561c0c65d1bac1b452e7b4e9aefda3c5f0d9329341686bb21ea;
        RES1_im = 255'h3f3ba8ecf29fc1b224ff365d3d47e20ceb6ac40d9be1f536b51253520314c6c;
        $display("[T1] A=%h, B=%h, D1_re=%h", A1, B1, D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", A1, B1, D1_im);
        $display("CONTROL x_im %d", D1_re == RES1_re);
        $display("CONTROL x_re %d", D1_im == RES1_im);

        RES2_re = 255'h664f48908e5af75c37643fd992646e711079ffb678605cdbcdf37a2c884aad3;
        RES2_im = 255'h7df90e9a180e4e9352d053e4be2e2c4362dd1de17a91a11319dbce68ee42901;
        $display("[T1] A=%h, B=%h, D2_re=%h", A2, B2, D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", A2, B2, D2_im);
        $display("CONTROL y_im %d", D2_re == RES2_re);
        $display("CONTROL y_re %d", D2_im == RES2_im);

        RES3_re = 255'h3e34a6f2e84a1b7718af5a38c683942dacb86b914bb61673927116b90002828;
        RES3_im = 255'h392b30493d1aced1c01c93d2b920e7755a61731e6b60020663b2e666f705408;
        $display("[T1] A=%h, B=%h, D3_re=%h", A3, B3, D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", A3, B3, D3_im);
        $display("CONTROL z_im %d", D3_re == RES3_re);
        $display("CONTROL z_re %d", D3_im == RES3_im);

        RES4_re = 255'h2daaee52c26170938393fb9daa1a93df99591977ac56df316fd59bbb99845f4;
        RES4_im = 255'h6a53ed17cee23f1d549ad4cf3ac8c916ec9b1845f3a5bc33b1ea69dcfeab47;
        $display("[T1] A=%h, B=%h, D4_re=%h", A4, B4, D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", A4, B4, D4_im);
        $display("CONTROL t_im %d", D4_re == RES4_re);
        $display("CONTROL t_re %d", D4_im == RES4_im);




        

        $display("==== FINISHED fp2_to_squared_theta TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
