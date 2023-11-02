import re

#var
net_name_list = [] 
comp_ref_list = []
comp_value_list = []
comp_footprint_list = []
comp_tstamps_list = []

# 使用正则表达式匹配 components、libparts 和 nets 的内容
components_pattern = r'\(components(.*?)\(libparts'
libparts_pattern = r'\(libparts(.*?)\(libraries'
nets_pattern = r'\(nets(.*)\)\)'  #有疑问

#找每一个property
comp_pattern = r'\(comp\s.*?[0-9]"\)\)'
comp_ref_pattern = r'\(ref\s".*?"\)'
comp_value_pattern = r'\(value\s".*?"\)'
comp_footprint_pattern = r'\(footprint\s".*?"\)'
comp_tstamp_pattern = r'\(tstamps\s"[a-z0-9].*?"\)'

lib_pattern = r'\(lib "(.*?)"\)'       
  
net_pattern = r'\(net\s.*?\)\)\)' 
net_name_pattern = r'\(name\s".*?"\)' 
net_node_pattern = r'\(node\s.*?\)\)' 

information = "1.txt"

# 读取并分割文件为行
net_file_contents = open(r"C:\Users\23915\Desktop\eda\demo.net", 'r').read()

components_match = re.search(components_pattern, net_file_contents, re.DOTALL)
libparts_match = re.search(libparts_pattern, net_file_contents, re.DOTALL)
nets_match = re.search(nets_pattern, net_file_contents, re.DOTALL)

components = components_match.group(1).strip() if components_match else "Not found"
libparts = libparts_match.group(1).strip() if libparts_match else "Not found"
nets = nets_match.group(1).strip() if nets_match else "Not found"

net_match = re.findall(net_pattern, nets, re.DOTALL) #每个net搞定
comp_match = re.findall(comp_pattern, components, re.DOTALL)
#print(nets)
#print(comp_match)

#net解析 net ref pinfunction pintype
#可以优化，解决net_name中有（）无法用strip一次性删除的bug
for net in net_match:
    #net_name解析
    net_name_match = re.search(net_name_pattern, net, re.DOTALL)
    net_name = net_name_match.group(0).strip() if net_name_match else "Not found"
    net_name = net_name.lstrip('(name "')
    net_name = net_name.rstrip(')')#分开切除，避免破坏name
    net_name_list.append(net_name.rstrip('"'))
    #net_node解析
    net_node_match = re.findall(net_node_pattern, net, re.DOTALL)

# print("name_list:") 
# print(net_str)

#components主要解析 ref、footprint、value、tstamps
# print("components:\n")
#print(comp_match)
for comp in comp_match:
    #comp_ref解析
    comp_ref_match = re.search(comp_ref_pattern, comp, re.DOTALL)
    comp_ref = comp_ref_match.group(0).strip() if comp_ref_match else "Not found"
    comp_ref_list.append(comp_ref.strip('(ref "")'))

    #comp_value解析
    comp_value_match = re.search(comp_value_pattern, comp, re.DOTALL)
    comp_value = comp_value_match.group(0).strip() if comp_value_match else "Not found"
    comp_value_list.append(comp_value.strip('(value "")'))

    #comp_footprint解析
    comp_footprint_match = re.search(comp_footprint_pattern, comp, re.DOTALL)
    comp_footprint = comp_footprint_match.group(0).strip() if comp_footprint_match else "Not found"
    comp_footprint_list.append(comp_footprint.strip('(footprint "")'))
    #print(comp_footprint)

    #comp_tstamps解析
    comp_tstamps_match = re.search(comp_tstamp_pattern, comp, re.DOTALL)
    comp_tstamps = comp_tstamps_match.group(0).strip() if comp_tstamps_match else "Not found"
    comp_tstamps_list.append(comp_tstamps.strip('(tstamps "")'))

#print(comp_tstamps_list)

#输出提取到的内容
print("Components_ref_list:")
print(comp_ref_list)

print("\nComponents_value_list:")
print(comp_value_list)

print("\nComponents_footprint_list:")
print(comp_footprint_list)

print("\nComponents_tstamps_list:")
print(comp_tstamps_list)

print("\nnet_name_list:")
print(net_name_list)

# file = open(information, 'w')
# file.write(components + "\n" + libparts + "\n" + nets + "\n")

# print(f"information saved as {information}")