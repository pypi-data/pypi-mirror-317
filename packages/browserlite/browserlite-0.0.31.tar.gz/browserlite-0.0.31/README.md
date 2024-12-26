# BrowserLite 🚀

BrowserLite is a lightweight Python library for browser automation, specifically designed to interact with popular search services and AI chat interfaces like Google Search, ChatGPT, and HuggingChat. It provides a simple, intuitive API for automated browsing and text extraction.

## 🌟 Features

- Simple, intuitive API for browser automation
- Support for multiple browsers (Chrome, Edge, Firefox)
- Built-in integration with popular services:
  - Google Search
  - ChatGPT
  - HuggingChat
- Automated text extraction and processing
- Configurable delays and safety settings
- Cross-platform compatibility

## 🔧 Installation

```bash
pip install browserlite
```

## 🚀 Quick Start

### Basic Usage

```python
from browserlite import browse, chatgpt, huggingchat

# Basic Google search
result = browse("Python programming best practices")

# ChatGPT interaction
response = chatgpt("Explain quantum computing in simple terms")

# HuggingChat interaction
response = huggingchat("Write a short story about AI")
```

### Advanced Usage

```python
from browserlite import browse

# Specify browser and search service
result = browse(
    query="machine learning tutorials",
    service_name="google",
    browser="google-chrome",
    base_url="https://www.google.com"
)

# Use ChatGPT with custom browser
response = browse(
    query="Write a poem about technology",
    service_name="chatgpt",
    browser="firefox"
)
```

## 🎯 Why BrowserLite?

1. **Simplicity First**: Get started with just one line of code
2. **Flexibility**: Choose your preferred browser and search service
3. **AI Integration**: Built-in support for popular AI chat services
4. **Automation**: Automate repetitive browsing tasks efficiently
5. **Cross-Platform**: Works on Windows, macOS, and Linux

## 📝 Configuration

You can customize the automation behavior using the `AutomationConfig` class:

```python
from browserlite.config import AutomationConfig, BaseDelay

# Custom delay settings
custom_delays = BaseDelay(
    safety_delay=2,
    edge_open_delay=2,
    chrome_open_delay=3,
    firefox_open_delay=3,
    search_delay=1.5,
    max_search_time=50,
    chatgpt_text_process_time=2
)

config = AutomationConfig(delays=custom_delays)
```

## 🔍 Supported Services

| Service | Description | Example |
|---------|-------------|---------|
| Google | Standard web search | `browse("query", service_name="google")` |
| ChatGPT | OpenAI's ChatGPT | `chatgpt("query")` |
| HuggingChat | Hugging Face's chat | `huggingchat("query")` |

## 🌐 Supported Browsers

- Google Chrome (`google-chrome`)
- Microsoft Edge (`microsoft-edge-stable`)
- Firefox (`firefox`)

## 📚 Examples

### 1. Web Search Automation

```python
from browserlite import browse

# Simple Google search
result = browse("latest tech news")

# Custom search with specific browser
tech_news = browse(
    query="AI developments 2024",
    service_name="google",
    browser="google-chrome"
)
```

### 2. AI Chat Interactions

```python
from browserlite import chatgpt, huggingchat

# ChatGPT conversation
code_review = chatgpt("Review this Python code: def hello(): print('world')")

# HuggingChat interaction with custom URL
story = huggingchat(
    "Write a creative story about a robot",
    base_url="https://huggingface.co/chat/"
)
```

## ⚠️ Important Notes

1. Make sure you have the desired browser installed on your system
2. Some services might require authentication
3. Respect the terms of service of the platforms you're automating
4. Consider rate limits and usage policies of the services

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Help and Support

- Report issues on GitHub
- Check the documentation
- Join our community discussions

## 🙏 Acknowledgments

- PyAutoGUI for automation capabilities
- Python community for inspiration
- All contributors and users

---

Made with ❤️