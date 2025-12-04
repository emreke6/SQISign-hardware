`timescale 1ns/1ps

module modmul_tb;

    // ----------------------------------------------------
    // DUT I/O signals
    // ----------------------------------------------------
    reg clk;
    reg rst;
    reg [254:0] A;
    reg [254:0] B;
    wire [254:0] D;

    reg [254:0] RES;

    // ----------------------------------------------------
    // Instantiate DUT
    // ----------------------------------------------------
    fp_mul dut (
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
        $display("==== STARTING modmul TESTBENCH ====");

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
        
        

        repeat(dut.LATENCY_MUL - 1) begin
            @(posedge clk);
        end;

        #1;
        RES = 255'h34f6359d42e6d96cccea4e509b41008becfd04006875248962245eaad58f111;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);

        @(posedge clk);
        #1;
        RES = 255'ha4c8350640e09d342354218e3674d7cd69d04839a367e864cd3b139b5d9427;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);





        

        $display("==== FINISHED fp_mul TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
