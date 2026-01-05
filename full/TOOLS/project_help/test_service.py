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

        # 总结
        print("=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"测试 1 (获取所有模块): {'[通过]' if test1_passed else '[失败]'}")
        print(f"测试 2 (获取模块详情): {'[通过]' if test2_passed else '[失败]'}")
        print(f"测试 3 (YAML解析): {'[通过]' if test3_passed else '[失败]'}")
        print(f"测试 4 (获取当前时间): {'[通过]' if test4_passed else '[失败]'}")
        print()

        if all([test1_passed, test2_passed, test3_passed, test4_passed]):
            print("[成功] 所有测试通过！服务正常运行。")
        else:
            print("[警告] 部分测试失败，请检查服务配置。")

    except Exception as e:
        print(f"\n[错误] 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
