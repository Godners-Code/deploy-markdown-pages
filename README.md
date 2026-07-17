<!-- markdownlint-disable MD025 MD033 MD060 -->
# Markdown to GitHub Pages Deploy

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Godners-Code/deploy-markdown-pages)](https://github.com/Godners-Code/deploy-markdown-pages/releases)
[![License](https://img.shields.io/github/license/Godners-Code/deploy-markdown-pages)](https://github.com/Godners-Code/deploy-markdown-pages/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Godners-Code/deploy-markdown-pages)](https://github.com/Godners-Code/deploy-markdown-pages/stargazers)

一个 GitHub Action，用于将 Markdown 文件转换为 HTML（基于 Pandoc），自动处理内部链接、复制资源文件，并部署到 GitHub Pages。

---

## 介绍

**deploy-markdown-pages** 是一个轻量、灵活的复合 GitHub Action，专为 Markdown 驱动的静态站点设计。它能自动完成从源码到可发布站点的全流程转换与部署，适合个人文档、知识库、博客等项目使用。

---

## 特性

- 支持批量将 .md 文件转换为带元数据的 HTML
- 自动将内部 .md 链接转换为 .html （保留锚点和查询参数）
- 支持复制图片目录、favicon、robots.txt 和 index.html
- 可自定义页面标题、资源路径和排除目录
- 输出 Workflow Run ID 和构建产物绝对路径
- 兼容 GitHub Pages 官方部署流程
- 代码简洁、易扩展

---

## 使用示例

```yaml
name: Deploy Markdown to GitHub Pages

on:
  workflow_dispatch:
  push:
    paths-ignore:
      - '.github/**'

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@main
      - name: Deploy using Markdown Action
        id: deploy
        uses: Godners-Code/deploy-markdown-pages@main
        with:
          page-title: '我的知识库'
          image-src: 'Images'
          ex-dir: 'drafts,archive'

```

---

## 输入参数

| 参数名称     | 描述                              | 默认值                  | 是否必填 |
|--------------|-----------------------------------|-------------------------|----------|
| page-title   | 页面标题     | 仓库名称                | 否       |
| image-src    | 图片源目录     | Images                  | 否       |
| image-dst    | 图片目标路径                      | Images                  | 否       |
| home-target  | 首页重定向目标 | README.html             | 否       |
| icons-src    | favicon.jpg 源路径                | favicon.jpg             | 否       |
| robot-src    | robots.txt 源路径                 | robots.txt              | 否       |
| ex-dir       | 额外排除目录（逗号分隔）          | （默认已排除 _site,.git,.github） | 否       |

---

## 进阶用法

- **自定义首页重定向**：通过 index.html 模板 + `home-target` 实现自动跳转。
- **多站点部署**：结合矩阵策略同时构建多个语言/版本的站点。
- **Jinja2 模板**：进阶用户可修改 index.j2 以支持更复杂逻辑。

---

## 推荐使用场景

- 个人知识库 / Wiki（Obsidian、Typora 等 Markdown 笔记）
- 项目文档站点
- 技术博客
- 需要简单链接转换和资源复制的静态页面
- 希望统一部署流程的开源/团队项目

---

## 注意事项

- 仓库需启用 GitHub Pages 功能（Settings → Pages）。
- 大量图片或 Markdown 文件可能增加构建时间。
- 建议将资源文件置于仓库根目录或指定路径下。
- `ex-dir` 参数用于避免处理不需要的目录。
- 首次使用建议通过 workflow_dispatch 手动触发测试。
- Action 运行环境为 ubuntu-latest。

---

## License

[MIT License](https://github.com/Godners-Code/deploy-markdown-pages/blob/main/LICENSE)

---

**欢迎 Star & Fork！**

有问题或功能建议欢迎提交 Issue。
