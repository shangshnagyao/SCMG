module multiplier_tb;

  // 参数配置乘数的位宽
  parameter WIDTH = 10;

  // 输入和输出信号
  reg [WIDTH-1:0] a, b;
  wire [2*WIDTH-1:0] product;
  reg fail;

  // 实例化乘法器模块
  multiplier #(WIDTH) uut (
    .a(a),
    .b(b),
    .r(product)
  );

  // 任务：检查结果是否正确
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
  // 初始化
  initial begin
    fail = 0;
    for (i = 0; i < 2**WIDTH; i = i + 1) begin
      for (j = 0; j < 2**WIDTH; j = j + 1) begin
        a = i; b = j; #0.01;
        check_result(a, b, a * b);
      end
    end

    // 完成测试
    if (fail)
        $display("FAIL!");
    else
        $display("SUCCESS!");
    $display("FINISH!");
    $finish;
  end

endmodule

