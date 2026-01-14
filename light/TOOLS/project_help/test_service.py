"""
测试脚本 - 用于验证project-help MCP服务的功能
"""

import sys
import asyncio
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from service import ProjectModuleExplorer, format_current_time_in_timezone


def test_get_all_modules():
    """测试获取所有模块信息"""
    print("=" * 70)
    print("测试 1: 获取所有模块信息")
    print("=" * 70)
    print()

    # 使用项目根目录
    project_root = Path(__file__).parent.parent.parent
    print(f"项目根目录: {project_root}")
    print()

    explorer = ProjectModuleExplorer(str(project_root))
    modules = explorer.get_all_modules_info()

    if not modules:
        print("[错误] 未找到带有YAML头的README.md文件")
        return False

    print(f"[成功] 找到 {len(modules)} 个模块\n")

    for i, module in enumerate(modules, 1):
        summary = module['summary']
        print(f"【模块 {i}】")
        print(f"  名称: {summary['name']}")
        print(f"  路径: {module['path']}")
        print(f"  状态: {summary['state']}")
        print(f"  作者: {summary['author']}")
        print(f"  描述:")
        print(f"    {summary['description'][:100]}...")
        print()

    return True


def test_get_module_details():
    """测试获取指定模块详情"""
    print("=" * 70)
    print("测试 2: 获取指定模块详情")
    print("=" * 70)
    print()

    # 使用项目根目录
    project_root = Path(__file__).parent.parent.parent
    explorer = ProjectModuleExplorer(str(project_root))

    # 测试PROJECT/README.md
    test_path = "PROJECT/README.md"
    print(f"测试路径: {test_path}")
    print("-" * 70)

    details = explorer.get_module_details(test_path)

    if not details:
        print(f"[错误] 未找到文件: {test_path}")
        return False

    print(f"[成功] 找到文件: {details['path']}")
    print(f"   包含YAML头: {'是' if details['has_yaml'] else '否'}")
    print()

    if details['yaml_header']:
        print("YAML头信息:")
        print("-" * 70)
        for key, value in details['yaml_header'].items():
            print(f"  {key}: {value}")
        print()

    print("完整内容长度:", len(details['full_content']), "字符")
    print()

    return True


def test_yaml_parsing():
    """测试YAML解析功能"""
    print("=" * 70)
    print("测试 3: YAML解析功能")
    print("=" * 70)
    print()

    from pathlib import Path
    # 使用项目根目录
    project_root = Path(__file__).parent.parent.parent
    explorer = ProjectModuleExplorer(str(project_root))

    # 找一个README.md文件测试
    readme_files = explorer.find_all_readme_files()

    if not readme_files:
        print("[错误] 未找到任何README.md文件")
        return False

    test_file = readme_files[0]
    print(f"测试文件: {test_file}")
    print()

    yaml_data = explorer.parse_yaml_header(test_file)

    if yaml_data:
        print("[成功] YAML头解析成功")
        print("包含的键:", list(yaml_data.keys()))
        print()
    else:
        print("[警告] 该文件没有YAML头或解析失败")
        print()

    return True


def test_get_current_time_in_timezone():
    print("=" * 70)
    print("测试 4: 获取指定时区当前时间")
    print("=" * 70)
    print()

    value = format_current_time_in_timezone("UTC")
    if not value or len(value) != len("2000年01月01日 00:00"):
        print(f"[错误] 返回格式不符合预期: {value}")
        return False

    print(f"[成功] UTC时间: {value}")
    print()
    return True


def test_list_todos():
    """测试列出TODO"""
    print("=" * 70)
    print("测试 5: 列出TODO")
    print("=" * 70)
    print()

    # 使用项目根目录
    project_root = Path(__file__).parent.parent.parent
    
    # 临时创建一个测试文件包含TODO
    test_file = project_root / "test_todo_file.py"
    try:
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("# This is a test file\n")
            f.write("# TODO: Fix this bug\n")
            f.write("def foo():\n")
            f.write("    pass\n")
            
        from service import _list_todos_impl as list_todos, _get_todo_context_impl as get_todo_context
        import json
        
        # 这里的list_todos是直接调用的函数，不是MCP工具，所以行为取决于service.py里的实现
        # service.py里的list_todos默认用PROJECT_ROOT，如果传参"."也用PROJECT_ROOT
        # 但我们为了测试特定文件，最好让它扫描project_root
        
        # 注意：service.py里的PROJECT_ROOT是全局变量，基于service.py的位置计算的
        # 在测试环境中导入service，PROJECT_ROOT应该是正确的
        
        result_json = list_todos(".")
        todos = json.loads(result_json)
        
        found = False
        target_todo = None
        for todo in todos:
            if todo['file'] == "test_todo_file.py" and "TODO: Fix this bug" in todo['content']:
                found = True
                target_todo = todo
                break
        
        if found:
            print(f"[成功] 找到测试TODO: {target_todo['content']}")
            print(f"  文件: {target_todo['file']}")
            print(f"  行号: {target_todo['line']}")
            print(f"  上下文: {target_todo['context'][:50]}...")
            print()
            return True, target_todo
        else:
            print("[错误] 未找到刚刚创建的TODO")
            print("扫描到的文件:", [t['file'] for t in todos])
            return False, None
            
    except Exception as e:
        print(f"[错误] 测试过程出错: {e}")
        return False, None
    finally:
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()

def test_get_todo_context(todo_item):
    """测试获取TODO上下文"""
    print("=" * 70)
    print("测试 6: 获取TODO上下文")
    print("=" * 70)
    print()
    
    # if not todo_item:
    #     print("[跳过] 依赖的前置测试失败")
    #     return False

    from service import _get_todo_context_impl as get_todo_context
    import json
    
    # 我们需要再次创建文件，因为上一个测试清理了
    # 或者我们修改测试逻辑，不删除文件... 
    # 为了简单，我们复用逻辑，这里不再创建文件，而是假设test_list_todos没有删除文件
    # 但test_list_todos确实删除了。
    # 让我们重新设计一下，找一个真实存在的TODO或者再次创建。
    
    project_root = Path(__file__).parent.parent.parent
    test_file = project_root / "test_todo_context.py"
    
    try:
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("def start():\n")
            f.write("    # TODO: Implement start\n")
            f.write("    pass\n")
            f.write("    # End of function\n")
        
        # 获取上下文
        # 注意：service.py的get_todo_context接收相对路径或绝对路径
        result_json = get_todo_context("test_todo_context.py", 2)
        result = json.loads(result_json)
        
        if "error" in result:
            print(f"[错误] 获取上下文失败: {result['error']}")
            return False
            
        print(f"[成功] 获取到上下文")
        print(f"  文件: {result['file']}")
        print(f"  内容: {result['content']}")
        print(f"  完整上下文长度: {len(result['full_context'])}")
        print()
        
        if "Implement start" in result['content']:
            return True
        else:
            print("[错误] 内容不匹配")
            return False

    except Exception as e:
        print(f"[错误] 测试出错: {e}")
        return False
    finally:
        if test_file.exists():
            test_file.unlink()


async def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "Project-Help MCP 服务测试" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    try:
        # 运行测试
        test1_passed = test_get_all_modules()
        print("\n")

        test2_passed = test_get_module_details()
        print("\n")

        test3_passed = test_yaml_parsing()
        print("\n")

        test4_passed = test_get_current_time_in_timezone()
        print("\n")
        
        test5_passed, todo_item = test_list_todos()
        print("\n")
        
        test6_passed = test_get_todo_context(None) # 独立测试，不依赖传参
        print("\n")

        # 总结
        print("=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"测试 1 (获取所有模块): {'[通过]' if test1_passed else '[失败]'}")
        print(f"测试 2 (获取模块详情): {'[通过]' if test2_passed else '[失败]'}")
        print(f"测试 3 (YAML解析): {'[通过]' if test3_passed else '[失败]'}")
        print(f"测试 4 (获取当前时间): {'[通过]' if test4_passed else '[失败]'}")
        print(f"测试 5 (列出TODO): {'[通过]' if test5_passed else '[失败]'}")
        print(f"测试 6 (获取TODO上下文): {'[通过]' if test6_passed else '[失败]'}")
        print()

        if all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed, test6_passed]):
            print("[成功] 所有测试通过！服务正常运行。")
        else:
            print("[警告] 部分测试失败，请检查服务配置。")

    except Exception as e:
        print(f"\n[错误] 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
