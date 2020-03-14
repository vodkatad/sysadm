from slacker import Slacker
import os

class SlackLogger:
    def __init__(self):

        self.token = os.getenv("SLACK_TOKEN")
        self.hostname = os.getenv('BIOINFO_HOST')
        if self.hostname == None:
            self.hostname = ''
        if not self.token:
            print(
                "The use of slack logging requires the user to set a user specific slack legacy token to the SLACK_TOKEN environment variable. Set this variable by 'export SLACK_TOKEN=your_token'. To generate your token please visit https://api.slack.com/custom-integrations/legacy-tokens."
            )
            exit(-1)
        self.slack = Slacker(self.token)
        # Check for success
        try:
            auth = self.slack.auth.test().body
        except Exception:
            print(
                "Slack connection failed. Please compare your provided slack token exported in the SLACK_TOKEN environment variable with your online token at https://api.slack.com/custom-integrations/legacy-tokens. A different token can be set up by 'export SLACK_TOKEN=your_token'."
            )
            exit(-1)
        self.own_id = auth["user_id"]
        self.error_occured = False
        self.names = ""

    def log_handler(self, msg):
        if "name" in msg and "level" in msg and msg["level"] == "job_info":
            self.names += msg['name']
        if msg["level"] == "error" and not self.error_occured:
            self.slack.chat.post_message(
                self.own_id, text="At least one error occured in " + self.names, username="snakemake_"+self.hostname
            )
            self.error_occured = True
        if msg["level"] == "progress" and msg["done"] == msg["total"]:
            # workflow finished
            self.slack.chat.post_message(
                self.own_id, text="Workflow " + self.names + " complete.", username="snakemake_"+self.hostname
            )

sl = SlackLogger()

def log_handler(msg):
    sl.log_handler(msg)

def main():
    print('no main!')

if __name__ == "__main__":
    main()
