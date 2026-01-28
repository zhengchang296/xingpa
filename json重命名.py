import os
import json

def update_json_file(file_path, new_path_id):
    try:
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 检查文件是否含有 "m_RD" 和 "texture" 字段，然后只修改 "m_PathID"
        if "m_RD" in data and isinstance(data["m_RD"], dict) and "texture" in data["m_RD"]:
            if "m_PathID" in data["m_RD"]["texture"]:
                data["m_RD"]["texture"]["m_PathID"] = new_path_id
            else:
                raise ValueError(f"文件 {file_path} 中 texture 中缺少 'm_PathID' 字段")
        else:
            raise ValueError(f"文件 {file_path} 中缺少或格式不正确的 'm_RD' 或 'texture' 字段")
        
        # 将更新后的 JSON 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        print(f"成功更新文件 {file_path} 的 PathID")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")

def update_json_in_folder(folder_path, new_path_id):
    try:
        # 遍历目录中的所有文件
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    update_json_file(file_path, new_path_id)
    except Exception as e:
        print(f"遍历文件夹 {folder_path} 时出错：{e}")

if __name__ == "__main__":
    # 指定包含 JSON 文件的文件夹路径
    folder_path = input("请输入包含 JSON 文件的文件夹路径：")
    
    try:
        # 动态输入 PathID
        path_id = int(input("请输入新的 PathID (必须为数字): ").strip())

        update_json_in_folder(folder_path, path_id)
    except ValueError:
        print("输入的 PathID 无效，请确保输入的是一个数字！")
