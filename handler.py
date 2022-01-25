import os
import re
import json
import subprocess
import logging
import urllib.request


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

soracom_auth_key_id = os.getenv('SORACOM_AUTH_KEY_ID')
soracom_auth_key = os.getenv('SORACOM_AUTH_KEY')
soracom_sim_id = os.getenv('SIM_ID')
slack_url = os.getenv('SLACK_URL')

# SORACOM API
soracom_common_arg = ' --auth-key-id ' + \
    soracom_auth_key_id + ' --auth-key ' + soracom_auth_key


def lambda_handler(event, context):
    soracom_cli_ping = "soracom sims downlink-ping " \
        + "--sim-id " + soracom_sim_id \
        + " --number-of-ping-requests 5 --timeout-seconds 3" \
        + soracom_common_arg

    cli_output = subprocess.run(
        soracom_cli_ping, shell=True, capture_output=True)

    if cli_output.returncode != 0:
        send_alert_to_slack((cli_output).stderr.decode())
        return

    cli_output_json = json.loads((cli_output).stdout.decode())
    ping_result = cli_output_json.get("success")
    ping_stat = cli_output_json.get("stat")

    if ping_result is False:
        send_alert_to_slack(ping_stat)
        return

    p = r'\s([0-9]+)%'
    r = re.findall(p, ping_stat)
    ping_loss_rate = int(r[0])

    if ping_loss_rate > 50:
        send_alert_to_slack(ping_stat)
    else:
        logger.info(ping_stat)

    return


def send_alert_to_slack(message):
    # NOTE: If you don't need to send alert to Slack, you can modify this function.
    message = "Ping to SIM ID " + soracom_sim_id + " got error: " + message
    send_data = {
        "text": message,
    }
    send_text = json.dumps(send_data)
    request = urllib.request.Request(
        slack_url,
        data=send_text.encode('utf-8'),
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        logger.info(response_body)


# if __name__ == '__main__':
#     lambda_handler()
