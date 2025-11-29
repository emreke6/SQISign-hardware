import sys, math


input_bits = int(sys.argv[1])


file1 = open("parametric_intmul.v", 'w+')


# Original Tiling - 26x17
mul_w = 24
mul_h = 17


w_num = math.ceil(input_bits/mul_w)
h_num = math.ceil(input_bits/mul_h)


print("w_num = ", w_num)
print("h_num = ", h_num)

p_count = w_num * h_num

p_arr = []

for i in range(h_num):
    for j in range(w_num):
        p_arr.append((i,j))

print(p_arr)

concat_needed = []

added = []

for elm in p_arr:
    if elm not in added:
        start_idx = p_arr.index(elm)
        concat_need = []
        print(concat_need, start_idx)
        for i in range(start_idx, len(p_arr), w_num+1):
            if p_arr[i][0] == h_num-1 or p_arr[i][1] == w_num-1:
                print("aa", p_arr[i])
                concat_need.append(p_arr[i])
                added.append(p_arr[i])
                break
            concat_need.append(p_arr[i])
            added.append(p_arr[i])
        added.append(elm)
        concat_needed.append(concat_need)

print(concat_needed)




input_bits = int(sys.argv[1])


#file1 = open("btf_files/parametric_intmul.v", 'w+')


str_aaa = """
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/21/2024 10:40:22 AM
// Design Name: 
// Module Name: intmul32_64_top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module parametric_intmul(input clk,rst,
              input [{input_bits_min1}:0] A,
              input [{input_bits_min1}:0] B,
              output reg [{input_bits_mult2_min1}:0] D);


(* use_dsp = "yes" *) reg [{mulw_plus_mulh_min1}:0] {p_init};


always @(posedge clk or posedge rst) begin
    if(rst) begin
{p_str_eq_0}

    end
    else begin
{p_str}
    end
end

wire [{input_bits_mult2_min1}:0] p;



assign p = {p_concat_add}; 


always @(*) begin
    D = p;
end
          
endmodule


"""

def partition_number(n, step_size):
    partitions = []
    while n > 0:
        part = min(n, step_size)
        partitions.append(part)
        n -= part
    return partitions

p_strings = []
p_sizes = []

for i in range(h_num):
    for j in range(w_num):
        p_strings.append("p" + str(i) + "_" + str(j))


p_sizes.append(partition_number(input_bits, mul_w))
p_sizes.append(partition_number(input_bits, mul_h))

print(p_sizes)

print(p_strings)

p_str_eq_0 = ""

for str1 in p_strings:
    p_str_eq_0 = p_str_eq_0 + "        " + str1 + " <= 0;\n"

print(p_str_eq_0)

start_a = 0
end_a = mul_w
start_b = 0
end_b =  mul_h

p_str_main = ""

for j in range(h_num):
    start_a = 0
    end_a = mul_w
    for i in range(w_num):
        str1 = p_strings[j*w_num + i]
        p_str_main = p_str_main + "        " + str1 + " <= A[{end_b_min1}:{start_b}] * B[{end_a_min1}:{start_a}];\n".format(start_a = start_a, start_b = start_b,
                                                                                                                            end_a_min1 = end_a - 1, end_b_min1 = end_b-1)
        start_a += mul_w
        if end_a + mul_w < input_bits:
            end_a = end_a + mul_w
        else:
            end_a = input_bits
    
    start_b += mul_h
    if end_b + mul_h < input_bits:
            end_b = end_b + mul_h
    else:
        end_b = input_bits


print(p_str_main)



concated_strs = []

for aa in concat_needed:
    aa.reverse()

start_end_address = []

for elm in concat_needed:
    start = elm[-1]
    end = elm[0]

    print(elm)

    print(start, end)

    start_idx = start[0]*mul_h + start[1]*mul_w
    end_idx = start_idx

    for elm1 in elm:
        end_idx = end_idx + p_sizes[1][elm1[0]] + p_sizes[0][elm1[1]]

    end_idx = end_idx - 1

    print("ee: ", start_idx, end_idx)

    start_end_address.append((start_idx, end_idx))


for need_concat in concat_needed:
    str_need = "{{"
    for elm in need_concat:
        idx1, idx2 = elm[0], elm[1]
        str_need = str_need + "p" + str(idx1) + "_" + str(idx2) + ","
    str_need = str_need[:-1] + "}};"

    end_addr = start_end_address[concat_needed.index(need_concat)][1]
    start_addr = start_end_address[concat_needed.index(need_concat)][0]

    if end_addr != 2*input_bits-1:
        str_need = "{{" + str(2*input_bits-1 - end_addr) + "'b0," + str_need[2:] 

    if start_addr != 0:
        str_need = str_need[:-3] + "," +  str(start_addr) + "'b0" + "}};"

    concated_strs.append(str_need)

    print(str_need)


p_concat_add = ""

for a in concated_strs:
    p_concat_add = p_concat_add + a[:-1] + " + "
    print(p_concat_add)

print(p_concat_add.format())
print(p_concat_add.format())

p_concat_add = p_concat_add[:-3]

print(p_concat_add.format())

x = input_bits

aa = ""

for str1 in p_strings:
    aa = aa + str1 + ","

aa = aa[:-1]

file1.write(str_aaa.format(input_bits = input_bits, input_bits_min1 = input_bits - 1, input_bits_mult2_min1 = 2*input_bits - 1,
                       x_mult2_min1_min18 = x*2 - 1 - 18, p_str_eq_0 = p_str_eq_0, p_str = p_str_main, 
                       input_bits_mult2_min1_min18 = input_bits * 2 - 1 - 18, p_concat_add = p_concat_add,
                       p_init = aa, mulw_plus_mulh_min1 = mul_w + mul_h - 1))





