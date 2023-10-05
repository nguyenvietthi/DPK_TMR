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
    return (text + "_" + str(i))
  
def find_words_after(key_word,text):
    output_lines_match = re.findall(key_word + '(.*?);', text)
    words_after_output = []
    if output_lines_match:
        for output_line_match in output_lines_match:
            words_group = output_line_match.strip()
            words = [word.strip() for word in words_group.split(',')]
            
            words_after_output.extend(words)
    
    return words_after_output
    
def replace_tmr(text, signal_list, index):
  inst_info = instances_info(text)
  # print(text)
  try:
    if (first_word(line) != "assign" and first_word(line) != "output"):
      replace_txt = text.replace(inst_info[1], add_suffix(inst_info[1], index))
    else:
       replace_txt = text
    for signal in signal_list:
      replace_txt = replace_txt.replace(signal, add_suffix(signal, index))
    return replace_txt
  except:
     return ""
  

def add_port(text, output_port):
  for port in output_port:
    replace_txt = ''
    for i in range(3):
       replace_txt = replace_txt + ", " + add_suffix(port, i)
    
    pattern = r'\b' + re.escape(port) + r'\b'
    text = re.sub(pattern, replace_txt, text)      
  return text


f = open("test.sv", "r")
verilog_content = f.read()

verilog_content = re.sub(r'\s+', ' ', verilog_content)
verilog_content = verilog_content.replace("\n", " ").replace("; ", ";\n").replace("endmodule ", "endmodule\n").replace("( ", "(").replace(" )", ")").replace("//", "\n//").replace("- ", "\n\n")
f1 = open("ccc.sv", "w")
f1.write(verilog_content)
port_split = verilog_content.split("\n")

module_split = verilog_content.split("endmodule")


f2 = open("aaa.sv", "w")


top_module = "rt_qos_controller"

for module in module_split[:-1]:
  internal_signal = find_words_after("wire", module)
  output_signal = find_words_after("output", module)
  if(instances_info(module)[1] == top_module):
     ...
  else:
    for line in module.split("\n")[0:-1]:
        if(first_word(line) == "module"):
          f2.write(add_port(line, output_signal) + "\n")
        elif (first_word(line) == "input"):
          f2.write(line + '\n')      
        else:
          for i in range(3):
            f2.write(replace_tmr(line, output_signal + internal_signal, i) + '\n')

  f2.write("endmodule\n\n")














































def CGTMR():
  f = open("out.sv", "w")
  voter_index = 0
  module_index = -1 
  for module in module_split:
    mark_voter = 0
    q_port_list = find_q_port(module)[-1]
    # print(q_port_list)
    # print(module.split("\n")[-1])
    for line in module.split("\n")[:-1]:
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
    if(module != "\n"):
      f.write("endmodule")

  f.close()

