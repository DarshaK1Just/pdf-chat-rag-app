"""
HTML and CSS templates for the Streamlit UI - Claude-style Chat Interface.
"""

CSS = '''
<style>
/* Chat Container */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem 0;
}

/* Message Bubbles */
.chat-message {
    display: flex;
    margin-bottom: 1.5rem;
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* User Message - Right Side */
.chat-message.user {
    justify-content: flex-end;
}

.chat-message.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.875rem 1.125rem;
    max-width: 75%;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    font-size: 0.95rem;
    line-height: 1.5;
    word-wrap: break-word;
}

/* Bot Message - Left Side */
.chat-message.bot {
    justify-content: flex-start;
}

.chat-message.bot .message-wrapper {
    display: flex;
    align-items: flex-start;
    max-width: 85%;
}

.chat-message.bot .avatar {
    flex-shrink: 0;
    margin-right: 0.75rem;
}

.chat-message.bot .avatar img {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid #e5e7eb;
    object-fit: cover;
}

.chat-message.bot .message-content {
    background: #f3f4f6;
    color: #1f2937;
    border-radius: 4px 18px 18px 18px;
    padding: 0.875rem 1.125rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    font-size: 0.95rem;
    line-height: 1.6;
    word-wrap: break-word;
}

/* User Avatar - Right Side */
.chat-message.user .avatar {
    flex-shrink: 0;
    margin-left: 0.75rem;
}

.chat-message.user .avatar img {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid #667eea;
    object-fit: cover;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .chat-message.bot .message-content {
        background: #374151;
        color: #f9fafb;
    }
    
    .chat-message.bot .avatar img {
        border-color: #4b5563;
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .chat-message.user .message-content,
    .chat-message.bot .message-wrapper {
        max-width: 90%;
    }
    
    .chat-message.bot .avatar img,
    .chat-message.user .avatar img {
        width: 32px;
        height: 32px;
    }
}
</style>
'''

BOT_TEMPLATE = '''
<div class="chat-message bot">
    <div class="message-wrapper">
        <div class="avatar">
            <img src="https://cdn-icons-png.flaticon.com/512/6134/6134346.png" 
                 alt="AI Assistant">
        </div>
        <div class="message-content">{{MSG}}</div>
    </div>
</div>
'''

USER_TEMPLATE = '''
<div class="chat-message user">
    <div class="message-content">{{MSG}}</div>
    <div class="avatar">
        <img src="https://png.pngtree.com/png-vector/20190321/ourmid/pngtree-vector-users-icon-png-image_856952.jpg" 
             alt="You">
    </div>
</div>
'''