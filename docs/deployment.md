# 部署说明

## 推荐方案：GitHub Pages

本项目是静态 Web Demo，不需要 Streamlit、后端服务或 API Key。

### 方式一：GitHub 网页操作

1. 在 GitHub 新建仓库，例如 `FoodSafe-Agent`。
2. 上传本项目全部文件。
3. 进入仓库 `Settings` -> `Pages`。
4. Source 选择 `Deploy from a branch`。
5. Branch 选择 `main`，目录选择 `/root`。
6. 保存后等待 GitHub Pages 生成访问链接。

根目录的 `index.html` 会自动跳转到 `web/index.html`。

### 方式二：命令行

```powershell
git init
git add .
git commit -m "Initial FoodSafe Agent portfolio demo"
git branch -M main
git remote add origin https://github.com/3293706561/FoodSafe-Agent.git
git push -u origin main
```

然后按方式一开启 Pages。

## 发布前检查

```powershell
.\run.ps1 "预包装饼干没有标生产日期，可以销售吗？"
.\run.ps1 "执行标准的年代号能否不写？"
.\run.ps1 "冷链车应该使用哪种压缩机？"

& "C:\Users\lenovopc\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

预期测试结果：

```text
Ran 5 tests
OK
```

## 当前限制

- 本机未检测到 `gh` 命令，无法在本地自动创建 GitHub 仓库。
- 真实发布前应复核 `docs/regulation-audit.md` 中列出的二级来源和待人工核验项。
