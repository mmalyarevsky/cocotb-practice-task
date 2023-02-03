`define USE_SCR1_PIPE_IALU

module tb();
    parameter VECTOR_WIDTH = 32;
    
    logic [VECTOR_WIDTH-1:0] op1; // input 1
    logic [VECTOR_WIDTH-1:0] op2; // input 2
    logic [VECTOR_WIDTH-1:0] cmd; // command
    logic [VECTOR_WIDTH-1:0] main_res; // main add/sub result
    logic                    cmp_res; // comparison result

`ifdef USE_SCR1_PIPE_IALU
    scr1_pipe_ialu dut(
        .exu2ialu_main_op1_i   (op1     ),
        .exu2ialu_main_op2_i   (op2     ),
        .exu2ialu_cmd_i        (cmd     ),
        .ialu2exu_main_res_o   (main_res),
        .ialu2exu_cmp_res_o    (cmp_res)
    );
`endif // USE_SCR1_PIPE_IALU

endmodule // tb