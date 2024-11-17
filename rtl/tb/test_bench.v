module multiplier_tb;

  // �������ó�����λ��
  parameter WIDTH = 10;

  // ���������ź�
  reg [WIDTH-1:0] a, b;
  wire [2*WIDTH-1:0] product;
  reg fail;

  // ʵ�����˷���ģ��
  multiplier #(WIDTH) uut (
    .a(a),
    .b(b),
    .r(product)
  );

  // ���񣺼�����Ƿ���ȷ
  task check_result;
    input [WIDTH-1:0] a, b;
    input [2*WIDTH-1:0] expected_product;
    begin
      if (product !== expected_product) begin
        $display("Error: a=%d, b=%d, expected=%d, got=%d, ed=%d", a, b, expected_product, product, expected_product-product);
        fail  = 1;
      end
    end
  endtask
integer i, j;
  // ��ʼ��
  initial begin
    fail = 0;
    for (i = 0; i < 2**WIDTH; i = i + 1) begin
      for (j = 0; j < 2**WIDTH; j = j + 1) begin
        a = i; b = j; #0.01;
        check_result(a, b, a * b);
      end
    end

    // ��ɲ���
    if (fail)
        $display("FAIL!");
    else
        $display("SUCCESS!");
    $display("FINISH!");
    $finish;
  end

endmodule

