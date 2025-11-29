`timescale 1ns/1ps

module modred_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [509:0] A;
    wire [254:0] D;

    reg [509:0] RES;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    modred dut (
        .clk(clk),
        .rst(rst),
        .A(A),
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
        A = 510'h6e931bd48623005f73f78c7faf5e8cd0fe48427042270dd30e2358df1f6d7e89300a831b2e2a2d59dbb5ad8b2fc99ab958d9d530de4b4b8de92cf7bec430b;
        
        @(posedge clk);
        A = 510'h14d528c02a515499e0bd27a05a187c9d15b7c3c9318fe39362c07048d409dd4b05453bb021f8b9be58133095847d367eb09c39577a7500cb8b694ad2c947c;

        @(posedge clk);
        @(posedge clk);
        @(posedge clk);
        
        

        @(posedge clk);
        RES = 255'ha4c8350640e09d342354218e3674d7cd69d04839a367e864cd3b139b5d9427;
        $display("[T1] A=%h, D=%h", A, D);
        $display("CONTROL %d", D == RES);

        @(posedge clk);
        RES = 255'h144bef82ea9afb303a9875879345aeeead8f2ad0e7e6f42c975c797ebef1f84;
        $display("[T1] A=%h, D=%h", A, D);
        $display("CONTROL %d", D == RES);





        

        $display("==== FINISHED fp_mul TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
