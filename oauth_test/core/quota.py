import json
import pytz
import datetime


class QuotaCounter:
    quota_limit = 9500
    _initialised = False
    _quota_available = []
    _cur_day = None

    @staticmethod
    def __initialize_quota():
        if not QuotaCounter._initialised:
            # initialize quota
            with open("client_secret.json") as file:
                strings = file.read().split('\n,\n')
                QuotaCounter._quota_available = [QuotaCounter.quota_limit]*len(strings)
            try:
                with open("quota.data", 'r') as file:
                    content = json.loads(file.read())
                    quotas = content['Quota_available']
                    for i in range(len(quotas)):
                        QuotaCounter._quota_available[i] = int(quotas[i])
                    QuotaCounter._cur_day = datetime.date.fromisoformat(content['Date_in_PST'])
                    if not QuotaCounter._cur_day:
                        QuotaCounter._cur_day = datetime.datetime.now(pytz.timezone('US/Pacific')).date()
                        QuotaCounter._quota_available = [QuotaCounter.quota_limit] * len(QuotaCounter._quota_available)
            except:
                with open("quota.data", 'a+') as file:
                    QuotaCounter._quota_available = [QuotaCounter.quota_limit]*len(QuotaCounter._quota_available)
                    QuotaCounter._cur_day = datetime.datetime.now(pytz.timezone('US/Pacific')).date()
            QuotaCounter._initialised = True

    @staticmethod
    def save_quota():
        if not QuotaCounter._initialised:
            QuotaCounter.__initialize_quota()
        QuotaCounter.check_quota_refresh()
        my_dict = dict()
        my_dict['Date_in_PST'] = QuotaCounter._cur_day.__str__()
        my_dict['Quota_available'] = QuotaCounter._quota_available
        with open("quota.data", 'w') as file:
            file.write(json.dumps(my_dict))

    @staticmethod
    def check_quota_refresh():
        if not QuotaCounter._initialised:
            QuotaCounter.__initialize_quota()
        date_now = datetime.datetime.now(pytz.timezone('US/Pacific')).date()
        if QuotaCounter._cur_day < date_now:
            QuotaCounter._cur_day = date_now
            QuotaCounter._quota_available = [QuotaCounter.quota_limit]*len(QuotaCounter._quota_available)

    @staticmethod
    def get_remaining_quota():
        if not QuotaCounter._initialised:
            QuotaCounter.__initialize_quota()
        QuotaCounter.check_quota_refresh()
        return QuotaCounter._quota_available

    @staticmethod
    def get_quota_of(index):
        if not QuotaCounter._initialised:
            QuotaCounter.__initialize_quota()
        QuotaCounter.check_quota_refresh()
        return QuotaCounter._quota_available[index]

    @staticmethod
    def reduce_quota_of(index, amount):
        if not QuotaCounter._initialised:
            QuotaCounter.__initialize_quota()
        QuotaCounter.check_quota_refresh()
        QuotaCounter._quota_available[index] -= amount

