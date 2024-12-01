module LUT6_2 (
    input  I5, I4, I3, I2, I1, I0, // �ֱ����6λ����
    output O6,                     // 6��������
    output O5                      // ǰ5��������
);
    parameter [63:0] INIT = 64'h0000000000000000;  // LUT��ʼ������

    // ����6λ�����γɵ�����ֵ
    wire [5:0] I = {I5, I4, I3, I2, I1, I0};

    // LUT�����O6�ǻ���6������Ĳ��ҽ��
    assign O6 = INIT[I];

    // LUT�����O5�ǻ���ǰ5������Ĳ��ҽ��
    assign O5 = INIT[{I4, I3, I2, I1, I0}];

endmodule
