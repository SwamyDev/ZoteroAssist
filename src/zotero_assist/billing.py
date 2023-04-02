import os
from dataclasses import dataclass
from datetime import date

import requests
from dateutil.relativedelta import relativedelta


@dataclass
class BillingInfo:
    limit_usd: float
    total_usage_usd: float
    today_usage_usd: float


def query_billing_info() -> BillingInfo:
    open_ai_headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "OpenAI-Organization": f"{os.getenv('OPENAI_ORG_ID')}",
    }
    billing_url = "https://api.openai.com/dashboard/billing"
    billing_sub = requests.get(f"{billing_url}/subscription", headers=open_ai_headers).json()
    today = date.today()
    tomorrow = today + relativedelta(days=1)
    previous = today - relativedelta(days=90)
    billing_total = requests.get(
        f"{billing_url}/usage?end_date={tomorrow.strftime('%Y-%m-%d')}&start_date={previous.strftime('%Y-%m-%d')}",
        headers=open_ai_headers).json()
    billing_today = requests.get(
        f"{billing_url}/usage?end_date={tomorrow.strftime('%Y-%m-%d')}&start_date={today.strftime('%Y-%m-%d')}",
        headers=open_ai_headers).json()

    return BillingInfo(billing_sub['hard_limit_usd'],
                       billing_total['total_usage'] / 100.0,
                       billing_today['total_usage'] / 100.0)
