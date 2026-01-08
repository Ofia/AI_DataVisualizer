# TODO - AI Data Visualizer

## 🎯 NEXT SESSION: Add BYOK (Bring Your Own Key) Claude Feature

### Goal
Add a burger menu in the top right corner allowing users to choose between:
- **Qwen 2.5 72B (Free/Default)** - Uses Hugging Face Router API
- **Claude API (BYOK)** - Users provide their own Anthropic API key

### Key Requirements
- API key stored in session only (cleared when browser closes)
- OAuth-style API key registration flow with modal
- Warning message about session-only storage
- Visual indicator of active model

---

## 📋 Implementation Plan

### 1. Frontend UI Components

#### Burger Menu
- Add burger menu icon (☰) in top right corner of the page
- Create dropdown menu with two options:
  - "Qwen 2.5 72B (Free)" - default, with checkmark
  - "Claude API (BYOK)" - option to use own key
- Add visual indicator showing which model is currently active

#### API Key Modal/Dialog
- Text input field for API key (with password/show toggle)
- "Confirm" and "Cancel" buttons
- Warning message: "Your API key will only be stored for this session and will be cleared when you close the browser"
- Success message after key is saved
- Error handling for invalid keys

#### Files to Modify
- `templates/index.html` - Add burger menu HTML and modal structure
- `static/style.css` - Style burger menu, dropdown, and modal
- `static/script.js` - Add menu and API key handling logic

---

### 2. Backend Changes

#### Session Management
- Add Flask session configuration (using `flask.session`)
- Create new API endpoint: `/api/set-api-key`
  - Receives API key via POST
  - Validates key format/functionality
  - Stores in session
  - Returns success/error response
- Create endpoint: `/api/get-current-provider`
  - Returns current model selection and whether key is set

#### Provider Logic Updates
- Modify `ai_providers/provider_factory.py`:
  - Check session for user's API key first
  - Fall back to environment variable if no session key
- Update `ai_providers/anthropic_provider.py`:
  - Accept API key parameter in constructor
  - Support both session-based and environment variable keys

#### API Key Validation
- Ensure the key works before saving to session
- Basic format validation (starts with 'sk-ant-')
- Optional: Test API call to verify key is active

#### Files to Modify
- `app.py` - Add session config and new endpoints
- `ai_providers/provider_factory.py` - Session-aware provider selection
- `ai_providers/anthropic_provider.py` - Dynamic API key support
- `config.py` - Re-enable Anthropic provider if needed

---

### 3. JavaScript Logic

#### Menu Management
- Handle burger menu toggle (open/close)
- Handle model selection (switch between Qwen/Claude)
- Store model preference in localStorage (NOT the API key)

#### API Key Flow
- Show modal when Claude is selected and no key exists in session
- Capture API key input
- Send API key to backend via POST to `/api/set-api-key`
- Handle success/error responses
- Update UI to show active provider

#### Form Submission
- Update form submission to include selected provider
- Pass session info (backend handles the rest)

#### Files to Modify
- `static/script.js` (or `static/js/app.js`)

---

### 4. Security & Best Practices

#### Security Measures
- API key stored in Flask session (server-side, encrypted)
- Never store key in localStorage or cookies
- Session expires when browser closes
- Key transmitted over HTTPS only
- Don't log API keys in server logs

#### Error Handling
- Invalid API key format → Clear error message
- API call fails → Suggest checking key
- Network errors → Graceful fallback
- Session expired → Prompt to re-enter key

#### UX Polish
- Loading states during validation
- Success feedback when key is saved
- Clear indicator of which model is active
- Mobile-responsive design

---

## 🔄 Implementation Steps (Suggested Order)

1. **Backend Foundation**
   - Set up Flask session configuration
   - Create `/api/set-api-key` endpoint
   - Create `/api/get-current-provider` endpoint
   - Update provider_factory.py to check session

2. **Provider Updates**
   - Update anthropic_provider.py to accept dynamic API keys
   - Add key validation logic
   - Test with sample keys

3. **Frontend UI**
   - Add burger menu HTML to index.html
   - Create modal structure for API key input
   - Style all components in style.css

4. **JavaScript Integration**
   - Add menu toggle functionality
   - Add model selection logic
   - Implement API key submission flow
   - Handle success/error states

5. **Testing & Polish**
   - Test full flow: menu → select Claude → enter key → generate viz
   - Test session persistence
   - Test error cases
   - Mobile testing
   - Update README.md

---

## 📁 Files That Will Be Modified

- `templates/index.html` - Burger menu + modal
- `static/style.css` - Styling
- `static/script.js` (or `static/js/app.js`) - Menu logic
- `app.py` - Session + new endpoints
- `ai_providers/provider_factory.py` - Session check
- `ai_providers/anthropic_provider.py` - Dynamic keys
- `config.py` - Ensure Anthropic is enabled
- `README.md` - Document new feature

---

## 🚨 Important Reminders

### Current State
- Using Qwen/Qwen2.5-72B-Instruct via HF Router
- Anthropic provider exists but may be disabled
- HF Router requires billing on HF account

### Deployment Note
When deploying to Hugging Face Spaces:
```bash
git checkout --orphan deploy-branch
git add -A
git commit -m "Add BYOK Claude feature"
git push huggingface deploy-branch:main --force
git checkout master && git branch -D deploy-branch
```

### Environment Variables
- `HUGGINGFACE_API_KEY` - For default Qwen model
- `ANTHROPIC_API_KEY` - Optional fallback for Claude (not required for BYOK)

---

**Created**: 2026-01-08
**Status**: Ready to implement
**Expected**: Full BYOK Claude feature with session-based key management
