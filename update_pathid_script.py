import random

INT64_MIN = -2**63
INT64_MAX = 2**63 - 1

def generate_pathID():
    # 在合理范围内随机生成 pathID
    pathID = random.randint(INT64_MIN, INT64_MAX)
    return pathID

def replace_both(first_value, preload_index, preload_size):
    # 生成新的pathID
    new_pathID = generate_pathID()

    # 第一个 JSON 数据
    data1 = {
        "m_FileID": 0,
        "m_PathID": new_pathID
    }

    # 第二个 JSON 数据
    data2 = {
        "first": first_value,
        "second": {
            "preloadIndex": preload_index,
            "preloadSize": preload_size,
            "asset": {
                "m_FileID": 0,
                "m_PathID": new_pathID
            }
        }
    }

    # 输出生成的 pathID
    print("生成的pathID:", new_pathID)

    # 输出第一个 JSON 结果
    print("第一个JSON结构替换结果:")
    print("      {")
    print(f"        \"m_FileID\": {data1['m_FileID']},")
    print(f"        \"m_PathID\": {data1['m_PathID']}")
    print("      },")

    # 输出第二个 JSON 结果
    print("\n第二个JSON结构替换结果:")
    print("      {")
    print(f"        \"first\": \"{data2['first']}\",")
    print("        \"second\": {")
    print(f"          \"preloadIndex\": {data2['second']['preloadIndex']},")
    print(f"          \"preloadSize\": {data2['second']['preloadSize']},")
    print("          \"asset\": {")
    print(f"            \"m_FileID\": {data2['second']['asset']['m_FileID']},")
    print(f"            \"m_PathID\": {data2['second']['asset']['m_PathID']}")
    print("          }")
    print("        }")
    print("      },")

# 按 `Enter` 控制是否生成下一次运行
def main():
    while True:
        # 提示用户输入 `first` 值
        first_value_input = input("请输入要替换的first值(按Enter确认，Ctrl+C退出程序): ").strip()
        if not first_value_input:
            print("请提供一个合法的first值！")
            continue

        # 提示用户输入 `preloadIndex` 值
        try:
            preload_index_input = int(input("请输入预加载索引值(preloadIndex)(按Enter确认，Ctrl+C退出程序): ").strip())
        except ValueError:
            print("请输入一个合法的整数作为预加载索引值！")
            continue

        # 提示用户输入 `preloadSize` 值
        try:
            preload_size_input = int(input("请输入预加载大小值(preloadSize)(按Enter确认，Ctrl+C退出程序): ").strip())
        except ValueError:
            print("请输入一个合法的整数作为预加载大小值！")
            continue

        replace_both(first_value_input, preload_index_input, preload_size_input)

# 开始运行主程序
if __name__ == "__main__":
    main()
