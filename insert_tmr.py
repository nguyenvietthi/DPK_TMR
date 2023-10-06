import re
import argparse

inst_voter = "dti_voter voter_inst (.in0(b_0), .in1(b_1), .in2(b_2), .out(b));"

def remove_first_comment_lines(input_code):
    lines = input_code.split('\n')
    comment_found = False

    line_n0 = 0

    for i, line in enumerate(lines):
        if '//' in line:
            comment_found = True
            lines[i] = '' 
            line_n0 = i
        elif not line.strip() and comment_found:
            lines[i] = '' 
        elif comment_found:
            break  
    return '\n'.join(lines)[line_n0 + 2:]

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

def replace_whole_word(original_string, target_word, replacement):
    pattern = r'\b' + target_word + r'\b'
    new_string = re.sub(pattern, replacement, original_string)
    return new_string

# new_string = replace_whole_word("wire \current_state[0] , \next_state[0] , n2_0, n1_0, n3_0, n4_0;", "current_state", "current_state[1]")
# print("asdasdasd", new_string)

def replace_tmr(text, signal_list, index):
  inst_info = instances_info(text)
  # print(signal_list)
  try:
    if (first_word(text) != "assign" and first_word(text) != "output" and first_word(text) != "wire"): 
      replace_txt = text.replace(inst_info[1], add_suffix(inst_info[1], index))
    elif (first_word(text) == "output"):
       replace_txt = text
    else:
       replace_txt = text
    signal_list = sorted(signal_list, key=lambda x: len(x), reverse=True)
    for signal in signal_list:
        # print("cccc", signal)
        if(len(signal.split(" ")) == 2):
            # print(signal.split(" ")[1], "11111")
            replace_txt = replace_whole_word(replace_txt, signal.split(" ")[1], add_suffix(signal.split(" ")[1], index))
        elif(signal[0] == '\\'):
           replace_txt = replace_txt.replace(signal, add_suffix(signal, index)+ " ")
        else:
            replace_txt = replace_whole_word(replace_txt, signal, add_suffix(signal, index))
            # print(signal,  add_suffix(signal, index), "11111w2222", replace_txt)
    # print("alllooo", replace_txt)
    return replace_txt
  except:
     return ""
  

def add_port(text, output_port):
  # print(output_port)
  output_port = sorted(output_port, key=lambda x: len(x), reverse=True)
  for port in output_port:
    replace_txt = ''
    if(len(port.split(" ")) > 1):
        for i in range(3):
            replace_txt = replace_txt + ", " + add_suffix(port.split(" ")[1], i)  
        pattern = r'\b' + re.escape(port.split(" ")[1]) + r'\b'
    else:
        for i in range(3):
            replace_txt = replace_txt + ", " + add_suffix(port, i) 
        pattern = r'\b' + re.escape(port) + r'\b'

    text = re.sub(pattern, replace_txt[1:], text)   
  return text

def modify_inst(text, signal_list):
  port_inst = text.split(", .")
  out_txt = port_inst[0]
  for port in port_inst:
    port_tmp = port.replace("(", " ").replace(".", "").replace(")", "").replace(";", "").split(" ")
    if(len(port_tmp) > 1):
      check = 0
      for signal in signal_list:
        if port_tmp[1] in signal:
          check = 1
          break
      if check:
        for i in range(3):
            out_txt = out_txt + ", ." + add_suffix(port_tmp[0], i) + "(" + add_suffix(port_tmp[1], i) + ")"
      else:
        out_txt = out_txt + ", ." + port_tmp[0] + "(" + port_tmp[1] + ")"
  out_txt = out_txt + ");\n"
  # print(out_txt)
  return out_txt

def insert_voter(output_list, f, index): 
    # print(output_list)
    output_dict = dict()
    voter_index = 0
    for output in output_list:
        try:
            # print(output.split(" ")[1])
            width = int(output.split(" ")[0].replace("[", "").replace("]", "").split(":")[0])
            for i in range(width + 1):
                f.write(inst_voter
                .replace("b_0", add_suffix(output.split(" ")[1] + "[", 0) + str(i) + "]")
                .replace("b_1", add_suffix(output.split(" ")[1] + "[", 1) + str(i) + "]")
                .replace("b_2", add_suffix(output.split(" ")[1] + "[", 2) + str(i) + "]")
                .replace("b", output.split(" ")[1] + index + "[" + str(i) + "]")
                .replace("voter_inst", "voter_" + str(voter_index)+ index) + "\n")
                voter_index = voter_index + 1
        except:
            f.write(inst_voter
            .replace("b_0", add_suffix(output.split(" ")[0], 0))
            .replace("b_1", add_suffix(output.split(" ")[0], 1))
            .replace("b_2", add_suffix(output.split(" ")[0], 2))
            .replace("b", output.split(" ")[0] + index)
            .replace("voter_inst", "voter_" + str(voter_index) + index) + "\n")
            voter_index = voter_index + 1

def q_port_dict(q_port):
  q_name_list = dict()
  q_name_string_wire = []
  try:
    for port in q_port:
      port_str = port.replace("[", " ").replace(":0]", "").split(" ")
      try:
        width = int(port_str[1])
        if(width == 0):
          q_name_list[port.replace(":0]", "]")] = 0
          for i in range(3):
            q_name_string_wire.append(add_suffix(port.replace(":0]", "]"),  str(i) + "_q"))
        else:
          q_name_list[port_str[0]] = width + 1
          for j in range(3):
             q_name_string_wire.append("[" + str(width) + ":0] " + port_str[0] + "_" + str(j) + "_q")
      except:
        q_name_list[port] = 0
        for i in range(3):
          q_name_string_wire.append(add_suffix(port, str(i) + "_q"))
  except:
    pass
  # print("cccccccccc", q_name_list, q_name_string_wire)
  return q_name_list, q_name_string_wire

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verilog_path", help = "Verilog file")
parser.add_argument("-t", "--top", help = "Top module")
parser.add_argument("-o", "--option", help = "TMR Options: fgltmr, cgtmr, fgdtmr")
# Read arguments from command line
args = parser.parse_args()
 
if args.verilog_path:
    verilog_path = args.verilog_path
if args.top:
    top_module = args.top
if args.option:
    option = args.option
    if(option == "fgltmr"):
      f1 = open("rt_qos_controller_netlist_fgltmr.sv", "w")
    elif (option == "cgtmr"):
      f2 = open("rt_qos_controller_netlist_cgtmr.sv", "w")
    elif (option == "fgdtmr"):
      f3 = open("rt_qos_controller_netlist_fgdtmr.sv", "w")
       
                       
f = open(verilog_path, "r")
f_voter = open("dti_voter_netlist.v", "r")
voter_content = f_voter.read()
verilog_content = f.read()
verilog_content = remove_first_comment_lines(verilog_content)

verilog_content = re.sub(r'\s+', ' ', verilog_content)
verilog_content = verilog_content.replace("\n", " ").replace("; ", ";\n").replace("endmodule ", "endmodule\n").replace("( ", "(").replace(" )", ")")
port_split = verilog_content.split("\n")

module_split = verilog_content.split("endmodule")

# top_module = "rt_qos_controller"

def CGTMR():
  f2.write(voter_content)
  for module in module_split[:-1]:
    internal_signal = find_words_after("wire", module)
    output_signal = find_words_after("output", module)
    if(instances_info(module)[1] == top_module):
      for line in module.split("\n")[0:-1]:
        # print(line)
        if(first_word(line) == "module" or first_word(line) == "input" or first_word(line) == "output"):
          f2.write(line + '\n') 
        elif (first_word(line) == "wire"):
          for i in range(3):
            f2.write(replace_tmr(line, internal_signal, i) + '\n')
          for port in output_signal:
            for i in range(3):
              f2.write("wire " + port + "_" + str(i) + ";\n")
        elif (line[:7] == "dti_12g"):
            for i in range(3):
              f2.write(replace_tmr(line, output_signal + internal_signal, i) + '\n')
        elif (line != ""):
          f2.write(modify_inst(line, internal_signal + output_signal))
      
      insert_voter(output_signal, f2, "")
      f2.write("endmodule\n\n")

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
  f2.close()

def FGDTMR():
  f3.write(voter_content)
  for module in module_split[:-1]:
    internal_signal = find_words_after("wire", module)
    output_signal = find_words_after("output", module)
    check_first = 0
    if(instances_info(module)[1] == top_module):
      check_first = 0
      for line in module.split("\n")[0:-1]:
        # print(line)
        if(first_word(line) == "module" or first_word(line) == "input" or first_word(line) == "output"):
          f3.write(line + '\n') 
        elif (first_word(line) == "wire"):
          for i in range(3):
            f3.write(replace_tmr(line, internal_signal, i) + '\n')
          for port in output_signal:
            for i in range(3):
              f3.write("wire " + port + "_" + str(i) + ";\n")
        elif (line[:7] == "dti_12g"):
            for i in range(3):
              f3.write(replace_tmr(line, output_signal + internal_signal, i) + '\n')
        elif (line != ""):
          f3.write(modify_inst(line, internal_signal + output_signal))
      
      insert_voter(output_signal, f3, "")
      f3.write("endmodule\n\n")

    else:
      q_port = find_q_port(module)
      # print("aaasdsds", q_port[1])
      q_dict = q_port_dict(q_port[1])
      write_first = 1
      for line in module.split("\n")[:-1]:
         
          if(first_word(line) == "module"):
            f3.write(add_port(line, output_signal) + "\n")
          elif (first_word(line) == "input"):
            f3.write(line + '\n')     
          else:
            if(first_word(line) == "wire"):
              if(write_first):
                for strr in q_dict[1]:
                   f3.write("wire " + strr + ";\n")
                write_first = 0
            text = ""
            for i in range(3):
              try:
                if (first_word(line)[:10] == 'dti_12g_ff'):
                  text = (replace_tmr(line, output_signal + internal_signal, i) + '\n')
                  q_port = find_q_port(text)[0]
                  text = text.replace( q_port, add_suffix(q_port, "q"))
                  # print(q_port)
                else:
                  text = replace_tmr(line, output_signal + internal_signal, i) + '\n'
              except:
                text = replace_tmr(line, output_signal + internal_signal, i) + '\n' 
                pass
                
              f3.write(text)
      # try:
        # for port in q_port:
        # for q in q_dict[0]:
      voter_index = 0
      for key, value in q_dict[0].items():
        for i in range(3):
          if(value == 0):
            f3.write(inst_voter
              .replace("b_0", add_suffix(key, "0_q"))
              .replace("b_1", add_suffix(key, "1_q"))
              .replace("b_2", add_suffix(key, "2_q"))
              .replace("b", add_suffix(key, str(i)))
              .replace("voter_inst", "voter_" + str(voter_index)) + "\n")
            voter_index = voter_index + 1
          else:
            for j in range(value):
              f3.write(inst_voter
                .replace("b_0", add_suffix(key + "[" + str(j) + "]", "0_q"))
                .replace("b_1", add_suffix(key + "[" + str(j) + "]", "1_q"))
                .replace("b_2", add_suffix(key + "[" + str(j) + "]", "2_q"))
                .replace("b", add_suffix(key + "[" + str(j) + "]", str(i)))
                .replace("voter_inst", "voter_" + str(voter_index)) + "\n")
              voter_index = voter_index + 1
      f3.write("endmodule\n\n")
  f3.close()

def FGLTMR():
  f1.write(voter_content)
  voter_index = 0
  for module in module_split:
    mark_voter = 0
    q_port_list = find_q_port(module)[-1]

    # print(module.split("\n")[-1])
    for line in module.split("\n")[:-1]:
      q_port = find_q_port(line)[0]
      if(q_port):
        for i in range(3):
          ins_info = instances_info(line)
          f1.write(line
            .replace(".Q(" + q_port, ".Q(" + add_suffix(q_port, i))
            .replace(ins_info[1], add_suffix(ins_info[1], i))
            .replace(")", " )") + "\n")
        f1.write(inst_voter
          .replace("b_0", add_suffix(q_port, 0))
          .replace("b_1", add_suffix(q_port, 1))
          .replace("b_2", add_suffix(q_port, 2))
          .replace("b", q_port)
          .replace("voter_inst", "voter_" + str(voter_index))
          .replace(")", " )") + "\n")
        voter_index = voter_index + 1

      elif (first_word(line) == "wire"):
        try:
          f1.write(line + "\n")
          if(mark_voter == 0):
            f1.write(("wire " + ", ".join([add_suffix(port.replace(":0", ""), 0) + " " for port in q_port_list]) 
                    + ", " +", ".join([add_suffix(port.replace(":0", ""), 1) + " " for port in q_port_list])
                    + ", " +", ".join([add_suffix(port.replace(":0", ""), 2) + " " for port in q_port_list])
                    + ";\n").replace(")", " )"))
            mark_voter = 1
        except:
          f1.write((line + "\n").replace(")", " )"))
      else:
        f1.write((line + "\n").replace(")", " )"))
    if(module != "\n"):
      f1.write("endmodule")

  f1.close()

if(option == "fgltmr"):
  FGLTMR()
elif (option == "cgtmr"):
  CGTMR()
elif (option == "fgdtmr"):
  FGDTMR()