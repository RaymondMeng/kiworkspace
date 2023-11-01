import re

#var
net_str = [] 

# 使用正则表达式匹配 components、libparts 和 nets 的内容
component_pattern = r'\(components(.*?)\(libparts'
libparts_pattern = r'\(libparts(.*?)\(libraries'
nets_pattern = r'\(nets(.*?)\)\)\)\)'

comp_pattern = r'\(ref "(.*?)"\)'
lib_pattern = r'\(lib "(.*?)"\)'       
#查找nets   
net_name_pattern = r'\(name "(.*?)"\)' 

information = "1.txt"

# 读取并分割文件为行
net_file_contents = open(r"C:\Users\23915\Desktop\eda\demo.net", 'r').read()

component_match = re.search(component_pattern, net_file_contents, re.DOTALL)
libparts_match = re.search(libparts_pattern, net_file_contents, re.DOTALL)
nets_match = re.search(nets_pattern, net_file_contents, re.DOTALL)

components = component_match.group(1).strip() if component_match else "Not found"
libparts = libparts_match.group(1).strip() if libparts_match else "Not found"
nets = nets_match.group(1).strip() if nets_match else "Not found"

net_name_match = re.findall(net_name_pattern, nets, re.DOTALL)

#net解析 net ref pinfunction pintype
#可以优化，解决net_name中有（）无法用strip一次性删除的bug(已解决，pattern问题)
for net in net_name_match:
    net_str.append(net.lstrip('(name "'))

print("name_list:") 
print(net_str)

#components主要解析 ref、footprint、value





# 输出提取到的内容
# print("Components:")
# print(components)

# print("\nLibparts:")
# print(libparts)

# print("\nNets:")
# print(nets)
file = open(information, 'w')
file.write(components + "\n" + libparts + "\n" + nets + "\n")

print(f"information saved as {information}")