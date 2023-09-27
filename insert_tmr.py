import re
filename = r"./test.sv"
inst_voter = "dti_voter voter_inst (.in0(b_0), .in1(b_1), .in2(b_2), out(b));"

def find_q_port(text):
  result = re.search(r'.Q\((.*?)\)', text)
  print(result)
  if(result):
    return result.group(1).replace(" ", "")
  else:
    return None

def instances_info(text):
  return text.split(" ")[0:2]

def add_suffix(text, i):
  matches = re.findall(r'\[', text)
  if(len(matches) > 0):
    return text.replace("[", "_" + str(i) + "[")
  else:
    return (text + "_" + str(i));

f = open("test.sv", "r")
verilog_content = f.read()
# print(verilog_content)

verilog_content = re.sub(r'\s+', ' ', verilog_content)
verilog_content = verilog_content.replace("\n", " ").replace("; ", ";\n").replace("endmodule ", "endmodule\n").replace("( ", "(").replace(" )", ")");
port_split = verilog_content.split("\n")

module_split = verilog_content.split("endmodule")

print((module_split[1]))
print(find_q_port(module_split[1]))
# print(port_split)


# f = open("out.sv", "w")
# voter_index = 0;
# module_index = -1 
# for line in port_split:

#   if(len(re.findall(r'module', line))):
#     voter_index = 0;
#     module_index = module_index + 1
#     try:
#       # print(module_split[module_index])
#       q_port_in_module = find_q_port(module_split[module_index])
#       # print(q_port_in_module)
#       for port in q_port_in_module:
#         # print(port)
#         if(port):
#           f.write(line 
#             + "\n" + "wire " + add_suffix(port, 0) + ";"
#             + "\n" + "wire " + add_suffix(port, 1) + ";"
#             + "\n" + "wire " + add_suffix(port, 2) + ";")
#     except:
#       pass

#   q_port = find_q_port(line)
#   if(q_port):
#     for i in range(3):
#       ins_info = instances_info(line)
#       f.write(line
#         .replace(".Q(" + q_port, ".Q(" + add_suffix(q_port, i))
#         .replace(ins_info[1], add_suffix(ins_info[1], i)) + "\n")
#     f.write(inst_voter
#       .replace("b_0", add_suffix(q_port, 0))
#       .replace("b_1", add_suffix(q_port, 1)).replace("b_2", add_suffix(q_port, 2))
#       .replace("b", q_port)
#       .replace("voter_inst", "voter_" + str(voter_index)) + "\n")
#     voter_index = voter_index + 1

#   else:
#     f.write(line + "\n")

# f.close()