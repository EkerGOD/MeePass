import os.path
import random
from unittest import TestCase

import pyotp

import config
from auth import authenticate_otp, authenticate_master_password


class TestAuth(TestCase):
    def setUp(self):
        self.db_name = 'test.db'
        self.db_path = os.path.join(config.TEST_DB_FOLDER_PATH, self.db_name)
        self.correct_master_password = 'qwer1234'
        self.incorrect_master_password = '123456'

    def test_authenticate_otp(self):
        correct_otp = pyotp.TOTP('UTTRDZ24BMUML5VXIAUNXDFRCKB4OXA6').now()
        incorrect_otp = str(random.randint(100000,999999))
        correct_response = authenticate_otp(correct_otp)
        incorrect_response = authenticate_otp(incorrect_otp)
        print(correct_response)
        print(incorrect_response)
        self.assertEqual(correct_response['data']['is_otp_correct'], True)
        self.assertEqual(incorrect_response['data']['is_otp_correct'], False)
        # if not totp.verify(otp):

    def test_authenticate_master_password(self):
        authenticate_master_password(self.db_path, self.correct_master_password)
        authenticate_master_password(self.db_path, self.incorrect_master_password)