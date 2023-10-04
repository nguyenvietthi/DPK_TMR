import re
filename = r"./test.sv"
inst_voter = "dti_voter voter_inst (.in0(b_0), .in1(b_1), .in2(b_2), out(b));"

def find_q_port(text):
  pattern = re.compile(r'\.Q\((.*?)\)')
  matches = pattern.findall(text)

  max_values = {}
  for item in matches:
      match = re.match(r'^([^\[]+)(?:\[(\d+)\])?$', item)
      if match:
          key, value = match.groups()
          if value is not None:
              value = int(value)
              if key not in max_values or value > max_values[key][0]:
                  max_values[key] = (value, item)
          else:
              max_values[item] = (None, item)
              print(max_values)

  unique_data = []
  for key in max_values:
    if(max_values[key][0] == None):
        unique_data.append(max_values[key][1])
    else:
       unique_data.append(max_values[key][1][:-1] + ":0]")


  if(len(matches)):
    return matches[0], unique_data
  else:
    return None, None

def first_word(text):
    match = re.match(r'\b\w+\b', text)
    if match:
        return match.group()
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

verilog_content = re.sub(r'\s+', ' ', verilog_content)
verilog_content = verilog_content.replace("\n", " ").replace("; ", ";\n").replace("endmodule ", "endmodule\n").replace("( ", "(").replace(" )", ")");
port_split = verilog_content.split("\n")

module_split = verilog_content.split("endmodule")


f = open("out.sv", "w")
voter_index = 0
module_index = -1 
for module in module_split:
  mark_voter = 0
  q_port_list = find_q_port(module)[-1]
  print(q_port_list)
  for line in module.split("\n"):
    q_port = find_q_port(line)[0]
    if(q_port):
      for i in range(3):
        ins_info = instances_info(line)
        f.write(line
          .replace(".Q(" + q_port, ".Q(" + add_suffix(q_port, i))
          .replace(ins_info[1], add_suffix(ins_info[1], i)) + "\n")
      f.write(inst_voter
        .replace("b_0", add_suffix(q_port, 0))
        .replace("b_1", add_suffix(q_port, 1)).replace("b_2", add_suffix(q_port, 2))
        .replace("b", q_port)
        .replace("voter_inst", "voter_" + str(voter_index)) + "\n")
      voter_index = voter_index + 1

    elif (first_word(line) == "wire"):
      try:
        f.write(line + "\n")
        if(mark_voter == 0):
          f.write("wire " + ", ".join([add_suffix(port, 0) for port in q_port_list]) 
                  + ", " +", ".join([add_suffix(port, 1) for port in q_port_list])
                  + ", " +", ".join([add_suffix(port, 2) for port in q_port_list])
                  + ";\n")
          mark_voter = 1
      except:
        f.write(line + "\n")
    else:
      f.write(line + "\n")

f.close()