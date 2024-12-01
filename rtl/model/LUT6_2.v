module LUT6_2 (
    input  I5, I4, I3, I2, I1, I0, // 分别代表6位输入
    output O6,                     // 6输入的输出
    output O5                      // 前5输入的输出
);
    parameter [63:0] INIT = 64'h0000000000000000;  // LUT初始化参数

    // 计算6位输入形成的索引值
    wire [5:0] I = {I5, I4, I3, I2, I1, I0};

    // LUT的输出O6是基于6个输入的查找结果
    assign O6 = INIT[I];

    // LUT的输出O5是基于前5个输入的查找结果
    assign O5 = INIT[{I4, I3, I2, I1, I0}];

endmodule
