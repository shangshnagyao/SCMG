module CARRY4 (input wire CI, CYINIT, input wire[3:0] DI, input wire[3:0] S, output wire[3:0] CO, output wire[3:0] O);
   wire	ci;
   wire	cyinit;
   wire	cin;
   wire [3:0] d;
   wire [3:0] s;
   //assign ci = (CYINIT !== 1'bz) ? CYINIT : ((CI !== 1'bz) ? CI : 0);
   assign ci = ((CI !== 1'bz) ? CI : 0) | ((CYINIT !== 1'bz) ? CYINIT : 0);
   assign d = (DI !== 4'bzzzz) ? DI : 4'b0000;
   assign s = (S !== 4'bzzzz) ? S : 4'b0000;
   assign O[0] = ci ^ s[0];
   assign O[1] = (s[0] ? ci : d[0]) ^ s[1];
   assign O[2] = (s[1] ? (s[0] ? ci : d[0]) : d[1]) ^ s[2];
   assign O[3] = (s[2] ? (s[1] ? (s[0] ? ci : d[0]) : d[1]) : d[2]) ^ s[3];
   assign CO[0] = s[0] ? ci : d[0];
   assign CO[1] = s[1] ? (s[0] ? ci : d[0]) : d[1];
   assign CO[2] = s[2] ? (s[1] ? (s[0] ? ci : d[0]) : d[1]) : d[2];
   assign CO[3] = s[3] ? (s[2] ? (s[1] ? (s[0] ? ci : d[0]) : d[1]) : d[2]) : d[3];
endmodule