# OGMSGUI

![License](https://img.shields.io/badge/license-MIT-green)
A powerful GUI package for geographical modeling and simulation in Jupyter environments, integrating model invoking and AI assistance.

## 🌟 Features

- **Interactive Model Invoking**
  - Visual model selection and configuration
  - Real-time model execution and monitoring
  - Integrated file management system

- **AI-Powered Assistance**
  - AI integration for modeling guidance
  - Automatic task planning based on academic research
  - Context-aware suggestions and help

- **User-Friendly Interface**
  - Intuitive drag-and-drop interface
  - Real-time feedback and status updates

## 📦 Installation

```bash
pip install ogmsgui
```

## 🚀 Quick Start

### Basic Usage

<!-- 显示所有模型列表 -->
```python
from ogmsgui import ModelGUI

# 创建并显示GUI
gui = ModelGUI()
gui.create_gui()
```

<!-- 展示图片 -->
<!-- 展示模型界面 -->
![create gui](https://github.com/MpLebron/picRepo/blob/main/creategui.png?raw=true)

<!-- 调用某个具体的模型 -->
```
from ogmsgui import ModelGUI

# 创建并显示GUI
gui = ModelGUI()
gui.show_model("地震群发滑坡概率评估预警模型")
```
<!-- 展示show model -->
![show model](https://github.com/MpLebron/picRepo/blob/main/showmodel.png?raw=true)
![show model](https://github.com/MpLebron/picRepo/blob/main/invoke.png?raw=true)

### Using AI Assistant

```python
# Use the magic command for AI assistance
# 导入自定义模块
import ogmsgui

%ogmsChat 南京市光伏屋顶的碳减排潜力大概有多大
```

<!-- 展示ogmschat -->
![ogmsChat](https://github.com/MpLebron/picRepo/blob/main/ogmsChat.png?raw=true)

```python
import ogmsgui

# Get task planning suggestions
%ogms_taskPlan 南京市光伏屋顶的碳减排潜力该怎么进行估算呢
```

<!-- taskPlan -->
![ogmsChat](https://github.com/MpLebron/picRepo/blob/main/ogms_task.png?raw=true)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped with the development
- Special thanks to the geographical modeling community
- Built with support from [OpenGMS]

## 📬 Contact

- Author: Phileon Ma
- Email: mpllonggis@gmail.com

## 🔄 Updates

### Latest Version (0.1.0)
- Initial release with core functionality
- Basic model invoking features
- Basic AI functionality

### Roadmap
- [x] Enhanced AI capabilities
