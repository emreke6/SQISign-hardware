`timescale 1ns/1ps

module fp2_hadamard_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A1;
    reg [254:0] B1;
    reg [254:0] A2;
    reg [254:0] B2;
    reg [254:0] A3;
    reg [254:0] B3;
    reg [254:0] A4;
    reg [254:0] B4;

    wire [254:0] D1_re;
    wire [254:0] D1_im;
    wire [254:0] D2_re;
    wire [254:0] D2_im;
    wire [254:0] D3_re;
    wire [254:0] D3_im;
    wire [254:0] D4_re;
    wire [254:0] D4_im;

    reg [254:0] RES1_re;
    reg [254:0] RES1_im;
    reg [254:0] RES2_re;
    reg [254:0] RES2_im;
    reg [254:0] RES3_re;
    reg [254:0] RES3_im;
    reg [254:0] RES4_re;
    reg [254:0] RES4_im;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    fp2_hadamard dut (
        .clk(clk),
        .rst(rst),
        .x_re(A1),
        .x_im(B1),
        .y_re(A2),
        .y_im(B2),
        .z_re(A3),
        .z_im(B3),
        .t_re(A4), 
        .t_im(B4),
        
        .out_x_re(D1_re),
        .out_x_im(D1_im),
        .out_y_re(D2_re),
        .out_y_im(D2_im),
        .out_z_re(D3_re),
        .out_z_im(D3_im),
        .out_t_re(D4_re), 
        .out_t_im(D4_im)
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
        $display("==== STARTING fp_hadamard TESTBENCH ====");

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
        B2 = 255'h08b5d5d46ffff5c5b7b00cb022c09d8af6d8f6eea791f928a654bf985415de9;

        A3 = 255'h3922c3166bde56c2bf193bac104830f3966ae6b0dd290cbd62444db903b0c18;
        B3 = 255'h1bd03610beb29944f7f755af7807da11751ee1031c6605711455af250fdab58;

        A4 = 255'h3f9f671b384cbde907a94d6e5c1a6d8707d9e55b45dc6c73c015873d24a7671;
        B4 = 255'h154e3fdf82be4d68fd647f59e9d31709a736232727416e7ea68a7711184bb97;


        repeat(dut.LATENCY_FP2_HADAMARD - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1_re = 255'h374c4af5bc3d676bdf5fdc266552d7bd492368e4bb5f4bc48a512cc740195d4;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1_re);
        $display("CONTROL %d", D1_re == RES1_re);

        RES1_im = 255'h7de12ff839b737728de2f9ba7fd3e01c3c356dffc059fdb0c01210849fc816b;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1_im);
        $display("CONTROL %d", D1_im == RES1_im);

        RES2_re = 255'h48e5c4436c4023a3c5e6f7b49f085e97ab5250bc9a144f49969d15348b874ba;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2_re);
        $display("CONTROL %d", D2_re == RES2_re);

        RES2_im = 255'h445344734bfcf4efc54d1d2d6613b30a2cc35ac2bf326436d4155b9b66f802a;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2_im);
        $display("CONTROL %d", D2_im == RES2_im);

        RES3_re = 255'h5284f098fe302fd530ed7be8a0018040bdd383cad42e8c095dfb037229b6315;
        $display("[T1] A=%h, B=%h, D=%h", A3, B3, D3_re);
        $display("CONTROL %d", D3_re == RES3_re);

        RES3_im = 255'h15c4a5ac8980a1cfbb8330689cc04120a74720d59903767e417bcf66cd64f93;
        $display("[T1] A=%h, B=%h, D=%h", A3, B3, D3_im);
        $display("CONTROL %d", D3_im == RES3_im);

        RES4_re = 255'hd68b6457ac8721a1f345524be90552c9264fb74cc6ac3511b8b074773eec49;
        $display("[T1] A=%h, B=%h, D=%h", A4, B4, D4_re);
        $display("CONTROL %d", D4_re == RES4_re);

        RES4_im = 255'h11f56704594827a9077be21e9a1fa1773679758021f9bb9561ffa14b36e812a;
        $display("[T1] A=%h, B=%h, D=%h", A4, B4, D4_im);
        $display("CONTROL %d", D4_im == RES4_im);

        @(posedge clk);
        
        #1;

                RES1_re = 255'h5bb57669ea88621241b4b98fe9ca3500ad745f0f8f8c438db19fafd3c605695;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, RES1_re);
        $display("CONTROL %d", D1_re == RES1_re);

        RES1_im = 255'h4cf15aa4aeb23d153df0a9b9fd3f149baf8252ae607df72a767af878e196a1c;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, RES1_im);
        $display("CONTROL %d", D1_im == RES1_im);

        RES2_re = 255'h380e6645bfb631fae386ed9cf7dc160f089e18123f90c9a1d55317901263b78;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, RES2_re);
        $display("CONTROL %d", D2_re == RES2_re);

        RES2_im = 255'h10e92f3cc935b6b7d3c791a5e417ab7273641e82c2d727dbdcbc8b2608d371c;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, RES2_im);
        $display("CONTROL %d", D2_im == RES2_im);

        RES3_re = 255'h0a312206a23238bab42fa75b1104f80b70eac6f74981512b6cec05e77555181;
        $display("[T1] A=%h, B=%h, D=%h", A3, B3, RES3_re);
        $display("CONTROL %d", D3_re == RES3_re);

        RES3_im = 255'h3ab46ec42bd06fb95338ffa73989326576d84a59d92f0f4b00baac0c9149c3d;
        $display("[T1] A=%h, B=%h, D=%h", A3, B3, RES3_im);
        $display("CONTROL %d", D3_im == RES3_im);

        RES4_re = 255'h4507ae4f5893004774a711218f808f35eb7c156710f7890e90f58a98545102a;
        $display("[T1] A=%h, B=%h, D=%h", A4, B4, RES4_re);
        $display("CONTROL %d", D4_re == RES4_re);

        RES4_im = 255'h3e542da514d1effdea1e4fac7ae2562d792a2cad88df9f701261afe19b579a;
        $display("[T1] A=%h, B=%h, D=%h", A4, B4, RES4_im);
        $display("CONTROL %d", D4_im == RES4_im);





        

        $display("==== FINISHED fp_hadamard TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
