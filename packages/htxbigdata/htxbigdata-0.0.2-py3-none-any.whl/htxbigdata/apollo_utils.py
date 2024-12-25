import json
import subprocess

def hello_world():
    print("hello_world")


def get_value(apollo_key):
    print("###get_value###")
    # Shell脚本路径
    script_path = '/hbdata/bigdata/dataquality/apollo_util.sh'
    process = subprocess.Popen(['sh', script_path, 'security_get_apollo_config_value', apollo_key],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate()  # 获取输出和错误信息
    return_code = process.returncode  # 获取返回码

    print(f"Return code: {return_code}")
    print(f"Error output: {stderr.strip()}")
    json_str = stdout.strip()
    json_result = json.loads(json_str)
    key_result = json_result['key']
    value_result = json_result['value']
    return key_result, value_result


def get_json_value(apollo_key):
    print("###get_json_value###")
    # Shell脚本路径
    script_path = '/hbdata/bigdata/dataquality/apollo_util.sh'
    process = subprocess.Popen(['sh', script_path, 'security_get_apollo_config_value_by_json', apollo_key],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate()  # 获取输出和错误信息
    return_code = process.returncode  # 获取返回码

    print(f"Return code: {return_code}")
    print(f"Error output: {stderr.strip()}")
    res_str = stdout.strip()
    res_list = res_str.split(" ")
    key_result = res_list[0]
    value_result = res_list[1]
    return key_result, value_result



if __name__ == '__main__':
    get_json_value("key")
    get_value("key")


