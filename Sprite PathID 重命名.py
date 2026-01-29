import os
import json

def modify_json_files(folder_path, new_path_id):
    """
    遍历指定文件夹中的 JSON 文件，修改目标字段中的 PathID。
    """
    print("\n正在处理文件夹:", folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # 只处理 JSON 文件
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # 检查并修改字段 m_RD.texture.m_PathID
                if "m_RD" in data and "texture" in data["m_RD"] and "m_PathID" in data["m_RD"]["texture"]:
                    old_path_id = data["m_RD"]["texture"]["m_PathID"]
                    data["m_RD"]["texture"]["m_PathID"] = new_path_id
                    print(f'修改文件: {filename}, 原 PathID: {old_path_id}, 新 PathID: {new_path_id}')
                    
                    # 写回文件，使用指定的缩进（例如：2 个空格）
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=2)
                else:
                    print(f'字段不存在，跳过文件: {filename}')
            except Exception as e:
                print(f'处理文件 {filename} 时出错: {e}')
    print("\n所有任务已完成！")

if __name__ == "__main__":
    print("JSON 文件批量 PathID 修改工具\n")
    
    while True:
        # 获取文件夹路径，去除前后的引号
        folder_path = input("请输入包含 JSON 文件的文件夹路径：").strip().strip('"')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            break
        print("路径无效，请重新输入有效的文件夹路径！")
    
    while True:
        try:
            # 获取新的 PathID
            new_path_id = int(input("请输入新的 PathID 值（整数）：").strip())
            break
        except ValueError:
            print("PathID 值无效，请输入一个整数！")
    
    # 调用修改函数
    modify_json_files(folder_path, new_path_id)
    
    # 避免窗口关闭
    input("\n任务完成！按 Enter 键以退出程序...")
