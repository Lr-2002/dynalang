import json
from save_data import classify_description
import os
import sys
import argparse
import re
def change_dict(input_dict):
    # 在这里实现对字典的修改逻辑
    log = input_dict['obs']['log_language_info']
    new_log = [item for sublist in log for item in sublist]
    input_dict['obs']['log_language_info'] = new_log
    # print(new_log)
    for i, log in enumerate(new_log):
        cls = classify_description(log)
        if cls :
            input_dict['obs'][cls][i] = log
    # print(input_dict['obs']['task'])
    return input_dict
    # ...

def change_file_path(file_path):
    # file_path = "path/data.json"
    print(file_path)
    # 使用 split 方法拆分路径和文件名
    path, filename = os.path.split(file_path)


    # 修改文件名
    modified_filename = "data_modified.json"

    # 使用 join 方法将路径和修改后的文件名组合起来
    modified_file_path = '/'.join([path, modified_filename])

    return modified_file_path


def process_one_file(file_path):
    # 读取JSON文件
    # file_path = './data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 调用change_dict函数
    modified_data = change_dict(data)
    file_path = change_file_path(file_path)
    # print(file_path)
    # 保存回原始文件位置
    with open(file_path, 'w') as file:
        json.dump(modified_data, file, indent=2)  # indent参数用于美化输出，可选

if __name__=='__main__':
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='Modify folder path.')

    # 添加命令行参数
    parser.add_argument('--folder', type=str, default=os.getcwd(), help='Path of the folder to modify')

    # 解析命令行参数
    args = parser.parse_args()

    # 获取文件夹路径
    folder_path = args.folder
    # 输出提示信息
    user_input = input(f"你当前要修改的是 {folder_path} 路径，你确定吗? (y/n): ")

    if user_input.lower() == 'y':
        print("用户确定要修改路径。")
        # 在这里添加路径修改的逻辑
    else:
        print("用户取消了路径修改。")
        sys.exit()

    # 使用正则表达式匹配以六个数字命名的文件夹
    pattern = re.compile(r'\d{6}')
    exclude_file = "data_modified1.json"
    # 获取所有文件夹列表
    folders = [
        folder
        for folder in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, folder)) and exclude_file not in os.listdir(
            os.path.join(folder_path, folder))
    ]
    print(folders)
    # 筛选以六个数字命名的文件夹

    matching_files = [os.path.join(folder_path, folder, 'data.json') for folder in folders if pattern.match(folder)]
    matching_files.reverse()
    # print(matching_files)
    matching_files = sorted(matching_files)
    # print('after sort', matching_files)
    folder_num = [int(folder) for folder in folders if pattern.match(folder)]
    max_iter = max(folder_num)
    print("max folder is ", max_iter)
    # print(matching_files)
    for i in matching_files:
        process_one_file(i)


