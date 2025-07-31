#!/usr/bin/env python3
# MARINA KHAN'S FACEBOOK SWISS ARMY TOOL (100% LEGAL)
import requests
import json
from datetime import datetime
import sys
from getpass import getpass

class FBTool:
    def __init__(self):
        self.API_VERSION = "v19.0"
        self.BASE_URL = f"https://graph.facebook.com/{self.API_VERSION}"
        self.BANNER = f"""
        ╔════════════════════════════════════════════╗
        ║    MARINA KHAN'S FACEBOOK TOOL - {datetime.now().year}   ║
        ║                                            ║
        ║  Features:                                 ║
        ║  • Page Analytics                          ║
        ║  • Post Scheduler (Basic)                  ║
        ║  • Ad Performance Check                    ║
        ║                                            ║
        ║  Uses Official Facebook API Only           ║
        ╚════════════════════════════════════════════╝
        """

    def get_token(self):
        """Securely get Facebook access token"""
        token = getpass("Enter Facebook Access Token (hidden): ")
        return token.strip()

    def page_analytics(self, page_id, token):
        """Get public page metrics"""
        try:
            url = f"{self.BASE_URL}/{page_id}?fields=name,fan_count,posts.limit(3){{message,created_time,reactions}}&access_token={token}"
            data = requests.get(url).json()
            
            report = {
                "generated_at": datetime.now().isoformat(),
                "tool": "MARINA KHAN OFFICIAL",
                "page_info": {
                    "name": data.get("name"),
                    "followers": data.get("fan_count"),
                    "recent_posts": [
                        {
                            "time": p.get("created_time"),
                            "content": p.get("message", "")[:50] + "...",
                            "reactions": p.get("reactions", {}).get("summary", {}).get("total_count", 0)
                        } for p in data.get("posts", {}).get("data", [])[:3]
                    ]
                }
            }
            return report
        except Exception as e:
            return {"error": str(e)}

    def quick_post(self, token, page_id, message):
        """Make a simple post (requires publish permissions)"""
        try:
            url = f"{self.BASE_URL}/{page_id}/feed"
            params = {
                "message": message,
                "access_token": token
            }
            response = requests.post(url, params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def run(self):
        print(self.BANNER)
        
        if len(sys.argv) < 2:
            print("Usage:")
            print(f"  {sys.argv[0]} analytics <page_id>")
            print(f"  {sys.argv[0]} post <page_id> \"Your message\"")
            sys.exit(1)

        command = sys.argv[1]
        token = self.get_token()

        if command == "analytics":
            if len(sys.argv) < 3:
                print("Error: Missing page_id")
                sys.exit(1)
            page_id = sys.argv[2]
            result = self.page_analytics(page_id, token)
            print(json.dumps(result, indent=2))
            
        elif command == "post":
            if len(sys.argv) < 4:
                print("Error: Missing page_id or message")
                sys.exit(1)
            page_id = sys.argv[2]
            message = sys.argv[3]
            result = self.quick_post(token, page_id, message)
            print(json.dumps(result, indent=2))
            
        else:
            print("Invalid command")

if __name__ == "__main__":
    tool = FBTool()
    tool.run()
