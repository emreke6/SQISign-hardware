`timescale 1ns/1ps

module fp2_sub_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A1;
    reg [254:0] B1;
    reg [254:0] A2;
    reg [254:0] B2;

    wire [254:0] D1;
    wire [254:0] D2;

    reg [254:0] RES1;
    reg [254:0] RES2;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    fp2_sub dut (
        .clk(clk),
        .rst(rst),
        .A1(A1),
        .B1(B1),
        .A2(A2),
        .B2(B2),
        .D1(D1), 
        .D2(D2)
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
        $display("==== STARTING fp2_sub TESTBENCH ====");

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

        @(posedge clk);

        A1 = 255'h8111a16abe13a48154940b369725839e90f4e986d3692ece9da0dd08b7eecc;
        B1 = 255'h269e99eea8bad8ba640c41182bc1ec23a2ce0c9b3123cbf4fc2afedb809cc36;

        A2 = 255'h12529317b325618341efef6b793653845c98a3f48661ccf0ac5106d9ffb2a93;
        B2 = 255'hd6fab372f6072170523a390c5c7e35a27a919f9e28777a4432021b36894cb6;

        repeat(dut.LATENCY_FP2_SUB - 1) begin
            @(posedge clk);
        end;

        #1
        
        RES1 = 255'h3273d4473844adef28da66caecc59e21edba618b33f894d59140e3dffbb082;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h2b2455bbd2a28e4c66647fa60019aa40b19e682170960fe61b0a7e734ef00aa;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2);
        $display("CONTROL %d", D2 == RES2);

        @(posedge clk);

        #1

        RES1 = 255'h45be86fef8bbd8c4d3595147f03c04b58c76aaa3e6d4c5fc3d8906f68bcc438;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h192eeeb7795a66a35ee89d8765fa08c97b24f2a14e9c5450b90add281807f80;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2);
        $display("CONTROL %d", D2 == RES2);





        

        $display("==== FINISHED fp2_sub TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
