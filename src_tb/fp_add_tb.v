`timescale 1ns/1ps

module fp_add_tb;

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
    fp_add dut (
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
        $display("==== STARTING fp_add TESTBENCH ====");

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

        repeat(dut.LATENCY_ADD - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES = 255'h4a838dcd027cc8b682e5f395dfed206022d9e5fe4c259f98f485ca61dd14b10;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);

        @(posedge clk);
        #1;

        RES = 255'h6c37faccbc55ef8b29f3cd8331071c3d525fd7c42850066580673db08e699e3;
        $display("[T1] A=%h, B=%h, D=%h", A, B, D);
        $display("CONTROL %d", D == RES);





        

        $display("==== FINISHED fp_add TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
