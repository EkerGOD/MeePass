import random
from unittest import TestCase

import pyotp

from auth import authenticate_otp


class TestAuth(TestCase):
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