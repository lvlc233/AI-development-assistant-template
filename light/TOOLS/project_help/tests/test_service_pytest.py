import sys
import os
import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Mock mcp module before importing service
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()

# Add parent directory to path to import service
sys.path.insert(0, str(Path(__file__).parent.parent))

from service import ProjectModuleExplorer

@pytest.fixture
def mock_project_root(tmp_path):
    """Fixture to provide a temporary project root."""
    return tmp_path

@pytest.fixture
def explorer(mock_project_root):
    """Fixture to provide a ProjectModuleExplorer instance."""
    return ProjectModuleExplorer(str(mock_project_root))

class TestProjectModuleExplorer:
    
    def test_init(self, mock_project_root):
        explorer = ProjectModuleExplorer(str(mock_project_root))
        assert explorer.project_root == mock_project_root
        
        # Test default init
        with patch('pathlib.Path.cwd', return_value=Path('/cwd')):
            explorer_default = ProjectModuleExplorer()
            assert explorer_default.project_root == Path('/cwd')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_todos(self, mock_file, mock_walk, explorer):
        # Setup mock file system structure
        mock_walk.return_value = [
            ('/root', ['src'], ['test.py', 'README.md', 'ignore.txt']),
            ('/root/src', [], ['main.py']),
            ('/root/.git', [], ['config']),  # Should be ignored
        ]
        
        # Setup mock file content
        file_content = "def foo():\n    # TODO: Fix this\n    pass\n"
        mock_file.return_value.readlines.return_value = [
            "def foo():\n",
            "    # TODO: Fix this\n",
            "    pass\n"
        ]
        
        todos = explorer._scan_todos('/root')
        
        # Verification
        assert len(todos) >= 1
        todo = todos[0]
        assert 'TODO' in todo['content']
        assert todo['line'] == 2
        # Verify ignored files/dirs
        # .git should be ignored
        # ignore.txt should be ignored (not in supported extensions)
        
    @patch('pathlib.Path.rglob')
    def test_find_all_readme_files(self, mock_rglob, explorer):
        # Setup mock paths
        p1 = MagicMock(spec=Path)
        p1.__str__.return_value = "/root/README.md"
        p2 = MagicMock(spec=Path)
        p2.__str__.return_value = "/root/node_modules/pkg/README.md" # Should be ignored
        
        mock_rglob.return_value = [p1, p2]
        
        readmes = explorer.find_all_readme_files()
        
        assert len(readmes) == 1
        assert readmes[0] == p1

    def test_parse_yaml_header_valid(self, explorer, tmp_path):
        f = tmp_path / "README.md"
        content = "---\nname: Test Module\ndescription: A test\n---\n# Content"
        f.write_text(content, encoding='utf-8')
        
        data = explorer.parse_yaml_header(f)
        assert data is not None
        assert data['name'] == "Test Module"
        assert data['description'] == "A test"

    def test_parse_yaml_header_invalid(self, explorer, tmp_path):
        # Case 1: No YAML block
        f1 = tmp_path / "no_yaml.md"
        f1.write_text("# Just markdown", encoding='utf-8')
        assert explorer.parse_yaml_header(f1) is None
        
        # Case 2: Broken YAML
        f2 = tmp_path / "broken.md"
        f2.write_text("---\nname: [unclosed list\n---\n", encoding='utf-8')
        # Should catch exception and return None
        assert explorer.parse_yaml_header(f2) is None

    def test_get_module_content(self, explorer, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello World", encoding='utf-8')
        
        content = explorer.get_module_content(f)
        assert content == "Hello World"
        
        # Test missing file
        content_missing = explorer.get_module_content(tmp_path / "missing.txt")
        assert "读取文件失败" in content_missing

    @patch.object(ProjectModuleExplorer, 'find_all_readme_files')
    @patch.object(ProjectModuleExplorer, 'parse_yaml_header')
    def test_get_all_modules_info(self, mock_parse, mock_find, explorer):
        # Setup
        p1 = MagicMock(spec=Path)
        p1.__str__.return_value = "/root/mod1/README.md"
        p1.relative_to.return_value = Path("mod1/README.md")
        
        mock_find.return_value = [p1]
        mock_parse.return_value = {
            "name": "Mod1",
            "description": "Desc1",
            "state": "beta",
            "author": "User"
        }
        
        modules = explorer.get_all_modules_info()
        
        assert len(modules) == 1
        info = modules[0]
        assert info['path'] == str(Path("mod1/README.md"))
        assert info['summary']['name'] == "Mod1"
        assert info['has_yaml'] is True

    def test_get_module_details(self, explorer, tmp_path):
        # Create a real file in tmp_path to test path logic
        mod_dir = tmp_path / "mod1"
        mod_dir.mkdir()
        readme = mod_dir / "README.md"
        readme.write_text("---\nname: M1\n---\nContent", encoding='utf-8')
        
        # Test valid path
        details = explorer.get_module_details("mod1/README.md")
        assert details is not None
        assert details['yaml_header']['name'] == 'M1'
        assert "Content" in details['full_content']
        
        # Test invalid path
        assert explorer.get_module_details("mod1/MISSING.md") is None
        
        # Test file exists but not README.md
        other = mod_dir / "other.txt"
        other.touch()
        assert explorer.get_module_details("mod1/other.txt") is None

    def test_format_modules_text(self):
        # Static method test
        modules = []
        assert "未找到" in ProjectModuleExplorer.format_modules_text(modules)
        
        modules = [{
            "path": "p1",
            "summary": {"name": "N1", "state": "S1", "author": "A1", "description": "D1"}
        }]
        text = ProjectModuleExplorer.format_modules_text(modules)
        assert "N1" in text
        assert "p1" in text

    def test_format_module_details_text(self):
        # Static method test
        details = {
            "path": "p1",
            "has_yaml": True,
            "yaml_header": {"k": "v"},
            "full_content": "CONTENT"
        }
        text = ProjectModuleExplorer.format_module_details_text(details)
        assert "p1" in text
        assert "k: v" in text
        assert "CONTENT" in text

class TestTimeFunctions:
    
    @patch('service.datetime')
    def test_format_current_time_in_timezone_utc(self, mock_dt):
        # Mock now()
        fixed_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = fixed_time
        
        # Test UTC
        res = ProjectModuleExplorer.format_current_time_in_timezone("UTC")
        assert "2023年01月01日 12:00" in res
        
    @patch('service.datetime')
    def test_format_current_time_in_timezone_offset(self, mock_dt):
        # Mock now() result isn't critical as we mock the return, 
        # but the function calls now(tz), so we need to ensure tz is constructed correctly.
        
        # We can't easily mock the return value of now() to depend on the tz argument 
        # without side_effect.
        
        real_dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        def side_effect(tz):
            return real_dt.astimezone(tz)
            
        mock_dt.now.side_effect = side_effect
        
        # Test +08:00
        res = ProjectModuleExplorer.format_current_time_in_timezone("+08:00")
        # 12:00 UTC -> 20:00 UTC+8
        assert "20:00" in res
        
    def test_format_current_time_invalid(self):
        with pytest.raises(ValueError):
            ProjectModuleExplorer.format_current_time_in_timezone("")
            
        with pytest.raises(ValueError):
            ProjectModuleExplorer.format_current_time_in_timezone("Invalid/Zone")
