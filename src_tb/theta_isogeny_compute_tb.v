`timescale 1ns/1ps

module theta_isogeny_compute_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] TT1_A1, TT1_A2, TT1_A3, TT1_A4;
    reg [254:0] TT1_B1, TT1_B2, TT1_B3, TT1_B4;
    reg [254:0] TT2_A1, TT2_A2, TT2_A3, TT2_A4;
    reg [254:0] TT2_B1, TT2_B2, TT2_B3, TT2_B4;

    wire [254:0] PRECOMP_D1_re, PRECOMP_D1_im, PRECOMP_D2_re, PRECOMP_D2_im, PRECOMP_D3_re, PRECOMP_D3_im, PRECOMP_D4_re, PRECOMP_D4_im;
    wire [254:0] NULL_POINT_D1_re, NULL_POINT_D1_im, NULL_POINT_D2_re, NULL_POINT_D2_im, NULL_POINT_D3_re, NULL_POINT_D3_im, NULL_POINT_D4_re, NULL_POINT_D4_im;

    reg [254:0] RES1_PRECOMP_re, RES1_PRECOMP_im, RES2_PRECOMP_re, RES2_PRECOMP_im, RES3_PRECOMP_re, RES3_PRECOMP_im, RES4_PRECOMP_re, RES4_PRECOMP_im;

    reg [254:0] RES1_NULL_POINT_re, RES1_NULL_POINT_im, RES2_NULL_POINT_re, RES2_NULL_POINT_im, RES3_NULL_POINT_re, RES3_NULL_POINT_im, RES4_NULL_POINT_re, RES4_NULL_POINT_im;
    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    theta_isogeny_compute dut (
        .clk(clk),
        .rst(rst),
        .TT1_A1(TT1_A1),
        .TT1_B1(TT1_B1),
        .TT1_A2(TT1_A2),
        .TT1_B2(TT1_B2),
        .TT1_A3(TT1_A3),
        .TT1_B3(TT1_B3),
        .TT1_A4(TT1_A4),
        .TT1_B4(TT1_B4),

        .TT2_A1(TT2_A1),
        .TT2_B1(TT2_B1),
        .TT2_A2(TT2_A2),
        .TT2_B2(TT2_B2),
        .TT2_A3(TT2_A3),
        .TT2_B3(TT2_B3),
        .TT2_A4(TT2_A4),
        .TT2_B4(TT2_B4),

        .PRECOMP_D1_re(PRECOMP_D1_re),
        .PRECOMP_D1_im(PRECOMP_D1_im),
        .PRECOMP_D2_re(PRECOMP_D2_re),
        .PRECOMP_D2_im(PRECOMP_D2_im),
        .PRECOMP_D3_re(PRECOMP_D3_re),
        .PRECOMP_D3_im(PRECOMP_D3_im),
        .PRECOMP_D4_re(PRECOMP_D4_re),
        .PRECOMP_D4_im(PRECOMP_D4_im),

        .NULL_POINT_D1_re(NULL_POINT_D1_re),
        .NULL_POINT_D1_im(NULL_POINT_D1_im),
        .NULL_POINT_D2_re(NULL_POINT_D2_re),
        .NULL_POINT_D2_im(NULL_POINT_D2_im),
        .NULL_POINT_D3_re(NULL_POINT_D3_re),
        .NULL_POINT_D3_im(NULL_POINT_D3_im),
        .NULL_POINT_D4_re(NULL_POINT_D4_re),
        .NULL_POINT_D4_im(NULL_POINT_D4_im)
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
        
        
        TT1_A1 = 255'h3807ed85e85d8b3fbd5a293a18bb42f0912b8e383d833a9a269d132d5a5167b;
        TT1_B1 = 255'h127ba0471a1f3d76c58bca5bc731dd6f91ae57c60ea264fecde8b73482c3495;

        TT1_A2 = 255'h34e0b04174d94060cacc82cd69eee90e724fe81f8a43b14ccd8904ef5a965f9;
        TT1_B2 = 255'h37574a8b477caf2a5f274ab5c718332ee00fefa49e0c5518b2de38c133d33ea;

        TT1_A3 = 255'h8111a16abe13a48154940b369725839e90f4e986d3692ece9da0dd08b7eecc;
        TT1_B3 = 255'h269e99eea8bad8ba640c41182bc1ec23a2ce0c9b3123cbf4fc2afedb809cc36;

        TT1_A4 = 255'h12529317b325618341efef6b793653845c98a3f48661ccf0ac5106d9ffb2a93;
        TT1_B4 = 255'hd6fab372f6072170523a390c5c7e35a27a919f9e28777a4432021b36894cb6;
        

        TT2_A1 = 255'h38bf2b416940f343d38497ea608af494449e54e00a6579da613515f8e883cee;
        TT2_B1 = 255'h131d0edffd4160a190e4c80078a385f59c54579575448a12154612aa655a544;

        TT2_A2 = 255'h4a3420f6dd1c5a22a76d988b1cdca1f1ca913e23622150822e10c4e4b52971c;
        TT2_B2 = 255'h8b5d5d46ffff5c5b7b00cb022c09d8af6d8f6eea791f928a654bf985415de9;

        TT2_A3 = 255'h3922c3166bde56c2bf193bac104830f3966ae6b0dd290cbd62444db903b0c18;
        TT2_B3 = 255'h1bd03610beb29944f7f755af7807da11751ee1031c6605711455af250fdab58;

        TT2_A4 = 255'h3f9f671b384cbde907a94d6e5c1a6d8707d9e55b45dc6c73c015873d24a7671;
        TT2_B4 = 255'h154e3fdf82be4d68fd647f59e9d31709a736232727416e7ea68a7711184bb97;

        @(posedge clk);

                // ---------- TT1 ----------
        TT1_A1 = 255'h28c1d62a684e5214897dc181616f99ab77e91d8930339fccb96c13ea7688ef8;
        TT1_B1 = 255'h28349ccbb96e2e4bbf3011d0b0f648be034aa0524bc0ce27dbb31bd09791ee1;

        TT1_A2 = 255'h194e9f8f1dd2235edad64d8ad2879185e8c6c70b59cac2c25115cbc2ca64a8a;
        TT1_B2 = 255'h15b4fb01397c47fd6324a1751b7da1cf35d41753bb42647288107132a5a6250;

        TT1_A3 = 255'h1c0ab017a5bb770463f51ec1b32dbfccd9ddcbd9f63f689d249645ef205b0ac;
        TT1_B3 = 255'h452dfdbc84a1bd27a44c1e9a648ac6be0322fba54a045b02807582dbd801c3a;

        TT1_A4 = 255'h325f3953a37323d4ba9b9d4f33f761511fbb4e58be03de7aa9cbeae13283bd7;
        TT1_B4 = 255'h3f93063d1e0f03d6af566080ecaa4db91778ce5ac89215d95e109b33fd81ad1;

        // ---------- TT2 ----------
        TT2_A1 = 255'h3dae7094965a8a86c810a6d55116092a3afb37f24e2f8f4493bcf1cd5310ee;
        TT2_B1 = 255'h82bd12fa082a26341d73eda2d1d5ffc9822183893b153bd115924a75ca4747;

        TT2_A2 = 255'h10b2ebb072ba85d3464db395bf2bd12795b457c899179c1cf3eb6b29f3874b;
        TT2_B2 = 255'h3c5b9b79243f95ed0f284d4d8faa845ec461c8aa61aa011e6c414be22840531;

        TT2_A3 = 255'h5de4e923b884fbbf3c26e084ad05010744624e1424a54f09b5a493c7b3c99b;
        TT2_B3 = 255'h2070e6beb2fcfe5b8ea2c9840f879e696a13b9a3fb7886ca20e70698657d07d;

        TT2_A4 = 255'h2dcee5948ce86a2cf9070467d7c6c963ab40d113e43b3d7ce7b942b8c684932;
        TT2_B4 = 255'h3ef07da9830958ce631828bd7a0fd4b7d3d0ba765c80aeabc225bc3cb81695e;

        

        repeat(dut.LATENCY_THETA_ISOGENY_COMPUTE - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1_PRECOMP_re = 255'h289f51632897181db9277903d1f75c6cb8926b144723d07ed7c7bce24a8bb37;
        RES1_PRECOMP_im = 255'h37679688a07506477c545ba03ada159cf2a295e4b05dc970958aad06cc6ab0b;
        $display("[T1] A=%h, B=%h, D1_re=%h", TT1_A1, TT1_B1, PRECOMP_D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", TT1_A1, TT1_B1, PRECOMP_D1_im);
        $display("CONTROL x_im %d", PRECOMP_D1_re == RES1_PRECOMP_re);
        $display("CONTROL x_re %d", PRECOMP_D1_im == RES1_PRECOMP_im);

        RES2_PRECOMP_re = 255'h432cb0d965bbfcd9f8edda44298628a8290868e9ad7d7a895cbf7a6b9c4ca7a;
        RES2_PRECOMP_im = 255'h4c5ce25d84c8da5b1d8716ae9f4d806f7a3d5d0dc675bf04e6578b4be070b79;
        $display("[T1] A=%h, B=%h, D2_re=%h", TT1_A2, TT1_B2, PRECOMP_D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", TT1_A2, TT1_B2, PRECOMP_D2_im);
        $display("CONTROL y_im %d", PRECOMP_D2_re == RES2_PRECOMP_re);
        $display("CONTROL y_re %d", PRECOMP_D2_im == RES2_PRECOMP_im);

        RES3_PRECOMP_re = 255'h20b2b2f8a2e2bd59ba6de08a9ffb14955ca38cd9d4136e12a3f0ab00ded8518;
        RES3_PRECOMP_im = 255'ha9c98a870fe80b51285a1f49eff8c06fd9b7b9f8d58c4391f0b8d6d61d1f70;
        $display("[T1] A=%h, B=%h, D3_re=%h", TT1_A3, TT1_B3, PRECOMP_D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", TT1_A3, TT1_B3, PRECOMP_D3_im);
        $display("CONTROL z_im %d", PRECOMP_D3_re == RES3_PRECOMP_re);
        $display("CONTROL z_re %d", PRECOMP_D3_im == RES3_PRECOMP_im);

        RES4_PRECOMP_re = 255'h1a3b6a08d15c6e4060e6a42eb240c232e472fdc85ed5a922ae042c1a52da78e;
        RES4_PRECOMP_im = 255'h4a16e689fffc24bcf5fd68b1c886447ba5d34523fbd4698f92b2f420a9d2485;
        $display("[T1] A=%h, B=%h, D4_re=%h", TT1_A4, TT1_B4, PRECOMP_D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", TT1_A4, TT1_B4, PRECOMP_D4_im);
        $display("CONTROL t_im %d", PRECOMP_D4_re == RES4_PRECOMP_re);
        $display("CONTROL t_re %d", PRECOMP_D4_im == RES4_PRECOMP_im);

        RES1_NULL_POINT_re = 255'h35e46e84c8a5480e721e84b79433b51107f8ddd1706dbcebe53b081b9c6ccc8;
        RES1_NULL_POINT_im = 255'h4234c60218bac903647532d239d89da5d80a45d19393bc7a07319eaf7b06a36;
        $display("[T1] A=%h, B=%h, D1_re=%h", TT1_A1, TT1_B1, NULL_POINT_D1_re);
        $display("[T1] A=%h, B=%h, D1_im=%h", TT1_A1, TT1_B1, NULL_POINT_D1_im);
        $display("CONTROL x_im %d", NULL_POINT_D1_re == RES1_NULL_POINT_re);
        $display("CONTROL x_re %d", NULL_POINT_D1_im == RES1_NULL_POINT_im);

        RES2_NULL_POINT_re = 255'h74c3905cfd92408d581907f6e1116c80cc7a62843606ef3c3e9eae5e7fccd81;
        RES2_NULL_POINT_im = 255'h737c877929d244ff8744e92d611a8611af6fb1c00a228dffd68c3c179d77de9;
        $display("[T1] A=%h, B=%h, D2_re=%h", TT1_A2, TT1_B2, NULL_POINT_D2_re);
        $display("[T1] A=%h, B=%h, D2_im=%h", TT1_A2, TT1_B2, NULL_POINT_D2_im);
        $display("CONTROL y_im %d", NULL_POINT_D2_re == RES2_NULL_POINT_re);
        $display("CONTROL y_re %d", NULL_POINT_D2_im == RES2_NULL_POINT_im);

        RES3_NULL_POINT_re = 255'h10083481e026f0da3b757b44efbc078085cbc88d0a9b8e81415159e5390737b;
        RES3_NULL_POINT_im = 255'h38cdc79d36c57e1f536f1d856accfca0912cc44a813960e8a3b49b9363be24a;
        $display("[T1] A=%h, B=%h, D3_re=%h", TT1_A3, TT1_B3, NULL_POINT_D3_re);
        $display("[T1] A=%h, B=%h, D3_im=%h", TT1_A3, TT1_B3, NULL_POINT_D3_im);
        $display("CONTROL z_im %d", NULL_POINT_D3_re == RES3_NULL_POINT_re);
        $display("CONTROL z_re %d", NULL_POINT_D3_im == RES3_NULL_POINT_im);

        RES4_NULL_POINT_re = 255'h31b2223ca09edec00b2780aebc861145bcdb80a72082791c2a77ac2b97c8896;
        RES4_NULL_POINT_im = 255'h4487ebb60bd6fcefc0555bb30e0d15285f001eb72d2b4352ef3d6eb10d773be;
        $display("[T1] A=%h, B=%h, D4_re=%h", TT1_A4, TT1_B4, NULL_POINT_D4_re);
        $display("[T1] A=%h, B=%h, D4_im=%h", TT1_A4, TT1_B4, NULL_POINT_D4_im);
        $display("CONTROL t_im %d", NULL_POINT_D4_re == RES4_NULL_POINT_re);
        $display("CONTROL t_re %d", NULL_POINT_D4_im == RES4_NULL_POINT_im);

        
        @(posedge clk);
        #1;

        // =================== PRECOMPUTATION RESULTS ===================

        RES1_PRECOMP_re = 255'h4c89fe7db5a25b8ca4f68f57be842608f7dd5554041d0965dece2c4f18b4cf0;
        RES1_PRECOMP_im = 255'h4b09b4054129a26f363482f2d37e41547814acf6e7e0222d0d0139037339c6f;
        $display("[PRECOMP1] A=%h, B=%h, D1_re=%h", TT1_A1, TT1_B1, PRECOMP_D1_re);
        $display("[PRECOMP1] A=%h, B=%h, D1_im=%h", TT1_A1, TT1_B1, PRECOMP_D1_im);
        $display("CONTROL x_im %d", PRECOMP_D1_re == RES1_PRECOMP_re);
        $display("CONTROL x_re %d", PRECOMP_D1_im == RES1_PRECOMP_im);

        RES2_PRECOMP_re = 255'h33b2a47feefd122926cfce64bd9c0e29d777f328f7759fde112b493fda704c5;
        RES2_PRECOMP_im = 255'h1f590e1200090e8da2dc975cb94d4b77f57609a4c104e44c76cbe4f5a8c6bc7;
        $display("[PRECOMP2] A=%h, B=%h, D2_re=%h", TT1_A2, TT1_B2, PRECOMP_D2_re);
        $display("[PRECOMP2] A=%h, B=%h, D2_im=%h", TT1_A2, TT1_B2, PRECOMP_D2_im);
        $display("CONTROL y_im %d", PRECOMP_D2_re == RES2_PRECOMP_re);
        $display("CONTROL y_re %d", PRECOMP_D2_im == RES2_PRECOMP_im);

        RES3_PRECOMP_re = 255'h35ef79c20567420cfb80834292ecab76eea19a96e794401905d6e36b388f503;
        RES3_PRECOMP_im = 255'h39c766a618856c8e8077a38e2c97241bd77017ca8c2ad723d7e7a2e61a9e088;
        $display("[PRECOMP3] A=%h, B=%h, D3_re=%h", TT1_A3, TT1_B3, PRECOMP_D3_re);
        $display("[PRECOMP3] A=%h, B=%h, D3_im=%h", TT1_A3, TT1_B3, PRECOMP_D3_im);
        $display("CONTROL z_im %d", PRECOMP_D3_re == RES3_PRECOMP_re);
        $display("CONTROL z_re %d", PRECOMP_D3_im == RES3_PRECOMP_im);

        RES4_PRECOMP_re = 255'h4164713aaa922a9f42bef9d60ae4375eeb22cba08de480692d229dadb69392f;
        RES4_PRECOMP_im = 255'h44452b58ed5943dd9539f8f1d58da7f39fa9e6f45cc02b81c304c479f28a69a;
        $display("[PRECOMP4] A=%h, B=%h, D4_re=%h", TT1_A4, TT1_B4, PRECOMP_D4_re);
        $display("[PRECOMP4] A=%h, B=%h, D4_im=%h", TT1_A4, TT1_B4, PRECOMP_D4_im);
        $display("CONTROL t_im %d", PRECOMP_D4_re == RES4_PRECOMP_re);
        $display("CONTROL t_re %d", PRECOMP_D4_im == RES4_PRECOMP_im);


        // =================== NULL POINT RESULTS ===================

        RES1_NULL_POINT_re = 255'h7f5e40dc4e68677e78c37e5d0ef3a3ff27517bf836767fa30882b23081986da;
        RES1_NULL_POINT_im = 255'h4bf432f47bb9c1dc4f45ac0434d9c5bc0c993f1be31586ca67eed774e001fc1;
        $display("[NULL1] A=%h, B=%h, D1_re=%h", TT1_A1, TT1_B1, NULL_POINT_D1_re);
        $display("[NULL1] A=%h, B=%h, D1_im=%h", TT1_A1, TT1_B1, NULL_POINT_D1_im);
        $display("CONTROL x_im %d", NULL_POINT_D1_re == RES1_NULL_POINT_re);
        $display("CONTROL x_re %d", NULL_POINT_D1_im == RES1_NULL_POINT_im);

        RES2_NULL_POINT_re = 255'h44953b1b6ac31389018fca0240e5e5165b2dd92d2022ad667d2df626fea3edb;
        RES2_NULL_POINT_im = 255'h20ad78b1f445e430a32a235ab32fea95b3a755be033d69e4450c654e3522eca;
        $display("[NULL2] A=%h, B=%h, D2_re=%h", TT1_A2, TT1_B2, NULL_POINT_D2_re);
        $display("[NULL2] A=%h, B=%h, D2_im=%h", TT1_A2, TT1_B2, NULL_POINT_D2_im);
        $display("CONTROL y_im %d", NULL_POINT_D2_re == RES2_NULL_POINT_re);
        $display("CONTROL y_re %d", NULL_POINT_D2_im == RES2_NULL_POINT_im);

        RES3_NULL_POINT_re = 255'h30b66ae2ee758e25fc44842bd351de5373c8af894b84fe9ea28faffea352a74;
        RES3_NULL_POINT_im = 255'h3fdb0ef66ffc610423e2730430902d9d1e65419e113f817f321608b4c5b117a;
        $display("[NULL3] A=%h, B=%h, D3_re=%h", TT1_A3, TT1_B3, NULL_POINT_D3_re);
        $display("[NULL3] A=%h, B=%h, D3_im=%h", TT1_A3, TT1_B3, NULL_POINT_D3_im);
        $display("CONTROL z_im %d", NULL_POINT_D3_re == RES3_NULL_POINT_re);
        $display("CONTROL z_re %d", NULL_POINT_D3_im == RES3_NULL_POINT_im);

        RES4_NULL_POINT_re = 255'h2dab4c2a206d42647312dcdb50f6cd46622b7719d3822cc62e9681a2029b683;
        RES4_NULL_POINT_im = 255'hbb1ef4c4a9e359279a578936142e2e62333b76a6212c1286ed22226854a2a6;
        $display("[NULL4] A=%h, B=%h, D4_re=%h", TT1_A4, TT1_B4, NULL_POINT_D4_re);
        $display("[NULL4] A=%h, B=%h, D4_im=%h", TT1_A4, TT1_B4, NULL_POINT_D4_im);
        $display("CONTROL t_im %d", NULL_POINT_D4_re == RES4_NULL_POINT_re);
        $display("CONTROL t_re %d", NULL_POINT_D4_im == RES4_NULL_POINT_im);






        

        $display("==== FINISHED fp2_to_squared_theta TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
