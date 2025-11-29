`timescale 1ns/1ps

module intmul_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A;
    reg [254:0] B;
    wire [509:0] D;

    reg [509:0] RES;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    intmul dut (
        .clk(clk),
        .rst(rst),
        .A(A),
        .B(B),
        .D(D)
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
        $display("==== STARTING fp_mul TESTBENCH ====");

        // Wait for reset deassertion
        @(negedge rst);

        // -------------------------
        // Test Vector 1
        // -------------------------
        A = 255'h3807ed85e85d8b3fbd5a293a18bb42f0912b8e383d833a9a269d132d5a5167b;
        B = 255'h253416b9fd917c11bf5458e3d2c49838944c136207a995c61be3db3c0a843f;
        
        @(posedge clk);
        
        
        A = 255'h34e0b04174d94060cacc82cd69eee90e724fe81f8a43b14ccd8904ef5a965f9;
        B = 255'h21754f0e4c2308796e42245b04d70960032fedb935aa9e8a2c71c03d90a6223;
        
        

        @(posedge clk);
        RES = 510'h8248be9fd6c8d400dd2abec651591039496e8c1b0ef2b7c3c3c49f50d34c5060369de9515c64f5f4bedbc9262322eae7c37ee273ddf9461a079c6805f445;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);

        @(posedge clk);
        RES = 510'h6e931bd48623005f73f78c7faf5e8cd0fe48427042270dd30e2358df1f6d7e89300a831b2e2a2d59dbb5ad8b2fc99ab958d9d530de4b4b8de92cf7bec430b;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);





        

        $display("==== FINISHED fp_mul TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
