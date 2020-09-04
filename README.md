# optimistic-locking-example

Proof of concept to implement database concurrency control with optimistic locking.

There are 2 branches `master` and `optimistic-locking`.
To see the faulty implementation you can run against `master` that has race condition issue and
the proper implementation is in `optimistic-locking` branch.

#### Prerequisite:

- postgresql
- python >= 3.6

#### Setup and run the project:
In case you need to update your database user and pasword, you can adjust it on `src/config/database.py`
then run following commands.
```bash
# setup
$ psql -U postgres
$ CREATE DATABASE db_promotions;
$ pip install -r requirements.txt

# run project
$ cd src
$ uvicorn main:app --workers 4 # it depends on your total CPU
```

#### Simulate concurrent request:
```bash
 # initial voucher data
$ curl -X POST http://127.0.0.1:8000/api/vouchers/ -H 'Content-Type: application/json' -d '{"promo_code": "HEMAT17", "quota": 50}'

# perform load test
$ locust # then you can use the interactive mode on http://0.0.0.0:8089
```