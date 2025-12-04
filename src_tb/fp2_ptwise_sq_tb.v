`timescale 1ns/1ps

module fp2_ptwise_sq_tb;

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
    fp2_ptwise_sq dut (
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
        $display("==== STARTING fp2_sqr TESTBENCH ====");

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
        

        repeat(dut.LATENCY_FP2_PTWISE_SQUARE - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1_re = 255'h3c1c4f9467e51a19be97071693ad823e905a8da3ecaa181fff9bbaf6a923321;
        RES1_im = 255'h37319e18249d047e4001270f26108a057741e2280414936d5dd56bb2ac5796a;
        $display("[T1] A=%h, B=%h, D1_re=%h", A1, B1, D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", A1, B1, D1_im);
        $display("CONTROL x_im %d", D1_re == RES1_re);
        $display("CONTROL x_re %d", D1_im == RES1_im);

        RES2_re = 255'h6961fa8023ef02728923172070710add14eb25535c8e17139bbb3d0ad46ef9;
        RES2_im = 255'h7a46fd2123e88c6240961494f8e20906e062222d240620f13f0044ec411a7c8;
        $display("[T1] A=%h, B=%h, D2_re=%h", A2, B2, D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", A2, B2, D2_im);
        $display("CONTROL y_im %d", D2_re == RES2_re);
        $display("CONTROL y_re %d", D2_im == RES2_im);

        RES3_re = 255'h2156f7723fdba4c9b046ed8ed459c8fef5e130abd8ae1351f5ef9646cb303c2;
        RES3_im = 255'h5d4af75b1d2a0dcfe249f4974bc0b8d552c797ac290f0589bde99cbef37573a;
        $display("[T1] A=%h, B=%h, D3_re=%h", A3, B3, D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", A3, B3, D3_im);
        $display("CONTROL z_im %d", D3_re == RES3_re);
        $display("CONTROL z_re %d", D3_im == RES3_im);

        RES4_re = 255'h207033bfa01f036d982903fe1ae3c468f2061106375bed610e347c8d9f38aeb;
        RES4_im = 255'h6bdb805861600df0b55dc60f8bad6c191e3d0e5193a08f6d57c474f81b49a12;
        $display("[T1] A=%h, B=%h, D4_re=%h", A4, B4, D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", A4, B4, D4_im);
        $display("CONTROL t_im %d", D4_re == RES4_re);
        $display("CONTROL t_re %d", D4_im == RES4_im);

        @(posedge clk);
        #1;

        RES1_re = 255'hf6bf923f3abf660b80359dab12dba5982dd4cef450cd0d680b35b826360eb7;
        RES1_im = 255'h3f4149a8712dc0c2434d72d86a10e095c5dcc1a478437d04db6febafee11d2f;
        $display("[T1] A=%h, B=%h, D1_re=%h", A1, B1, D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", A1, B1, D1_im);
        $display("CONTROL x_im %d", D1_re == RES1_re);
        $display("CONTROL x_re %d", D1_im == RES1_im);

        RES2_re = 255'h3d6eddb24b4dc268da873c1f12ee39312df3c05832b132cfe1ced08e5279652;
        RES2_im = 255'h4cf222f2a6af877faf40723f9123842b5d0959f18b5d7e99b0f2b12c8efb30a;
        $display("[T1] A=%h, B=%h, D2_re=%h", A2, B2, D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", A2, B2, D2_im);
        $display("CONTROL y_im %d", D2_re == RES2_re);
        $display("CONTROL y_re %d", D2_im == RES2_im);

        RES3_re = 255'h297c2e811e56305b69e1aeef78dea652dfd48a6ac9065603ff900248169d7a8;
        RES3_im = 255'h4759121b14294760789a524893aa269261472f5312f64e200c07252d8a99d87;
        $display("[T1] A=%h, B=%h, D3_re=%h", A3, B3, D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", A3, B3, D3_im);
        $display("CONTROL z_im %d", D3_re == RES3_re);
        $display("CONTROL z_re %d", D3_im == RES3_im);

        RES4_re = 255'h352a016238596cf70ff98cd184b9b90a2444174b6301972ed081130f9f3a538;
        RES4_im = 255'hbaf2a36c699320fb9d6fefcae6956b9673d7924854aab781ca89147fb6deaa;
        $display("[T1] A=%h, B=%h, D4_re=%h", A4, B4, D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", A4, B4, D4_im);
        $display("CONTROL t_im %d", D4_re == RES4_re);
        $display("CONTROL t_re %d", D4_im == RES4_im);

        // RES1 = 255'h6961fa8023ef02728923172070710add14eb25535c8e17139bbb3d0ad46ef9;
        // $display("[T1] A=%h, B=%h, D=%h", A, B, D1);
        // $display("CONTROL %d", D1 == RES1);

        // RES2 = 255'h7a46fd2123e88c6240961494f8e20906e062222d240620f13f0044ec411a7c8;
        // $display("[T1] A=%h, B=%h, D=%h", A, B, D2);
        // $display("CONTROL %d", D2 == RES2);




        

        $display("==== FINISHED fp2_sqr TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
