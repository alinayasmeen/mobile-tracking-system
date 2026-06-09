---
name: python-dependency-resolution
description: Resolve Python package dependency conflicts in mobile tracking systems
source: auto-skill
extracted_at: '2026-06-09T04:35:53.607Z'
---

# Python Dependency Resolution for Mobile Tracking Systems

## Overview
This skill provides a systematic approach to resolving Python package dependency conflicts, particularly for complex systems like mobile tracking applications with AI components.

## Common Dependency Conflicts in Mobile Tracking Systems

### 1. Pydantic Version Conflicts
**Problem:** Multiple packages require different versions of Pydantic
```
openai-agents 0.8.3 depends on pydantic>=2.12.3
fastapi 0.109.0 depends on pydantic!=1.8, !=1.8.1, !=2.0.0, !=2.0.1, !=2.1.0, <3.0.0 and >=1.7.4
```

**Solution:** Use version ranges instead of exact versions
```txt
# Change from:
pydantic==2.5.3
# To:
pydantic>=2.12.3
```

### 2. OpenAI Version Conflicts
**Problem:** Different packages require different OpenAI versions
```
openai-agents 0.8.3 depends on openai>=2.9.0
requirements.txt specified openai==1.12.0
```

**Solution:** Update to compatible version range
```txt
# Change from:
openai==1.12.0
# To:
openai>=2.9.0
```

### 3. Python-Multipart Conflicts
**Problem:** MCP packages require newer python-multipart versions
```
mcp 1.27.2 depends on python-multipart>=0.0.9
requirements.txt specified python-multipart==0.0.6
```

**Solution:** Update to minimum required version
```txt
# Change from:
python-multipart==0.0.6
# To:
python-multipart>=0.0.9
```

## Resolution Workflow

### Step 1: Identify Conflicts
Run the install command to see specific conflicts:
```bash
pip install -r requirements.txt
```

### Step 2: Update Requirements File
For each conflict, update the requirements.txt:
1. Replace exact versions (`==`) with minimum versions (`>=`)
2. Prioritize the highest required version from conflicting packages

### Step 3: Update Yanked Versions
Check for and update yanked packages:
```txt
# Change from:
email-validator==2.1.0  # Yanked version
# To:
email-validator>=2.1.0
```

### Step 4: Retry Installation
```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation
Check if packages installed correctly:
```bash
pip show <package-name>
```

## Special Considerations for AI Agents

### Agent-Specific Dependencies
Mobile tracking systems with AI agents often have special requirements:
```txt
# For OpenAI/Gemini agents:
openai-agents==0.8.3
openai>=2.9.0
python-dotenv==1.0.0
```

### Environment Variables
Ensure required environment variables are set:
```bash
# For Gemini API access
export GEMINI_API_KEY=your_api_key_here
```

## Best Practices

1. **Use version ranges** instead of exact versions when possible
2. **Regularly update** requirements.txt to avoid outdated packages
3. **Test after each change** to ensure compatibility
4. **Document dependencies** that require special handling
5. **Consider using virtual environments** for isolation

## Troubleshooting

### If conflicts persist:
1. Remove specific version constraints and let pip resolve:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
2. Check for transitive dependencies causing conflicts
3. Consider using `pipdeptree` to visualize dependency trees

### For agent services:
1. Verify API keys are properly configured
2. Check that the agent service can start independently:
   ```bash
   python agents/agent_service.py
   ```

## Example Requirements.txt Structure

```txt
# Core framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart>=0.0.9

# AI/ML Components
pydantic>=2.12.3
pydantic-settings==2.1.0
openai>=2.9.0
openai-agents==0.8.3
email-validator>=2.1.0

# Utilities
python-dotenv==1.0.0
bcrypt==4.1.2
requests==2.32.5
```