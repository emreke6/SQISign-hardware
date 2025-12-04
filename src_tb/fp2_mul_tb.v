`timescale 1ns/1ps

module fp2_mul_tb;

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
    fp2_mul dut (
        .clk(clk),
        .rst(rst),
        .y_re(A1),
        .y_im(B1),
        .z_re(A2),
        .z_im(B2),
        .x_re(D1), 
        .x_im(D2)
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
        
        
        A1 = 255'h3807ed85e85d8b3fbd5a293a18bb42f0912b8e383d833a9a269d132d5a5167b;
        B1 = 255'h127ba0471a1f3d76c58bca5bc731dd6f91ae57c60ea264fecde8b73482c3495;

        A2 = 255'h34e0b04174d94060cacc82cd69eee90e724fe81f8a43b14ccd8904ef5a965f9;
        B2 = 255'h37574a8b477caf2a5f274ab5c718332ee00fefa49e0c5518b2de38c133d33ea;

         @(posedge clk);

        A1 = 255'h8111a16abe13a48154940b369725839e90f4e986d3692ece9da0dd08b7eecc;
        B1 = 255'h269e99eea8bad8ba640c41182bc1ec23a2ce0c9b3123cbf4fc2afedb809cc36;

        A2 = 255'h12529317b325618341efef6b793653845c98a3f48661ccf0ac5106d9ffb2a93;
        B2 = 255'hd6fab372f6072170523a390c5c7e35a27a919f9e28777a4432021b36894cb6;

        repeat(dut.LATENCY_FP2_MUL - 1) begin
            @(posedge clk);
        end;

        #1;
        
        RES1 = 255'h42f8db0ba94384ea5bb5bda2695af5572d7fdc202cc2c7ccb0086cd1f62a1ab;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h3c7c4687469c2177efa9113ef61c4fdd3c8c41b4eae6eafa5f5674d1fbc8f6;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2);
        $display("CONTROL %d", D2 == RES2);

        @(posedge clk);
        #1;

        RES1 = 255'h3e5f390ff2a63e189150dc54dc1320b92bddb8ff55fabc3a4dbf4b38a93a1fc;
        $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1);
        $display("CONTROL %d", D1 == RES1);

        RES2 = 255'h218595ba6b5a05007157f0cdb50bb2306e560674def661a7926cf23175b0d06;
        $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2);
        $display("CONTROL %d", D2 == RES2);

        // RES1 = 255'h2eafb405549c1302795581cb9534445d8bdd5b339e5a5ee1e6050cac0c1bb02;
        // $display("[T1] A=%h, B=%h, D=%h", A1, B1, D1);
        // $display("CONTROL %d", D1 == RES1);

        // RES2 = 255'h1fc23e4ee285d39a471392fc3efe36de8441bdee68e94494ef71288d6847749;
        // $display("[T1] A=%h, B=%h, D=%h", A2, B2, D2);
        // $display("CONTROL %d", D2 == RES2);





        

        $display("==== FINISHED fp_add TESTBENCH ====");
        #20;
        $stop;
    end

endmodule
