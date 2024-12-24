import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import shutil

import git
from rich.console import Console
from rich.table import Table

class CBox:
    def __init__(self):
        """初始化 MyBox 实例"""
        self.config_file = os.path.expanduser("~/.mybox.yaml")
        self.workspaces = self._load_config()
        self.console = Console()

    def _load_config(self) -> Dict[str, str]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save_config(self) -> None:
        """保存配置到文件"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.workspaces, f)

    def add_workspace(self, name: str, path: str) -> None:
        """添加新的工作空间"""
        path = os.path.expanduser(path)
        if name in self.workspaces:
            raise ValueError(f"工作空间 '{name}' 已存在")
        
        os.makedirs(path, exist_ok=True)
        self.workspaces[name] = path
        self._save_config()
        self.console.print(f"[green]已添加工作空间 '{name}' -> {path}")

    def list_workspaces(self) -> None:
        """列出所有工作空间"""
        table = Table(show_header=True)
        table.add_column("名称")
        table.add_column("路径")
        table.add_column("状态")

        for name, path in self.workspaces.items():
            status = "[green]活动" if os.path.exists(path) else "[red]未找到"
            table.add_row(name, path, status)

        self.console.print(table)

    def _get_workspace_path(self, workspace: str) -> str:
        """获取工作空间路径"""
        if workspace not in self.workspaces:
            raise ValueError(f"工作空间 '{workspace}' 不存在")
        return self.workspaces[workspace]

    def _get_repos_in_workspace(self, workspace: str) -> List[git.Repo]:
        """获取工作空间中的所有 Git 仓库"""
        workspace_path = self._get_workspace_path(workspace)
        repos = []
        for item in os.listdir(workspace_path):
            item_path = os.path.join(workspace_path, item)
            if os.path.isdir(item_path):
                try:
                    repo = git.Repo(item_path)
                    repos.append(repo)
                except git.InvalidGitRepositoryError:
                    continue
        return repos

    def clone(self, workspace: str, repo_url: str) -> None:
        """克隆远程仓库到工作空间"""
        workspace_path = self._get_workspace_path(workspace)
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        target_path = os.path.join(workspace_path, repo_name)
        
        if os.path.exists(target_path):
            raise ValueError(f"目标路径 '{target_path}' 已存在")
        
        git.Repo.clone_from(repo_url, target_path)
        self.console.print(f"[green]已克隆仓库到 {target_path}")

        # 检查是否是 Gerrit 仓库
        if 'gerrit' in repo_url:
            self.console.print(f"[yellow]检测到 Gerrit 仓库，执行额外配置...")
            os.system(f"cd {target_path} && mkdir -p $(git rev-parse --git-dir)/hooks/ && \
                       curl -Lo $(git rev-parse --git-dir)/hooks/commit-msg http://gerrit.classup.info/tools/hooks/commit-msg && \
                       chmod +x $(git rev-parse --git-dir)/hooks/commit-msg")

    def status(self, workspace: str) -> None:
        """显示工作空间中所有仓库的状态"""
        repos = self._get_repos_in_workspace(workspace)
        
        table = Table(show_header=True)
        table.add_column("仓库")
        table.add_column("分支")
        table.add_column("状态")
        table.add_column("未跟踪")

        for repo in repos:
            name = os.path.basename(repo.working_dir)
            branch = repo.active_branch.name
            status = "[red]有更改" if repo.is_dirty() else "[green]clean"
            untracked = len(repo.untracked_files)
            table.add_row(name, branch, status, str(untracked))

        self.console.print(table)

    def pull(self, workspace: str) -> None:
        """拉取工作空间中所有仓库的更新"""
        repos = self._get_repos_in_workspace(workspace)
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 检查当前分支是否跟踪了远程分支
                if repo.active_branch.tracking_branch() is None:
                    self.console.print(f"[red]{name}: 当前分支没有跟踪远程分支")
                    continue

                repo.remotes.origin.pull()
                self.console.print(f"[green]{name}: 已更新")
            except Exception as e:
                self.console.print(f"[red]{name}: 更新失败 - {str(e)}")

    def pull_rebase(self, workspace: str) -> None:
        """使用 rebase 方式拉取工作空间中所有仓库的更新
        
        Args:
            workspace: 工作空间名称
        """
        repos = self._get_repos_in_workspace(workspace)
        
        if not repos:
            self.console.print("[yellow]工作空间中没有找到任何仓库")
            return
            
        table = Table(show_header=True)
        table.add_column("仓库", style="blue")
        table.add_column("状态", style="yellow")
        
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 检查是否有未提交的更改
                if repo.is_dirty():
                    table.add_row(name, "[yellow]有未提交的更改，已跳过")
                    continue
                
                # 执行 pull --rebase
                repo.git.pull('--rebase')
                table.add_row(name, "[green]已更新")
            except Exception as e:
                table.add_row(name, f"[red]更新失败 - {str(e)}")
        
        self.console.print(table)

    def push(self, workspace: str) -> None:
        """推送工作空间中所有仓库的更改"""
        repos = self._get_repos_in_workspace(workspace)
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 检查当前分支是否跟踪了远程分支
                if repo.active_branch.tracking_branch() is None:
                    self.console.print(f"[red]{name}: 当前分支没有跟踪远程分支")
                    continue

                # 检查是否存在 gitpush.sh 脚本
                gitpush_script = os.path.join(repo.working_dir, 'gitpush.sh')
                if os.path.exists(gitpush_script):
                    self.console.print(f"[yellow]{name}: 运行 gitpush.sh 脚本")
                    os.system(f'cd {repo.working_dir} && ./gitpush.sh')
                else:
                    repo.remotes.origin.push()
                    self.console.print(f"[green]{name}: 已推送")
            except Exception as e:
                self.console.print(f"[red]{name}: 推送失败 - {str(e)}")

    def commit(self, workspace: str, message: str) -> None:
        """提交工作空间中所有仓库的更改"""
        repos = self._get_repos_in_workspace(workspace)
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            if repo.is_dirty() or repo.untracked_files:
                try:
                    repo.git.add(A=True)
                    repo.index.commit(message)
                    self.console.print(f"[green]{name}: 已提交")
                except Exception as e:
                    self.console.print(f"[red]{name}: 提交失败 - {str(e)}")
            else:
                self.console.print(f"[yellow]{name}: 没有更改")

    def create_branch(self, workspace: str, branch_name: str, start_point: Optional[str] = None) -> None:
        """在工作空间中的所有仓库创建新分支"""
        repos = self._get_repos_in_workspace(workspace)
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 检查仓库是否有任何提交
                try:
                    repo.head.commit
                except (ValueError, TypeError):
                    self.console.print(f"[red]{name}: 创建分支失败 - 仓库没有任何提交，请先提交一些更改")
                    continue

                if start_point:
                    repo.create_head(branch_name, start_point)
                else:
                    repo.create_head(branch_name)
                self.console.print(f"[green]{name}: 已创建分支 {branch_name}")
            except Exception as e:
                self.console.print(f"[red]{name}: 创建分支失败 - {str(e)}")

    def switch_branch(self, workspace: str, branch_name: str) -> None:
        """切换工作空间中所有仓库的分支"""
        repos = self._get_repos_in_workspace(workspace)
        
        if not repos:
            self.console.print("[yellow]工作空间中没有找到任何仓库")
            return
            
        table = Table(show_header=True)
        table.add_column("仓库", style="blue")
        table.add_column("原分支", style="cyan")
        table.add_column("目标分支", style="green")
        table.add_column("状态", style="yellow")
        
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 检查仓库是否有任何提交
                try:
                    repo.head.commit
                except (ValueError, TypeError):
                    table.add_row(name, "无分支", branch_name, "[red]仓库没有任何提交，请先提交一些更改")
                    continue

                # 获取当前分支
                try:
                    current_branch = repo.active_branch.name
                except TypeError:
                    current_branch = "无分支"
                
                # 检查本地是否有这个分支
                local_branch_exists = branch_name in [branch.name for branch in repo.heads]
                
                if not local_branch_exists:
                    try:
                        # 尝试从远程获取更新
                        self.console.print(f"[yellow]{name}: 正在从远程获取更新...")
                        repo.remotes.origin.fetch()
                        
                        # 检查远程分支是否存在
                        remote_branches = [ref.name for ref in repo.remotes.origin.refs]
                        remote_branch = f"origin/{branch_name}"
                        
                        if remote_branch in remote_branches:
                            # 基于远程分支创建本地分支
                            repo.create_head(branch_name, remote_branch)
                            # 设置上游分支
                            repo.heads[branch_name].set_tracking_branch(repo.remotes.origin.refs[branch_name])
                            local_branch_exists = True
                            self.console.print(f"[green]{name}: 已基于远程分支创建本地分支")
                    except Exception as e:
                        self.console.print(f"[red]{name}: 获取远程更新失败 - {str(e)}")
                
                if not local_branch_exists:
                    table.add_row(name, current_branch, branch_name, "[red]分支不存在（本地和远程）")
                    continue
                
                # 检查是否有未提交的更改
                if repo.is_dirty():
                    table.add_row(name, current_branch, branch_name, "[red]有未提交的更改")
                    continue
                
                # 切换分支
                repo.git.checkout(branch_name)
                status = "[green]已切换" if current_branch != branch_name else "[yellow]已在该分支"
                table.add_row(name, current_branch, branch_name, status)
                
            except Exception as e:
                table.add_row(name, "未知", branch_name, f"[red]错误: {str(e)}")
        
        self.console.print("\n切换分支结果:")
        self.console.print(table)

    def delete_branch(self, workspace: str, branch_name: str, force: bool = False) -> None:
        """删除工作空间中所有仓库的指定分支"""
        repos = self._get_repos_in_workspace(workspace)
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                if force:
                    repo.git.branch('-D', branch_name)
                else:
                    repo.git.branch('-d', branch_name)
                self.console.print(f"[green]{name}: 已删除分支 {branch_name}")
            except Exception as e:
                self.console.print(f"[red]{name}: 删除分支失败 - {str(e)}")

    def import_repo(self, workspace: str, repo_path: str) -> None:
        """导入现有的本地仓库到工作空间"""
        workspace_path = self._get_workspace_path(workspace)
        repo_path = os.path.expanduser(repo_path)
        
        # 检查仓库路径是否存在
        if not os.path.exists(repo_path):
            self.console.print(f"[red]错误: 仓库路径 '{repo_path}' 不存在")
            return
        
        # 检查是否是有效的 Git 仓库
        try:
            git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            self.console.print(f"[red]错误: '{repo_path}' 不是有效的 Git 仓库")
            return
        
        repo_name = os.path.basename(repo_path)
        target_path = os.path.join(workspace_path, repo_name)

        # 检查目标路径是否已存在
        if os.path.exists(target_path):
            self.console.print(f"[red]错误: 目标路径 '{target_path}' 已存在")
            return
        
        try:
            os.symlink(repo_path, target_path)
            self.console.print(f"[green]已导入仓库 {repo_path} -> {target_path}")
        except OSError as e:
            self.console.print(f"[red]错误: 创建符号链接失败 - {str(e)}")

    def init(self, workspace: str, repo_name: str, bare: bool = False) -> None:
        """在工作空间中初始化新的 Git 仓库"""
        workspace_path = self._get_workspace_path(workspace)
        repo_path = os.path.join(workspace_path, repo_name)
        
        if os.path.exists(repo_path):
            raise ValueError(f"目标路径 '{repo_path}' 已存在")
        
        git.Repo.init(repo_path, bare=bare)
        self.console.print(f"[green]已初始化仓库 {repo_path}")

    def scan_import(self, workspace: str, scan_path: str) -> None:
        """扫描目录并导入所有找到的 Git 仓库"""
        scan_path = os.path.expanduser(scan_path)
        workspace_path = self._get_workspace_path(workspace)
        
        # 检查扫描路径是否存在
        if not os.path.exists(scan_path):
            self.console.print(f"[red]错误: 扫描路径 '{scan_path}' 不存在")
            return
            
        if not os.path.isdir(scan_path):
            self.console.print(f"[red]错误: '{scan_path}' 不是目录")
            return
            
        # 获取工作空间中已存在的仓库
        existing_repos = set()
        if os.path.exists(workspace_path):
            for item in os.listdir(workspace_path):
                item_path = os.path.join(workspace_path, item)
                if os.path.islink(item_path):  # 检查符号链接
                    real_path = os.path.realpath(item_path)
                    existing_repos.add(real_path)
                elif os.path.isdir(item_path):  # 检查普通目录
                    existing_repos.add(item_path)
        
        imported = 0
        skipped = 0
        already_exists = 0
        errors = []

        for root, dirs, _ in os.walk(scan_path):
            # 如果dirs列表的对应的文件目录下含有.git
            if '.git' in dirs:
                real_path = os.path.realpath(root)
                if real_path in existing_repos:
                    self.console.print(f"[yellow]跳过: {root} (已存在)")
                    already_exists += 1
                    continue

                # 检查是否是有效的 Git 仓库
                try:
                    git.Repo(real_path)
                except git.InvalidGitRepositoryError:
                    self.console.print(f"[red]错误: '{real_path}' 不是有效的 Git 仓库")
                    skipped += 1
                    continue

                repo_name = os.path.basename(real_path)
                target_path = os.path.join(workspace_path, repo_name)

                # 检查目标路径是否已存在
                if os.path.exists(target_path):
                    self.console.print(f"[red]错误: 目标路径 '{target_path}' 已存在")
                    already_exists += 1
                    continue

                try:
                    os.symlink(real_path, target_path)
                    self.console.print(f"[green]已导入仓库 {real_path} -> {target_path}")
                    imported += 1
                except OSError as e:
                    self.console.print(f"[red]错误: 创建符号链接失败 - {str(e)}")
                    errors.append((real_path, str(e)))
                    skipped += 1
        
        # 打印汇总信息
        self.console.print(f"\n[green]扫描完成:")
        if imported > 0:
            self.console.print(f"✓ 成功导入: {imported} 个仓库")
        if already_exists > 0:
            self.console.print(f"- 已存在: {already_exists} 个仓库")
        if skipped > 0:
            self.console.print(f"✗ 导入失败: {skipped} 个仓库")
            self.console.print("\n[yellow]失败详情:")
            for repo_path, error in errors:
                self.console.print(f"  - {repo_path}: {error}")

    def list_branches(self, workspace: str) -> None:
        """列出工作空间中所有仓库的分支"""
        repos = self._get_repos_in_workspace(workspace)
        
        if not repos:
            self.console.print("[yellow]工作空间中没有找到任何仓库")
            return
            
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            self.console.print(f"\n[bold blue]{name}[/bold blue]")
            
            table = Table(show_header=True)
            table.add_column("分支名", style="green")
            table.add_column("当前", style="cyan")
            table.add_column("远程跟踪", style="magenta")
            table.add_column("最后提交", style="yellow")
            
            try:
                active_branch = repo.active_branch.name
                for branch in repo.heads:
                    # 获取分支信息
                    is_active = "✓" if branch.name == active_branch else ""
                    tracking = ""
                    if branch.tracking_branch():
                        tracking = branch.tracking_branch().name
                    
                    # 获取最后一次提交信息
                    try:
                        last_commit = branch.commit.message.split('\n')[0][:50]
                    except Exception:
                        last_commit = "无提交记录"
                    
                    table.add_row(
                        branch.name,
                        is_active,
                        tracking or "无跟踪",
                        last_commit
                    )
                
                self.console.print(table)
            except Exception as e:
                self.console.print(f"[red]获取分支信息失败: {str(e)}")

    def remove_repo(self, workspace: str, repo_name: str) -> None:
        """删除工作空间中的指定仓库"""
        workspace_path = self._get_workspace_path(workspace)
        repo_path = os.path.join(workspace_path, repo_name)

        if not os.path.exists(repo_path):
            self.console.print(f"[red]错误: 仓库 '{repo_name}' 不存在于工作空间 '{workspace}' 中")
            return

        try:
            if os.path.islink(repo_path):
                os.unlink(repo_path)
            else:
                shutil.rmtree(repo_path)
            self.console.print(f"[green]已删除仓库 '{repo_name}'")
        except Exception as e:
            self.console.print(f"[red]删除仓库失败 - {str(e)}")

    def remove_workspace(self, workspace: str) -> None:
        """删除整个工作空间及其所有内容"""
        workspace_path = self._get_workspace_path(workspace)

        if not os.path.exists(workspace_path):
            self.console.print(f"[red]错误: 工作空间 '{workspace}' 不存在")
            return

        try:
            shutil.rmtree(workspace_path)
            # 从配置中移除工作空间
            if workspace in self.workspaces:
                del self.workspaces[workspace]
                self._save_config()
            self.console.print(f"[green]已删除工作空间 '{workspace}'")
        except Exception as e:
            self.console.print(f"[red]删除工作空间失败 - {str(e)}")

    def merge(self, workspace: str, source_branch: str) -> None:
        """合并指定分支到当前分支
        
        Args:
            workspace: 工作空间名称
            source_branch: 要合并的源分支名称
        """
        repos = self._get_repos_in_workspace(workspace)
        
        if not repos:
            self.console.print("[yellow]工作空间中没有找到任何仓库")
            return
            
        table = Table(show_header=True)
        table.add_column("仓库", style="blue")
        table.add_column("当前分支", style="cyan")
        table.add_column("源分支", style="green")
        table.add_column("状态", style="yellow")
        
        for repo in repos:
            name = os.path.basename(repo.working_dir)
            try:
                # 获取当前分支
                current_branch = repo.active_branch.name
                
                # 检查源分支是否存在
                if source_branch not in [branch.name for branch in repo.heads]:
                    table.add_row(name, current_branch, source_branch, "[red]源分支不存在")
                    continue
                
                # 检查是否有未提交的更改
                if repo.is_dirty():
                    table.add_row(name, current_branch, source_branch, "[red]有未提交的更改")
                    continue
                
                # 执行合并
                try:
                    repo.git.merge(source_branch)
                    status = "[green]合并成功"
                except git.GitCommandError as e:
                    if "CONFLICT" in str(e):
                        status = "[red]合并冲突"
                    else:
                        status = f"[red]合并失败: {str(e)}"
                except Exception as e:
                    status = f"[red]错误: {str(e)}"
                
                table.add_row(name, current_branch, source_branch, status)
                
            except Exception as e:
                table.add_row(name, "未知", source_branch, f"[red]错误: {str(e)}")
        
        self.console.print("\n合并结果:")
        self.console.print(table)

    def get_repo(self, workspace: str, repo_name: str) -> git.Repo:
        """获取指定工作空间中的特定仓库

        Args:
            workspace: 工作空间名称
            repo_name: 仓库名称

        Returns:
            git.Repo: Git 仓库对象

        Raises:
            ValueError: 如果工作空间或仓库不存在
        """
        workspace_path = self._get_workspace_path(workspace)
        repo_path = os.path.join(workspace_path, repo_name)
        
        if not os.path.exists(repo_path):
            raise ValueError(f"仓库 '{repo_name}' 不存在于工作空间 '{workspace}'")
        
        try:
            return git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path}' 不是有效的 Git 仓库")
