import smtplib, asyncio, requests
from concurrent.futures import ThreadPoolExecutor

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from model import Gateway

# ---- Prod Setting. ----
SMTP_SERVER = '142.101.194.230'
SMTP_PORT = '25'
REPORT_RECEIPTS = ['noccgi.si@cgi.com', 'repotnp.gto@cgi.com']
# -----------------------

# ---- Dev Setting. ----
# SMTP_SERVER = 'mailhog'
# SMTP_PORT = '1025'
# REPORT_RECEIPTS = ['vincent.corriveau@cgi.com']
# ----------------------

GATEWAYS = [
    Gateway('CONNECT', 'MTL', '10.255.250.17'),
    Gateway('CONNECT', 'MTL', '10.255.250.27'),
    Gateway('CONNECT', 'TOR', '10.253.250.96'),
    Gateway('CONNECT', 'TOR', '10.253.250.97'),
    Gateway('CONNECT', 'PHX', '10.254.239.150'),
    Gateway('CONNECT', 'PHX', '10.254.239.151'),
    Gateway('RNAS', 'MTL', '10.255.251.95'),
    Gateway('RNAS', 'MTL', '10.255.251.96'),
    Gateway('RNAS', 'TOR', '10.253.250.180'),
    Gateway('RNAS', 'TOR', '10.253.250.181'),
    Gateway('RNAS', 'PHX', '10.254.239.155'),
    Gateway('RNAS', 'PHX', '10.254.239.156'),
    Gateway('BELL-PAAS', 'MTL', '10.255.251.97'),
    Gateway('BELL-PAAS', 'MTL', '10.255.251.98'),
    Gateway('BELL-PAAS', 'TOR', '10.253.250.139'),
    Gateway('BELL-PAAS', 'TOR', '10.253.250.140'),
    Gateway('LITE', 'MTL', '10.255.251.56'),
    Gateway('LITE', 'MTL', '10.255.251.57'),
    Gateway('LITE', 'STO', '10.254.239.2'),
    Gateway('LITE', 'STO', '10.254.239.6')
]


def send_report(data: str):
    body = "Hi,\n\nPlease find below the latest statistics for Unified Access. The numbers represent the number of people connected.\n\n" + data

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Unified Access - Statistics"
    msg['From'] = "CGI GTO NOC <noccgi.si@cgi.com>"
    msg['To'] = "repotnp.gto@cgi.com"
    msg['Cc'] = "noccgi.si@cgi.com"
    msg.attach(MIMEText(body, 'plain'))

    smtp = smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT)
    smtp.sendmail("noccgi.si@cgi.com", REPORT_RECEIPTS, msg.as_string())
    smtp.quit()


def fetch_gateway_session_count(gateway: Gateway):
    """Fetch the gateway session usage"""
    if gateway.is_primary:
        if gateway.type == 'RNAS' and gateway.location in ['MTL', 'TOR']:
            csp_session_counts = 0
            session_counts = 0
            for vsrv_name, count in gateway.detailed_session_count.items():
                if 'csp' in vsrv_name.lower():
                    csp_session_counts += int(count)
                else:
                    session_counts += int(count)

            # specific line for RNAS type gateways
            csp_wrapup = f'{gateway.parent} {gateway.type} {gateway.location} (CSP) : {csp_session_counts}'
            all_others_wrapup = f'{gateway.parent} {gateway.type} {gateway.location} : {session_counts}'
            return f'{all_others_wrapup}\n{csp_wrapup}'

        # default line
        return f'{gateway.parent} {gateway.type} {gateway.location} : {gateway.current_session_count}'


async def fetch_gateway_data():
    """Generate a Threat per gateway to run various tasks on each of them at the same time"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, fetch_gateway_session_count, g)
            for g in GATEWAYS
        ]
        for response in await asyncio.gather(*tasks):
            # not storing response if they are NoneType
            if response is not None:
                success_logs.append(response)


if __name__ == "__main__":
    success_logs = []
    exception_logs = []

    # get a async loop to run tasks
    loop = asyncio.get_event_loop()
    fetching_data = asyncio.ensure_future(fetch_gateway_data())
    loop.run_until_complete(fetching_data)

    # bridge both result list into a single string with prompt return between each
    data_as_string = '\n'.join(success_logs) + '\n' + '\n'.join(exception_logs)
    send_report(data_as_string)
