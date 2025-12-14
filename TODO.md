# TODO - AI Data Visualizer

## 📝 Summary of Today's Work (2025-12-14)

### What We Accomplished:

1. **Fixed Deployment Issues**
   - ✅ Removed burger menu and hard-coded Hugging Face as backend provider
   - ✅ Resolved "proxies" error by removing OpenAI client library
   - ✅ Fixed 410 error (old API deprecated)
   - ✅ Navigated HF Router API transition
   - ✅ Added billing and got the router working

2. **Upgraded AI Model**
   - Started with: `meta-llama/Llama-3.2-3B-Instruct` (poor quality)
   - Ended with: `Qwen/Qwen2.5-72B-Instruct` (much better quality)
   - Result: App generates 3 charts with real insights now!

3. **Current State**
   - ✅ Deployed on Hugging Face Spaces
   - ✅ Using HF Router with billing enabled
   - ✅ Working end-to-end (upload → analyze → visualize)
   - ⚠️ Quality is "good but not Claude-level"

---

## 🔴 CRITICAL REMINDERS

### API Configuration
- **HF Router Endpoint**: `https://router.huggingface.co/v1/chat/completions`
- **Current Model**: `Qwen/Qwen2.5-72B-Instruct`
- **Requires**: Billing enabled on HF account
- **API Key**: Stored in HF Space Settings → Repository secrets

### Code Structure
- **Provider disabled**: Anthropic (set `enabled: False` in config.py)
- **Only active provider**: Hugging Face
- **No burger menu**: Removed from UI (templates/index.html)
- **Hard-coded provider**: Set to `huggingface` in static/js/app.js

### Deployment Process
```bash
# Always use clean orphan branch for HF deployment (avoids PDF binary file errors)
git checkout --orphan deploy-branch
git add -A
git commit -m "Deploy message"
git push huggingface deploy-branch:main --force
git checkout master && git branch -D deploy-branch
```

### Files That Must Stay in .gitignore
- `.env` (API keys)
- `venv/` (Python virtual environment)
- `uploads/`, `temp/`, `test_data/` (user data)
- `SECURE NOT TO DEPLOY/` (sensitive files)
- `*.pdf` files (binary files rejected by HF)
- `Antrophic API key.txt` (API key file)

---

## 🎯 NEXT STEP: Add "Bring Your Own Claude Key" Feature

### Goal
Allow users to optionally use their own Anthropic Claude API key for better quality results.

### Requirements
- ✅ No user accounts
- ✅ No saved history
- ✅ API key stored in memory only (until page refresh)
- ✅ Users enter key each session
- ✅ Option A: Key persists in JavaScript memory until page refresh

### Implementation Plan

#### Phase 1: Restore UI Components
1. **Bring back burger menu**
   - Add back burger menu HTML to `templates/index.html`
   - Restore burger menu CSS to `static/css/styles.css`
   - Restore burger menu JavaScript to `static/js/app.js`

2. **Add provider selection**
   ```
   ☰ Menu
   ├─ 🟢 Hugging Face (Free, uses server key)
   └─ 🟦 Anthropic Claude (Best quality, BYOK)
       └─ [Input field for API key]
           💡 Your key stays in browser memory only
   ```

#### Phase 2: Frontend Implementation
1. **JavaScript changes** (`static/js/app.js`)
   ```javascript
   // Global variable (memory only, not persisted)
   let userClaudeKey = null;

   // Function to store key in memory
   function setClaudeKey(key) {
       userClaudeKey = key;
       // Validate format (starts with 'sk-ant-')
   }

   // Include key in API request
   function analyzeData() {
       fetch('/analyze', {
           method: 'POST',
           body: JSON.stringify({
               provider: currentProvider,
               user_api_key: userClaudeKey,  // Send if Anthropic selected
               // ... other data
           })
       });
   }
   ```

2. **UI updates**
   - Add API key input field (hidden by default)
   - Show input when "Anthropic Claude" is selected
   - Add helper text: "Not saved • Secure • Reset on refresh"
   - Add validation indicator (✓ key format valid)

#### Phase 3: Backend Changes
1. **Update `app.py`**
   ```python
   @app.route('/analyze', methods=['POST'])
   def analyze():
       provider_name = request.json.get('provider', 'huggingface')
       user_api_key = request.json.get('user_api_key')  # Optional

       # Create provider with user's key if provided
       if provider_name == 'anthropic' and user_api_key:
           provider = AnthropicProvider(api_key=user_api_key)
       else:
           provider = ProviderFactory.get_provider(provider_name)

       # Rest of analysis logic...
       # user_api_key is discarded after this function
   ```

2. **Update `anthropic_provider.py`**
   ```python
   class AnthropicProvider(BaseProvider):
       def __init__(self, api_key=None):
           # Use provided key OR fall back to env variable
           self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
           self.client = anthropic.Anthropic(api_key=self.api_key)
   ```

3. **Re-enable Anthropic in `config.py`**
   ```python
   AI_PROVIDERS = {
       'anthropic': {'name': 'Anthropic Claude', 'enabled': True},
       'huggingface': {'name': 'Hugging Face', 'enabled': True},
   }
   ```

#### Phase 4: Security & UX Polish
1. **Security measures**
   - ✅ API key never saved to localStorage/cookies
   - ✅ Sent over HTTPS only
   - ✅ Not logged on server
   - ✅ Input type="password" or with toggle visibility
   - ✅ Clear from memory on page unload

2. **Error handling**
   - Invalid API key → Show clear error message
   - API key format validation (starts with `sk-ant-`)
   - Network errors → Suggest checking key

3. **UX improvements**
   - Show "Using your Claude key" indicator when active
   - Add "Test Key" button (optional)
   - Clear instructions: "Get your key from console.anthropic.com"
   - Loading state: "Analyzing with Claude..."

#### Phase 5: Testing Checklist
- [ ] Burger menu opens/closes correctly
- [ ] Provider selection switches between HF and Claude
- [ ] API key input appears only for Claude
- [ ] Key validation works (format check)
- [ ] Analysis works with user's Claude key
- [ ] Analysis falls back to HF if no key provided
- [ ] Key is cleared on page refresh
- [ ] Error messages are clear and helpful
- [ ] Works on mobile devices

---

## 📋 Additional Future Ideas (Not Urgent)

### Quality Improvements
- [ ] Add more chart types (scatter matrix, heatmap, etc.)
- [ ] Improve prompt engineering for better insights
- [ ] Add data preprocessing options

### Features
- [ ] Allow users to edit/customize charts
- [ ] Save/share chart configurations (without data)
- [ ] Add chart export formats (SVG, high-res PNG)

### Infrastructure
- [ ] Add rate limiting to prevent abuse
- [ ] Add usage analytics (privacy-respecting)
- [ ] Consider adding more AI providers (Groq, Together AI)

---

## 🚨 Known Issues

1. **Model Quality**
   - Qwen 2.5 72B is good but not Claude-level
   - Sometimes generates only 1-2 charts instead of 3
   - JSON parsing can fail with complex data

2. **Cost**
   - HF Router requires billing (not truly "free")
   - Need to monitor costs for users

3. **Performance**
   - First request can be slow (model cold start)
   - Large datasets may timeout

---

## 📚 Documentation to Update

After implementing BYOK feature:
- [ ] Update README.md with new feature info
- [ ] Update DEPLOYMENT_GUIDE.md if needed
- [ ] Add screenshots to show burger menu
- [ ] Document API key security approach

---

**Last Updated**: 2025-12-14
**Next Session**: Implement "Bring Your Own Claude Key" feature
