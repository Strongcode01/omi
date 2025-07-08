import requests
from django.conf import settings

class Paystack:
    VERIFY_URL = "https://api.paystack.co/transaction/verify/{ref}"

    def verify_payment(self, ref):
        url  = self.VERIFY_URL.format(ref=ref)
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type":  "application/json",
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and r.json()['status']:
            data = r.json()['data']
            # amount returned is in kobo
            return True, data
        return False, {}
