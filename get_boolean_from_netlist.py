from anytree import Node, RenderTree, PreOrderIter, LevelOrderGroupIter
import re
filename = r"./test.sv"
cell_regex = r"xor|_or|and|inv"
def get_line_include_string(sub_string):
    list_line = []
    with open(filename) as file:
        lines = file.readlines()
    for number, line in enumerate(lines, 1): 
        if sub_string in line: 
            if(re.findall("assign", line)):
                list_line.append(re.sub(' +', ' ', line).replace("\n", ""))
            elif(line[-2] != ';'):
                list_line.append(re.sub(' +', ' ',line + lines[number]).replace("\n", ""))
            elif(len(re.findall("dti", line)) == 0):
                if(re.findall("output", line) or re.findall("input", line)):
                    list_line.append(re.sub(' +', ' ', line).replace("\n", ""))
                else:
                    list_line.append(re.sub(' +', ' ', lines[number - 2] + re.sub(' +', ' ',line)[1:]).replace("\n", ""))
            elif(re.findall("dti", line)):
                list_line.append(re.sub(' +', ' ', line).replace("\n", ""))       
    return list_line

def get_list_port(direction):
    port_list = get_line_include_string(direction)
    string_list = []
    for port_string in port_list:
        port = port_string.replace(direction, "").replace("]", "").replace("[", "").replace(":0", "").replace(";", "")
        port_split = port.split(" ")
        for i in range(int(port_split[2]) + 1):
            string_list.append(port_split[-1] + "[" + str(i) + "]")
    return string_list

def get_list_input_ouput_of_subcell(output):
    lines = get_line_include_string(output)
    line = ""
    for _line in lines:
        if(re.search("Z\(" + output.replace("[", "\[").replace("]", "\]"), _line)):
            line = _line
            break
    cell_name = re.search(r"\bdti\w+ \w+", line).group()
    port_inst = re.findall(r"\b[A-Z]\(\S+\)", line)
    cell_input = []
    for port in port_inst:
        if(port[0] != "Z"):
            cell_input.append(port[2:-1])
    try:   
        return cell_input, [cell_name.split(" ")[-1], re.search(cell_regex, cell_name).group()]
    except AttributeError:
        return cell_input, cell_name

def get_end_list_to_gen_tree():
    input_list = get_list_port("input")
    for number, input in enumerate(input_list):
        lines = get_line_include_string(input)
        if(len(lines) and re.sub(' +', ' ', lines[-1]).split(" ")[1] == "assign"):
            input_list[number] = re.sub(' +', ' ', lines[-1]).split(" ")[2]
    return input_list

def get_tree(pre_node, output_pre, end_tree_list, input_list):
    info_cell = get_list_input_ouput_of_subcell(output_pre)
    current_node = Node(info_cell[-1], parent=pre_node)
    for output_curr in info_cell[0]:
        if(output_curr in end_tree_list):
            Node(input_list[end_tree_list.index(output_curr)], parent=current_node)
        else:
            get_tree(current_node, output_curr, end_tree_list, input_list)

def get_boolean(output):
    boolean = ""
    root_node = Node(output)
    end_tree_list  = get_end_list_to_gen_tree()
    input_list = get_list_port("input")
    get_tree(root_node, output, end_tree_list, input_list)
    print()
    for pre, fill, node in RenderTree(root_node):
        print("%s%s" % (pre, node.name))
    level_node_list = [[node for node in children] for children in LevelOrderGroupIter(root_node)]
    level_node_list.reverse()
    parent_node = {}
    for node_list in level_node_list:
        for node in node_list:
            if node in parent_node:
                if node.parent in parent_node:
                    if(parent_node[node.parent][-1] != ")"):
                        parent_node[node.parent] = parent_node[node.parent] + " " + node.parent.name[1] + " " + parent_node[node] + ")"
                    else:
                        parent_node[node.parent] = parent_node[node.parent][:-1] + " " + node.parent.name[1] + " " + parent_node[node] + ")"
                else:
                    try:
                        if(node.parent.name[1] == "inv"):
                            parent_node[node.parent] =  "(inv" + parent_node[node] + ")"
                        else:
                            parent_node[node.parent] =  "(" + parent_node[node] + ")"
                    except AttributeError:
                        boolean = node.name + " = " + parent_node[node][2:-2]
                parent_node.pop(node)
            else:
                if node.parent in parent_node:
                    if(parent_node[node.parent][-1] != ")"):
                        parent_node[node.parent] = parent_node[node.parent] + " " + node.parent.name[1] + " " + node.name + ")"
                    else:
                        parent_node[node.parent] = parent_node[node.parent][:-1] + " " + node.parent.name[1] + " " + node.name + ")"
                else:                   
                    if(node.parent.name[-1] == "inv"):
                        parent_node[node.parent] = "(inv" + node.name + ")"
                    else:
                        parent_node[node.parent] = "(" + node.name + ")"
    print(boolean.replace("xor", "^").replace("and", "&").replace("_or", "|").replace("inv", "~"))

output_list = get_list_port("output")
for output in output_list:
    get_boolean(output)