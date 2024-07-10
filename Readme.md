# Feedback Bot

This is a simple feedback bot designed to facilitate communication between users and the administrator of a channel. The bot allows users to send messages to the administrator, who can then manage these messages.

## Features

- Users can send messages to the bot.
- The bot forwards the messages, along with user data, to the administrator.
- The administrator can:
  - Block users and delete all their messages.
  - Reply to user messages.
  - Delete specific messages in their chat.
  - Broadcast messages to all active users.

## Also

- Flood filter with adjustable delay to prevent flood.

## Limitations

- The bot operates on polling.
- Only one attachment can be included per message.

## Database Structure(Mongo)

### Database: `feedback`

#### Collection: `users`


## Setup

1. Install the dependencies listed in `r.txt`:
   ```bash
   pip install -r r.txt
1. Edit a `env_example.py` file and rename it to `env.py` and fill it with the necessary configuration data.
2. Run the `main.py` file to start the bot.

### Example env.py File
```python
botToken : str = 'TOKEN'
admin_id : int = 123456789
flood_delay : int = 10 #seconds
```
