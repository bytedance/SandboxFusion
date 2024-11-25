# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os

import pytest
from fastapi.testclient import TestClient

from sandbox.runners import CommandRunStatus
from sandbox.server.sandbox_api import RunCodeRequest, RunCodeResponse, RunStatus
from sandbox.server.server import app

client = TestClient(app)


def get_dir_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, 'samples', 'verilog')
    file_contents = {}

    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            base64_content = base64.b64encode(content).decode('utf-8')
            file_contents[filename] = base64_content

    return file_contents


@pytest.mark.verilog
def test_verilog_basic():
    test_code = """
`timescale 1 ps/1 ps
`define OK 12
`define INCORRECT 13
module reference_module(
	input a,
	input b,
	output out_assign,
	output reg out_alwaysblock
);

	assign out_assign = a & b;
	always @(*) out_alwaysblock = a & b;

endmodule


module stimulus_gen (
	input clk,
	output reg a, b,
	output reg[511:0] wavedrom_title,
	output reg wavedrom_enable
);


// Add two ports to module stimulus_gen:
//    output [511:0] wavedrom_title
//    output reg wavedrom_enable

	task wavedrom_start(input[511:0] title = "");
	endtask

	task wavedrom_stop;
		#1;
	endtask



	initial begin
		int count; count = 0;
		{a,b} <= 1'b0;
		wavedrom_start("AND gate");
		repeat(10) @(posedge clk)
			{a,b} <= count++;
		wavedrom_stop();

		repeat(200) @(posedge clk, negedge clk)
			{b,a} <= $random;

		#1 $finish;
	end

endmodule

module tb();

	typedef struct packed {
		int errors;
		int errortime;
		int errors_out_assign;
		int errortime_out_assign;
		int errors_out_alwaysblock;
		int errortime_out_alwaysblock;

		int clocks;
	} stats;

	stats stats1;


	wire[511:0] wavedrom_title;
	wire wavedrom_enable;
	int wavedrom_hide_after_time;

	reg clk=0;
	initial forever
		#5 clk = ~clk;

	logic a;
	logic b;
	logic out_assign_ref;
	logic out_assign_dut;
	logic out_alwaysblock_ref;
	logic out_alwaysblock_dut;

	initial begin
		$dumpfile("wave.vcd");
		$dumpvars(1, stim1.clk, tb_mismatch ,a,b,out_assign_ref,out_assign_dut,out_alwaysblock_ref,out_alwaysblock_dut );
	end


	wire tb_match;		// Verification
	wire tb_mismatch = ~tb_match;

	stimulus_gen stim1 (
		.clk,
		.* ,
		.a,
		.b );
	reference_module good1 (
		.a,
		.b,
		.out_assign(out_assign_ref),
		.out_alwaysblock(out_alwaysblock_ref) );

	top_module top_module1 (
		.a,
		.b,
		.out_assign(out_assign_dut),
		.out_alwaysblock(out_alwaysblock_dut) );


	bit strobe = 0;
	task wait_for_end_of_timestep;
		repeat(5) begin
			strobe <= !strobe;  // Try to delay until the very end of the time step.
			@(strobe);
		end
	endtask


	final begin
		if (stats1.errors_out_assign) $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.", "out_assign", stats1.errors_out_assign, stats1.errortime_out_assign);
		else $display("Hint: Output '%s' has no mismatches.", "out_assign");
		if (stats1.errors_out_alwaysblock) $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.", "out_alwaysblock", stats1.errors_out_alwaysblock, stats1.errortime_out_alwaysblock);
		else $display("Hint: Output '%s' has no mismatches.", "out_alwaysblock");

		$display("Hint: Total mismatched samples is %1d out of %1d samples\\n", stats1.errors, stats1.clocks);
		$display("Simulation finished at %0d ps", $time);
		$display("Mismatches: %1d in %1d samples", stats1.errors, stats1.clocks);
	end

	// Verification: XORs on the right makes any X in good_vector match anything, but X in dut_vector will only match X.
	assign tb_match = ( { out_assign_ref, out_alwaysblock_ref } === ( { out_assign_ref, out_alwaysblock_ref } ^ { out_assign_dut, out_alwaysblock_dut } ^ { out_assign_ref, out_alwaysblock_ref } ) );
	// Use explicit sensitivity list here. @(*) causes NetProc::nex_input() to be called when trying to compute
	// the sensitivity list of the @(strobe) process, which isn't implemented.
	always @(posedge clk, negedge clk) begin

		stats1.clocks++;
		if (!tb_match) begin
			if (stats1.errors == 0) stats1.errortime = $time;
			stats1.errors++;
		end
		if (out_assign_ref !== ( out_assign_ref ^ out_assign_dut ^ out_assign_ref ))
		begin if (stats1.errors_out_assign == 0) stats1.errortime_out_assign = $time;
			stats1.errors_out_assign = stats1.errors_out_assign+1'b1; end
		if (out_alwaysblock_ref !== ( out_alwaysblock_ref ^ out_alwaysblock_dut ^ out_alwaysblock_ref ))
		begin if (stats1.errors_out_alwaysblock == 0) stats1.errortime_out_alwaysblock = $time;
			stats1.errors_out_alwaysblock = stats1.errors_out_alwaysblock+1'b1; end

	end
endmodule
    """

    code_preface = """
module top_module(
	input a,
	input b,
	output out_assign,
	output reg out_alwaysblock
);
    """

    extracted_code = """
assign out_assign = a & b;
always @(*) out_alwaysblock = a & b;
endmodule
    """

    verilog_test_code = f"{test_code}{code_preface}{extracted_code}"
    # verilog_test_code = f"{code_preface}{extracted_code}"
    request = RunCodeRequest(language='verilog', code=verilog_test_code, compile_timeout=40, run_timeout=40)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    print('run output:')
    print(result.run_result.stdout)
    assert result.status == RunStatus.Success
    assert result.run_result.status == CommandRunStatus.Finished
