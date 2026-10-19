"""一键发布：把本地 HTML 同步到 index.html 并推送到 GitHub Pages。

用法：
    python 发布更新.py "更新说明"
不带参数时使用默认提交信息。
"""
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).resolve().parent
GIT = r"C:\Users\HEYTEA\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd\git.exe"
SRC = DIR / "打标工作台.html"
DST = DIR / "index.html"


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def main():
    if not SRC.exists():
        print("找不到 打标工作台.html")
        return 1

    # 1. 同步到 index.html（GitHub Pages 入口）
    shutil.copy2(SRC, DST)
    print("已同步 index.html")

    # 2. 暂存
    run([GIT, "-C", str(DIR), "add", "-A"])

    # 3. 是否有改动
    st = run([GIT, "-C", str(DIR), "status", "--porcelain"])
    if not st.stdout.strip():
        print("没有改动，跳过提交")
        return 0

    # 4. 提交
    msg = sys.argv[1] if len(sys.argv) > 1 else f"Update {datetime.now():%Y-%m-%d %H:%M}"
    c = run([GIT, "-C", str(DIR), "commit", "-m", msg])
    print(c.stdout.strip() or c.stderr.strip())

    # 5. 推送
    p = run([GIT, "-C", str(DIR), "push"])
    if p.returncode != 0:
        print("推送失败：")
        print(p.stderr)
        return 1

    print("已推送，GitHub Pages 约 1 分钟后生效")
    print("网址：https://datouyeye.github.io/biaoji-workbench/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
