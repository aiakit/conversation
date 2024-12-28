# HomingAI Conversation for Home Assistant

这是一个 Home Assistant 的智能对话代理集成，基于 HomingAI 的大语言模型，让您的智能家居系统能够理解自然语言指令并做出响应。

## ✨ 功能特点

- 🎯 智能对话：自然语言理解，精准执行指令
- 🌍 中文支持：完美支持中文交互体验
- ⚡ 实时响应：快速处理对话请求
- 📱 场景丰富：支持查询、控制、场景联动等
- 🔒 安全可靠：数据传输加密，保护隐私
- 🤖 上下文感知：支持多轮对话，理解上下文

## 📦 安装方法

### HACS 安装（推荐）

1. 确保已经安装了 [HACS](https://hacs.xyz/)
2. HACS > 集成 > 右上角菜单 > Custom repositories
3. 添加仓库：`https://github.com/aiakit/conversation`
4. 类别选择：Integration
5. 在 HACS 集成页面搜索 "HomingAI Conversation"
6. 点击下载
7. 重启 Home Assistant

### 手动安装

1. 下载此仓库的最新版本
2. 将 `custom_components/homingai_conversation` 文件夹复制到您的 `custom_components` 目录
3. 重启 Home Assistant

## ⚙️ 配置说明

[![Open your Home Assistant instance and show an integration.](https://my.home-assistant.io/badges/integration.svg)](https://my.home-assistant.io/redirect/integration/?domain=homingai_conversation)

1. 在 Home Assistant 的配置页面中添加集成
2. 搜索 "HomingAI STT"
3. 完成HomingAi的授权
4. 点击“提交”完成配置
5. 到语音助手配置homingai_conversation

## 🎯 使用方法

1. 在 Home Assistant 的对话框中直接输入指令，例如：
   - "打开客厅的灯"
   - "现在室内温度是多少？"
   - "帮我设置一个睡眠模式"

2. 在自动化中使用：
   - 可以配置触发条件后的对话响应
   - 支持语音助手接入使用

## ⚠️ 注意事项

- 确保网络连接稳定
- 正确配置授权信息
- 注意 API 调用限制
- 妥善保管 Client ID 和 Client Secret

## 🔧 故障排除

如果遇到问题，请检查：

1. 授权信息是否正确
2. 网络连接是否正常
3. Home Assistant 日志中的错误信息
4. 查看[技术文档](https://homingai.com)获取更多帮助

## 📝 问题反馈

如果您遇到任何问题或有改进建议，欢迎通过以下方式反馈：

- [提交 Issue](https://github.com/aiakit/conversation/issues)
- [技术支持](https://homingai.com)

## 📄 许可证

本项目采用 Apache License 2.0 许可证，详见 [LICENSE](LICENSE) 文件。

## 🔄 更新日志

### v1.0.0 (2024-03-19)
- ✨ 初始版本发布
- 🎯 支持自然语言对话
- 🌍 支持中文交互
- ⚡ 优化响应性能
- 📱 完善配置界面

## 🤝 贡献指南

欢迎提交 Pull Request 或者建立 Issue。

---

Made with ❤️ by HomingAI Team