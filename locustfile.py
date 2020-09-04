import random
import string

from locust import HttpUser, task, between, SequentialTaskSet


class UserRedeemTask(SequentialTaskSet):

    def __init__(self, *args, **kwargs):
        super(UserRedeemTask, self).__init__(*args, **kwargs)
        self.email = None
        self.password = 'admin123'

    @staticmethod
    def _generate_random_email():
        letters = string.ascii_lowercase
        result = ''.join(random.choice(letters) for _ in range(10))
        return f'{result}@gmail.com'

    @task
    def register(self):
        self.email = self._generate_random_email()

        self.client.post('/api/users/', json={
            'email': self.email,
            'password': self.password
        })

    @task
    def redeem(self):
        if self.email is not None:
            self.client.post(
                url='/api/vouchers/redeem/',
                json={'promo_code': 'HEMAT17'},
                auth=(self.email, self.password),
            )


class UserRedeem(HttpUser):
    wait_time = between(0, 1)
    tasks = [
        UserRedeemTask
    ]
