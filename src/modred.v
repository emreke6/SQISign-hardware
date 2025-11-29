
`timescale 1ns / 1ps


module modred(input clk,rst,
              input [509:0] A,
              output reg [254:0] D);


reg [509:0] A_tmp, A_tmp_d1, A_tmp_d2, m_times_q_calc; 
reg [255:0] C_times_mu;
reg [509:0] sum_m_c;
 
always @(posedge clk or posedge rst) begin
    if(rst) begin
        A_tmp <= 0;
        C_times_mu <= 0;
        m_times_q_calc <= 0;
        sum_m_c <= 0;
        A_tmp_d1 <= 0;
        A_tmp_d2 <= 0;
        
    end
    else begin
        A_tmp           <= A;

        A_tmp_d1        <= A_tmp;
        C_times_mu      <= (A_tmp[255:0] << 250) + (A_tmp[255:0] << 248) + A_tmp[255:0];

        A_tmp_d2        <= A_tmp_d1;
        m_times_q_calc  <= (((C_times_mu<<2) + C_times_mu) << 248) - C_times_mu;
        
        sum_m_c         <= A_tmp_d2 + m_times_q_calc;
    end
end

always @(posedge clk) begin
    D <= sum_m_c[509:256];
end
          
endmodule


