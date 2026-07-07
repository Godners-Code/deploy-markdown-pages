<!-- markdownlint-disable MD025 MD033 MD060 -->
# Deploy to GitHub Pages

将 Markdown 文档转换为 HTML（使用 Pandoc），自动修改内部 `.md` 链接为 `.html`，复制资源文件，并部署到 GitHub Pages 的 Action。

## 特性

- 支持 Markdown 批量转换为带标题的 HTML
- 自动将内部 `.md` 链接转换为 `.html`（保留锚点和查询参数）
- 复制 Images 目录、favicon.jpg、robots.txt、index.html
- 支持自定义图片目录、图标路径和排除目录
- 输出 Workflow Run ID 和制品（_site）绝对路径
- 兼容 GitHub Pages 部署流程
- 复合 Action，可直接在任意仓库复用

## 输入参数

| 参数 | 描述 | 默认值 | 是否必填 |
|:----:|:-----|:-------|:--------:|
| `image-src` | 图片源目录（相对于仓库根目录） | `Images` | 否 |
| `image-dst` | 图片目标路径（通常为 `_site/Images`） | `_site/Images` | 否 |
| `icons-src` | favicon.jpg 源路径 | `favicon.jpg` | 否 |
| `ex-dir` | 额外排除目录（逗号分隔），默认已包含 `_site,.git,.github` | 空 | 否 |

## 输出参数

| 输出 | 描述 |
|:----:|:-----|
| `run-id` | 当前 GitHub Workflow 的 Run ID |
| `artifact-path` | 生成的 `_site` 目录的绝对路径 |

## 使用示例

```yaml
- name: Deploy with TE2 Action
  id: te2-deploy
  uses: YOUR_USERNAME/te2-deploy-action@v1
  with:
    image-src: 'Images'
    icons-src: 'favicon.jpg'
    ex-dir: 'private, temp'
- name: Show Outputs
  run: |
    echo "Run ID: ${{ steps.te2-deploy.outputs.run-id }}"
    echo "Artifact Path: ${{ steps.te2-deploy.outputs.artifact-path }}"
```

## 进阶用法

- 在 monorepo 中使用时，可通过 ex-dir 排除子模块目录。
- 结合矩阵策略同时部署多个站点。
- 在后续 Job 中使用 artifact-path 进行自定义处理（如压缩或上传到其他 CDN）。

## 推荐使用场景

- 个人知识库 / Wiki 项目（Markdown 驱动的静态站点）
- 文档型 GitHub Pages 站点
- 需要自动处理内部链接和资源复制的博客系统
- 希望复用标准化部署流程的开源项目

## 注意事项

- 仓库必须启用 GitHub Pages 功能。
- Pandoc 版本由 pandoc/actions/setup 提供，如需特定版本可自行调整。
- 图片等大文件会影响构建时间，建议合理组织资源。
- ex-dir 参数会追加到默认排除列表中。
- 首次使用建议手动触发 workflow_dispatch 测试。
- Action 运行在 ubuntu-latest 环境，Python 3.x。
