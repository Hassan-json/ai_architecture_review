# AI Architecture Review

AI-powered tool to review software architecture diagrams using OpenAI GPT-4 Vision. Provides analysis of issues, security concerns, scalability problems, and actionable recommendations.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

### 3. Run the Application

**Web UI** (Recommended):
```bash
python app.py
```
Then open http://localhost:5000 in your browser

**CLI**:
```bash
python cli.py -i path/to/diagram.png
```

## Usage

### Web Interface
1. Start server: `python app.py`
2. Open http://localhost:5000
3. Upload your architecture diagram
4. Get detailed review with mitigation strategies

### Command Line
```bash
# Basic usage
python cli.py -i architecture.png

# Save output to JSON file
python cli.py -i diagram.png -o review.json
```

### API Endpoint
```bash
curl -X POST -F "image=@architecture.png" http://localhost:5000/api/review
```

## What You Get

The AI analyzes your architecture and provides:
- **Issues & Anti-Patterns** - Problems and how to fix them
- **Security Concerns** - Vulnerabilities and mitigation steps
- **Scalability Issues** - Growth bottlenecks and solutions
- **Best Practices** - Missing practices and implementation guides
- **Priority Recommendations** - Top changes ranked by importance

## Supported Formats

PNG, JPEG, GIF, WebP, BMP (max 16MB)

## Cost

Uses GPT-4o-mini (~$0.001 per review). Monitor usage at [OpenAI Platform](https://platform.openai.com/usage)

## Project Structure

```
├── app.py              # Flask server
├── cli.py              # Command-line tool
├── config.py           # Configuration
├── services/
│   └── ai_reviewer.py  # AI integration
├── templates/
│   └── index.html      # Web UI
└── static/
    └── style.css       # Styles
```
