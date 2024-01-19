from PIL import Image
import numpy as np
import os
import json
global_cnt = 000000
obs_set = set(['token', 'is_read_step', 'reset', 'token_embed', 'log_language_info'])
mapping_dict = {0: 'left', 1: 'right', 2: 'up', 3: 'down', 4: 'pickup', 5: 'drop', 6: 'get', 7: 'pedal', 8: 'grasp', 9: 'lift', 10:"noop"}
def from_onehot_word(x):
    global mapping_dict
    if sum(x) == 0:
        return mapping_dict[10]
    index = np.argmax(x)
    return mapping_dict[index]


def classify_description(description):
    task_keywords = ['find the', 'get the', 'put the',
                     'move the', 'open the']
    future_keywords = ['is in', 'i moved',
                       'there will']
    dynamics_keywords = ['to open the']
    corrections_keywords = ['turn around']

    for keyword in task_keywords:
        if keyword in description:
            return 'task'

    for keyword in future_keywords:
        if keyword in description:
            return 'future'

    for keyword in dynamics_keywords:
        if keyword in description:
            return 'dynamics'

    for keyword in corrections_keywords:
        if keyword in description:
            return 'correction'

    return 'unknown'




def process_large_array(large_array):
    words = [from_onehot_word(onehot) for onehot in large_array]
    return words

def update_global_cnt(path):
    # 检查目录是否存在
    if os.path.exists(path):
        # 获取目录下所有文件名
        files = os.listdir(path)
        if files:
            # 从文件名中提取数字部分并找到最大值
            existing_nums = [int(file.split('.')[0]) for file in files if file.isdigit()]
            if existing_nums:
                max_existing_num = max(existing_nums)
                # 更新global_cnt
                global global_cnt
                global_cnt =  max_existing_num + 1
                print('resume save_data in ', global_cnt)
            else:
                # 如果目录下没有数字文件名，则直接使用global_cnt的值
                pass
        else:
            # 如果目录为空，则直接使用global_cnt的值
            pass
    else:
        # 如果目录不存在，则直接使用global_cnt的值
        pass
def convert_numpy_to_list(arr):
    if isinstance(arr, np.ndarray):
        return arr.tolist()
    elif isinstance(arr, list):
        return [convert_numpy_to_list(item) for item in arr]
    else:
        return arr
def save_image(imgs, path):
    cnt = 000000
    for img in imgs:
        # 创建 Image 对象
        img = Image.fromarray(img)
        # 保存为 PNG 文件
        cnt_str = f"{cnt:06d}"
        """000000/images/000000.png"""
        save_path = f"{path}images/{cnt_str}.png"
        img.save(save_path)
        cnt+=1


def save_data(ep, save_dir='./save_data_co'):
    """
    ep: {'image', 'is_read_step', 'token', 'token_embed', 'log_language_info', 'reward', 'is_first', 'is_last', 'is_terminal', 'action', 'reset'}
    save_data
        1. fu for future observation
        2. co for correction
        3. dy for dynamics
    """
    imgs = ep['image']
    json_data = {
        "obs": {
            "token": None,
            "token_embed": None,
            "reset": None,
            "is_read_step": None,
            "log_language_info": None,
            "future": None,
            "task": None,
            "correction":None,
            "dynamics":None
        },
        "action": None,
        "action_word":None,
        "reward": None
    }
    global global_cnt
    if global_cnt == 000000:
        update_global_cnt(save_dir)

    global obs_set
    save_path = f"{save_dir}/{global_cnt:06d}/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path+'images'):
        os.makedirs(save_path+'images')
    save_image(imgs, save_path)
    classify_list = ['future', 'task','correction', 'dynamics']
    for key, value in ep.items():
        value = convert_numpy_to_list(value)
        if key in obs_set:
            json_data['obs'][key] = value
            if key == "log_language_info":
                # json_data[key] = value
                clas = classify_description(value)
                obs = json_data['obs']
                for cls in classify_list:
                    if clas == cls:
                        obs[cls] = value
                    else:
                        obs[cls] = '<pad>'
        elif key == 'action':
            json_data['action'] = value
            json_data['action_word'] = process_large_array(value)
        elif key == 'reward':
            json_data['reward'] = value
        else:
            continue

    # 指定保存路径
    save_path = save_path+'data.json'

    # 将 JSON 结构写入文件
    with open(save_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    global_cnt +=1

if __name__ =='__main__':
    # print(from_onehot_word([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    print(save_data({'log_language_info':"object/bin is in the room"}, save_dir='./'))