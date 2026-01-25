import random
import re

def generate_random_pathid():
    """
    生成一个随机的 19 位数字 pathID（可以是正数或负数）
    :return: 随机 19 位 pathID
    """
    sign = random.choice([-1, 1])  # 随机选择正负号
    pathid = sign * random.randint(10**18, 10**19 - 1)  # 确保生成 19 位
    return pathid

def replace_in_text(original_text, new_pathid, new_first_value):
    """
    替换文本中的 pathID 和 first 的内容，并在最顶部添加逗号
    :param original_text: 原始模板文本
    :param new_pathid: 新生成的 pathID 替换值
    :param new_first_value: 用户输入的 first 替换值
    :return: 添加逗号并替换内容后的最终文本
    """
    try:
        # 替换 pathID
        updated_text = re.sub(r'"m_PathID": ?-?\d+', f'"m_PathID": {{new_pathid}}', original_text)
        # 替换 first 的内容
        updated_text = re.sub(r'"first": ?".*?"', f'"first": "{{new_first_value}}"', updated_text)
        # 在顶部添加一个逗号
        updated_text_with_comma = f",\n{{updated_text.strip()}}"  # 添加逗号和换行符
        return updated_text_with_comma
    except Exception as e:
        raise ValueError(f"Error while replacing values: {{e}}")

def run_script():
    # 定义模板文本
    original_text1 = '''{{
        "m_FileID": 0,
        "m_PathID": 8611026594319798942
    }}'''

    original_text2 = '''{{
        "first": "13c4fce6c63acb44aa566ce1ee3cd8ef",
        "second": {{
            "preloadIndex": 22,
            "preloadSize": 22,
            "asset": {{
                "m_FileID": 0,
                "m_PathID": 1444030624789926558
            }}
        }}
    }}'''

    try:
        while True:
            # 提示用户是否开始生成新数据
            user_input = input("Press Enter to generate a new pathID and set a new 'first' value, or type any key to exit: ").strip()
            if user_input:
                print("Exiting the script. Goodbye!")
                break  # 用户输入了任何非空内容，退出脚本

            # 生成新的 19 位随机 pathID
            new_pathid = generate_random_pathid()
            print("\nGenerated pathID:")
            print(new_pathid)

            # 提示用户输入新的 first 值
            new_first_value = input("\nEnter the new 'first' value: ").strip()
            if not new_first_value:
                print("Error: 'first' value cannot be empty. Please try again.")
                continue  # 如果用户未输入有效的 first 值，重新开始

            # 替换两个模板文本中的 pathID 和 first 值，并在顶部添加逗号
            updated_text1 = replace_in_text(original_text1, new_pathid, new_first_value)
            updated_text2 = replace_in_text(original_text2, new_pathid, new_first_value)

            # 输出替换后的结果
            print("\nUpdated Text 1:")
            print(updated_text1)

            print("\nUpdated Text 2:")
            print(updated_text2)

    except KeyboardInterrupt:
        print("\nOperation cancelled by the user. Exiting the script. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {{e}}")

# 主程序入口
if __name__ == "__main__":
    run_script()
