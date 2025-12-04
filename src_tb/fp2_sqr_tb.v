`timescale 1ns/1ps

module fp2_sqr_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A;
    reg [254:0] B;
    wire [254:0] D1, D2;

    reg [254:0] RES1, RES2;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    fp2_sqr dut (
        .clk(clk),
        .rst(rst),
        .A1(A),
        .B1(B),
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
        $display("==== STARTING fp2_sqr TESTBENCH ====");

        // Wait for reset deassertion
        @(negedge rst);

        // -------------------------
        // Test Vector 1
        // -------------------------
        
        @(posedge clk);
        
        
        A = 255'h3807ed85e85d8b3fbd5a293a18bb42f0912b8e383d833a9a269d132d5a5167b;
        B = 255'h127ba0471a1f3d76c58bca5bc731dd6f91ae57c60ea264fecde8b73482c3495;
        
        

        @(posedge clk);
        A = 255'h34e0b04174d94060cacc82cd69eee90e724fe81f8a43b14ccd8904ef5a965f9;
        B = 255'h37574a8b477caf2a5f274ab5c718332ee00fefa49e0c5518b2de38c133d33ea;

        repeat(dut.LATENCY_FP2_SQR - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1 = 255'h3c1c4f9467e51a19be97071693ad823e905a8da3ecaa181fff9bbaf6a923321;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h37319e18249d047e4001270f26108a057741e2280414936d5dd56bb2ac5796a;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D2);
        $display("CONTROL %d", D2 == RES2);

        @(posedge clk);
        #1;

        RES1 = 255'h6961fa8023ef02728923172070710add14eb25535c8e17139bbb3d0ad46ef9;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h7a46fd2123e88c6240961494f8e20906e062222d240620f13f0044ec411a7c8;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D2);
        $display("CONTROL %d", D2 == RES2);




        

        $display("==== FINISHED fp2_sqr TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
