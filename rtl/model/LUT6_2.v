module LUT6_2 (
    input  I5, I4, I3, I2, I1, I0, // 
    output O6,                     // 
    output O5                      // 
);
    parameter [63:0] INIT = 64'h0000000000000000;  // 

    // 
    wire [5:0] I = {I5, I4, I3, I2, I1, I0};

    // 
    assign O6 = INIT[I];

    // 
    assign O5 = INIT[{I4, I3, I2, I1, I0}];

endmodule
