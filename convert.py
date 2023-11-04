from kiutils.board import Board
from kiutils.utils import sexpr
from kiutils.items.common import Net
from kiutils.footprint import Footprint
from kiutils.items.fpitems import *
import re
import sys

#######*******vars*******#######
net_name_list = [] 
comp_ref_list = []
comp_value_list = []
comp_footprint_list = []
comp_tstamps_list = []
 
#######*******regular expression patterns*******#######
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

######*******function*******#######
def load_net(net_list, objectboard):
    """
    将指定.net文件中的net_name载入目标pcb文件

    Args:
    - net_list: .net文件中net的列表集合
    - objectboard: kiutils库中Board类

    Returns: None
    """
    lenth = len(net_list)
    for i in range(lenth):
        objectboard.nets.append(Net(number = i+1, name = net_list[i])) #因为是列表，值可以同步到外面参数引用



def extract_string(text, start_symbol, end_symbol):
    """
    从字符串中提取两个字符中间的字符串

    Args:
    - text: 需要提取的字符串
    - start_symbol: 开始字符
    - end_symbol: 结束字符

    Returns: 提取的字符串
    """
    pattern = re.compile(f"{start_symbol}(.*?){end_symbol}")
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None


#将footprint从kicad的封装库读取为footprint类，然后添加到pcb文件中
def load_fp(fp_name_list, objectboard):
    """
    将指定.net文件中的footprint载入目标pcb文件

    Args:
    - fp_name_list: .net文件中footprint的列表集合
    - objectboard: kiutils库中Board类

    Returns: None
    """
    original_path = 'D:\\Kicad\\7.0\\share\\kicad\\footprints\\' #kicad封装库的地址
    lenth = len(fp_name_list)
    for i in range(lenth):
        lib_name = extract_string(fp_name_list[i], '^', ':')
        fp_name = extract_string(fp_name_list[i], ':', '$') #此处作分割，方便索引
        fp_path = original_path + lib_name + '.pretty\\' + fp_name + '.kicad_mod' #封装的具体地址
        fp_origin = Footprint.from_file(filepath = fp_path)
        objectboard.footprints.append(fp_origin)
        objectboard.footprints[i].libraryNickname = lib_name #kicad_mod文件中不含libnickname，需要额外添加
        objectboard.footprints[i].graphicItems[0].text = comp_ref_list[i] #修复ref_name没有命名的问题



#######*******regular expression*******#######
# 读取并分割文件为行
net_file_contents = open("E:\\sch-convert-pcd\\demo.net", "r").read()

components_match = re.search(components_pattern, net_file_contents, re.DOTALL)
libparts_match = re.search(libparts_pattern, net_file_contents, re.DOTALL)
nets_match = re.search(nets_pattern, net_file_contents, re.DOTALL)

components = components_match.group(1).strip() if components_match else "Not found"
libparts = libparts_match.group(1).strip() if libparts_match else "Not found"
nets = nets_match.group(1).strip() if nets_match else "Not found"

net_match = re.findall(net_pattern, nets, re.DOTALL) #每个net搞定
comp_match = re.findall(comp_pattern, components, re.DOTALL)

#net解析 net ref pinfunction pintype
for net in net_match:
    #net_name解析
    net_name_match = re.search(net_name_pattern, net, re.DOTALL)
    net_name = net_name_match.group(0).strip() if net_name_match else "Not found"
    net_name = net_name.lstrip('(name "')
    net_name = net_name.rstrip(')')#分开切除，避免破坏name
    net_name_list.append(net_name.rstrip('"'))
    #net_node解析
    net_node_match = re.findall(net_node_pattern, net, re.DOTALL)


#components主要解析 ref、footprint、value、tstamps
#修改一下正则模式，改为首尾匹配，避免字母被截取
for comp in comp_match:
    #comp_ref解析
    comp_ref_match = re.search(comp_ref_pattern, comp, re.DOTALL)
    comp_ref = comp_ref_match.group(0).strip() if comp_ref_match else "Not found"
    comp_ref_list.append(extract_string(comp_ref, 'ref "', '"'))

    #comp_value解析
    comp_value_match = re.search(comp_value_pattern, comp, re.DOTALL)
    comp_value = comp_value_match.group(0).strip() if comp_value_match else "Not found"
    comp_value_list.append(extract_string(comp_value, 'value "', '"'))

    #comp_footprint解析
    comp_footprint_match = re.search(comp_footprint_pattern, comp, re.DOTALL)
    comp_footprint = comp_footprint_match.group(0).strip() if comp_footprint_match else "Not found"
    comp_footprint_list.append(extract_string(comp_footprint, 'footprint "', '"'))
    
    #comp_tstamps解析
    comp_tstamps_match = re.search(comp_tstamp_pattern, comp, re.DOTALL)
    comp_tstamps = comp_tstamps_match.group(0).strip() if comp_tstamps_match else "Not found"
    comp_tstamps_list.append(extract_string(comp_tstamps, 'tstamps "', '"'))

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

def main():
    board = Board.create_new()
    load_fp(comp_footprint_list, board)
    load_net(net_name_list, board)
    board.to_file('E:\\sch-convert-pcd\\test.kicad_pcb')
    sys.exit()

if __name__ == "__main__":
    main()