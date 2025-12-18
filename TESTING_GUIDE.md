# Testing Guide for Chat Enhancements

## 🚀 Quick Start

### 1. Start Backend
```bash
cd Backend
python app.py
```
The backend should start on `http://localhost:5000`

### 2. Start Frontend
```bash
cd Frontend
npm run dev
```
The frontend should start on `http://localhost:5173` (or similar)

---

## ✅ Feature Testing Checklist

### 🧭 ChatGPT-Like Sidebar

**Test Steps:**
1. Navigate to the chat page
2. **Verify**: Left sidebar appears with "+ New Chat" button
3. Click "+ New Chat"
4. **Verify**: New empty chat session starts
5. Send a message
6. **Verify**: Session appears in sidebar with message as title
7. Click "+ New Chat" again
8. Send another message
9. **Verify**: Two sessions now visible in sidebar
10. Click on first session
11. **Verify**: Previous conversation loads correctly
12. Hover over a session
13. **Verify**: Delete (trash) icon appears
14. Click delete icon
15. **Verify**: Session removed from sidebar and database

**Mobile Testing:**
1. Resize browser to mobile width (<1024px)
2. **Verify**: Sidebar collapses
3. **Verify**: Hamburger menu button appears in top-left
4. Click hamburger button
5. **Verify**: Sidebar slides in as overlay
6. **Verify**: Dark backdrop appears behind sidebar
7. Click backdrop
8. **Verify**: Sidebar closes

---

### 🎙️ Voice Input

**Test Steps:**
1. Click microphone icon in input area
2. **Verify**: Button turns red
3. **Verify**: "Listening..." indicator appears
4. **Verify**: Mic icon pulses/animates
5. Speak a medical query (e.g., "What are symptoms of diabetes?")
6. Stop speaking and wait 2-3 seconds
7. **Verify**: Text appears in input box
8. **Verify**: Toast notification shows captured text
9. **Verify**: Button returns to normal state
10. Type additional text manually
11. Click mic again and speak more
12. **Verify**: New speech appends to existing text (not replace)

**Browser Compatibility:**
- Chrome/Edge: ✅ Full support
- Firefox: ⚠️ May need flag enabled
- Safari: ⚠️ Limited support

---

### 🖼️ Image Upload

**Test Image Only:**
1. Click image icon in input area
2. Select an image file
3. **Verify**: Preview appears above input bar (80x80px thumbnail)
4. **Verify**: X button appears on preview
5. **Verify**: Toast notification shows "Image attached"
6. Click Send (without typing text)
7. **Verify**: Image appears in chat bubble
8. **Verify**: Message saved to database

**Test Image + Text:**
1. Click image icon
2. Select image
3. Type a message (e.g., "What does this show?")
4. Click Send
5. **Verify**: Both text and image appear in chat bubble
6. **Verify**: Image displays under text
7. **Verify**: Both saved to database

**Test Remove Image:**
1. Click image icon and select image
2. **Verify**: Preview appears
3. Click X button on preview
4. **Verify**: Preview disappears
5. **Verify**: File input cleared
6. Select image again
7. **Verify**: Works normally after removal

---

### 💬 Chat Sessions

**Test Session Creation:**
1. Start fresh (or click "+ New Chat")
2. Send first message
3. **Verify**: Session automatically created in database
4. **Verify**: Session appears in sidebar with message as title
5. Send more messages
6. **Verify**: All messages saved to same session

**Test Session Switching:**
1. Create 3 different chat sessions
2. Click on session #1
3. **Verify**: Messages from session #1 load
4. Click on session #2
5. **Verify**: Messages switch to session #2
6. **Verify**: Smooth transition animation
7. **Verify**: Input area clears on switch

**Test Session Persistence:**
1. Create a chat session
2. Send several messages
3. Refresh the page
4. **Verify**: Session still appears in sidebar
5. Click on the session
6. **Verify**: All messages load correctly

---

### 🕐 Timestamp Display

**Test Steps:**
1. Send a message
2. Hover mouse over the message bubble
3. **Verify**: Timestamp appears below message
4. **Verify**: Format like "Nov 5, 10:07 PM"
5. **Verify**: Smooth fade-in animation
6. Move mouse away
7. **Verify**: Timestamp fades out

---

### 📜 Auto-Scroll

**Test Steps:**
1. Start a new chat
2. Send 10-15 messages to fill the screen
3. **Verify**: Chat scrolls automatically to show latest message
4. Scroll up manually to view older messages
5. Send a new message
6. **Verify**: View automatically scrolls to bottom
7. **Verify**: Scroll animation is smooth

---

### 💭 Typing Indicator

**Test Steps:**
1. Send a message
2. **Verify**: Three animated dots appear while waiting for response
3. **Verify**: Dots pulse up and down
4. Wait for AI response
5. **Verify**: Dots disappear when response arrives
6. **Verify**: Response appears smoothly

---

### 🎨 Responsive Design

**Desktop (>1024px):**
1. **Verify**: Both sidebars visible
2. **Verify**: Chat history sidebar on left (288px)
3. **Verify**: Navigation sidebar next to it (256px)
4. **Verify**: Main chat area has proper margins
5. Click sidebar collapse button
6. **Verify**: Sidebar smoothly collapses

**Tablet (768px - 1024px):**
1. **Verify**: Chat history sidebar becomes overlay
2. **Verify**: Hamburger menu button visible
3. **Verify**: Original sidebar still shows

**Mobile (<768px):**
1. **Verify**: Both sidebars hidden by default
2. **Verify**: Hamburger button in top-left
3. **Verify**: Input area spans full width
4. **Verify**: Chat bubbles adjust width appropriately
5. **Verify**: All buttons remain accessible

---

### 🗑️ Delete Session

**Test Steps:**
1. Create a test chat session
2. Send a few messages
3. Hover over the session in sidebar
4. **Verify**: Trash icon appears
5. Click trash icon
6. **Verify**: Session removed from sidebar immediately
7. Check database
8. **Verify**: All messages for that session deleted
9. If it was active session:
   - **Verify**: New empty chat starts automatically

---

## 🐛 Common Issues & Solutions

### Backend Not Connecting
- Check MySQL is running
- Verify database credentials in `Backend/app.py`
- Ensure `user_auth` database exists
- Check Flask server is running on port 5000

### Voice Input Not Working
- Check browser supports Web Speech API
- Grant microphone permissions when prompted
- Try using Chrome/Edge for best compatibility
- Check console for error messages

### Images Not Displaying
- Check image file is valid format (JPG, PNG, etc.)
- Verify image_url column exists in database
- Check browser console for errors
- Ensure base64 encoding is working

### Sidebar Not Showing Sessions
- Check database connection
- Verify sessions exist in `chat_history` table
- Check browser console for API errors
- Refresh the page

---

## 📊 Database Verification

### Check Sessions Table
```sql
SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 20;
```

### Check Specific Session
```sql
SELECT * FROM chat_history WHERE session_id = 'your_session_id';
```

### Verify Image URLs
```sql
SELECT id, session_id, message, image_url FROM chat_history WHERE image_url IS NOT NULL;
```

---

## 🎯 Expected Behavior Summary

✅ **Sidebar**: Shows all user sessions, allows switching, "+ New Chat" creates new session  
✅ **Voice**: Click mic → speak → text appears → click send  
✅ **Images**: Upload → preview → send with/without text → displays in chat  
✅ **Sessions**: Auto-create, switch seamlessly, delete functionality  
✅ **Timestamps**: Show on hover, smooth animations  
✅ **Auto-scroll**: Always shows latest message  
✅ **Responsive**: Works on all screen sizes  
✅ **Persistence**: Everything saved to MySQL database

---

## 📝 Notes

- User ID is currently hardcoded as `1` - update after implementing authentication
- Session IDs are auto-generated with timestamp + random string
- All images stored as base64 data URLs in database
- Voice input appends to existing text (doesn't replace)
- Timestamps use local timezone
- Delete operations are permanent (no soft delete)

Happy testing! 🎉
