import os
import json

def modify_json_files(folder_path, new_path_id):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                # 打开并读取 JSON 文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # 检查并修改 m_RD.texture.m_PathID 字段
                if "m_RD" in data and "texture" in data["m_RD"] and "m_PathID" in data["m_RD"]["texture"]:
                    old_path_id = data["m_RD"]["texture"]["m_PathID"]
                    data["m_RD"]["texture"]["m_PathID"] = new_path_id
                    print(f'修改文件: {filename}, 原 PathID: {old_path_id}, 新 PathID: {new_path_id}')
                
                    # 以更新的内容写回文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                else:
                    print(f'字段不存在，跳过文件: {filename}')
            except Exception as e:
                print(f'处理文件 {filename} 时出错: {e}')

if __name__ == "__main__":
    # 动态获取文件夹路径和新的 PathID
    folder_path = input("请输入包含JSON文件的文件夹路径：").strip()
    if not os.path.exists(folder_path):
        print("文件夹路径无效，请确认后重新运行脚本。")
    else:
        try:
            new_path_id = int(input("请输入新的 PathID 值：").strip())
            modify_json_files(folder_path, new_path_id)
        except ValueError:
            print("PathID 值无效，需要输入一个整数。")
