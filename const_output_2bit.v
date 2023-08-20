module const_output_2bit(clk,reset,asset, data_out);
  input clk,reset;
  input asset;
  reg [1:0] count;
  output reg [1:0] data_out; 

  wire const_1, const_0;

  assign const_1 = asset^ ~asset;

  always@(posedge clk) 
  begin


    if(reset)    //Set Counter to Zero
    begin
      count = 0;
      data_out =0;
    end
    else 
      count = count+1;
    if (count ==1)
	begin
	data_out[0] = const_1;
	data_out[1] = const_1;
	end
    else if (count == 2)
	begin
	data_out[0] = const_1;
	data_out[1] = const_1;
	end
    else if (count == 3)
	begin
	data_out[0] = asset;
	data_out[1] = const_1;
	end
    else
	data_out = 0;
	
  end
    
endmodule
