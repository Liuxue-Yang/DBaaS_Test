import os
import yaml
import csv
import random

root_path = os.getcwd()

# read config
"""
    :param key: 需要读取的key
    :param filename: 需要读取的yaml文件，默认值为：conf/conf.yaml
    :return: 指定key对应的值
"""
def read_yaml_by_key(key, filename="/conf/conf.yaml"):
    file = root_path+filename
    with open(file, mode='r', encoding='utf-8') as f:
        try:
            content = yaml.load(stream=f, Loader=yaml.FullLoader)
            return content[key]
        except Exception as e:
            print("获取指定key失败：{0}".format(e)) 

# read file
"""
    :param filename: 需要读取的yaml文件
    :return: 指定key对应的值
"""
def read_yaml_file(filename=None):
    if filename:
        with open(root_path+filename, mode='r', encoding='utf-8') as f:
            content = yaml.load(stream=f, Loader=yaml.FullLoader)
            return content
    else:
        ("filename cannot be empty")

# write config
"""
    :param data: 需要写入的数据
    :param filename: 需要写入数据的文件名，默认为：conf/conf.yaml
    :return: 
"""
def write_yaml_by_key(data, filename="/conf/conf.yaml"):
    with open(root_path + filename, mode='a', encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


"""
    :param filename: 需要清除内容的文件名，默认为conf/tmp.yaml
    :return: 
"""
# clear config
def clear_config_yaml(filename="/conf/tmp.yaml"):
    with open(root_path + filename, mode='w', encoding='utf-8') as f:
        f.truncate()



read_yaml_by_key("graphd_ip")


def generate_random_csv(filename, num_rows, num_cols):
    # 生成一个名为 "int_data.csv" 的 CSV 文件，其中包含 100000 行，每行 3 列的随机整数数据
    # generate_random_csv('int_data.csv', 100000, 3)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(num_rows):
            row = [(random.randint(1, 100000000))] + [random.randint(1, 100) for _ in range(num_cols - 1)]
            writer.writerow(row)