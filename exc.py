import os
import zipfile
import sys
import json

class exc():
    class json():
            def read(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            
            def write(path, data):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

    def run(file):
        try:
            if not os.path.isfile(file):
                raise FileNotFoundError(f"文件 {file} 不存在")

            extract_path = os.path.join("temp", os.path.splitext(os.path.basename(file))[0])
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(file, 'r') as zip_file:
                zip_file.extractall(extract_path)

            info_json_path = os.path.join(extract_path, "info.json")
            if not os.path.isfile(info_json_path):
                raise FileNotFoundError("解压目录中缺少 info.json 文件")

            os.chdir(extract_path)
            info_json_read = exc.json.read('info.json')
            os.system(info_json_read['run'])

        except zipfile.BadZipFile:
            print(f"错误: 文件 {file} 不是有效的 EXC 文件")

        except FileNotFoundError as e:
            print(f"错误: {e}")

        except Exception as e:
            print(f"未知错误: {e}")

    def new(name):
        try:
            os.makedirs(os.path.join(name, 'main'), exist_ok=True)

            start_bat_content = "@echo off\ncd main\npython main.py\npause\n"
            with open(os.path.join(name, "start.bat"), "w") as f:
                f.write(start_bat_content)

            main_py_content = "print('Hello World')\n"
            with open(os.path.join(name, "main", "main.py"), "w") as f:
                f.write(main_py_content)

            info_json_content = {
                "run":"start.bat",
            }

            info_json_path = os.path.join(name, "info.json")
            with open(os.path.join(name, "info.json"), "w", encoding='utf-8') as f:
                exc.json.write(info_json_path, info_json_content)

        except FileExistsError:
            print(f"错误: 目录 {name} 已存在")

        except Exception as e:
            print(f"未知错误: {e}")

    def main():
        try:
            if len(sys.argv) == 2 and sys.argv[1].endswith(".exc"):
                    exc.run(sys.argv[1])
                    sys.exit(0)
            print("XingHai EXC")
            while True:
                user_input = input("/>").strip()
                if user_input == "exit":
                    print("退出")
                    sys.exit(0)

                elif user_input == "help":
                    print("XingHai EXC Help")
                    print("命令列表:")
                    print("  help - 显示帮助信息")
                    print("  exit - 退出程序")
                    print("  new - 创建新的 EXC 软件")

                elif user_input == "new":
                    name = input('请输入EXC软件名称: ').strip()
                    if not name:
                        print("错误: APP名称不能为空")
                        return
                    exc.new(name)
                elif user_input == "":
                    pass

                else:
                    print("错误: 无效的命令")
            
        except Exception as e:
            print(f"未知错误: {e}")

if __name__ == '__main__':
    exc.main()