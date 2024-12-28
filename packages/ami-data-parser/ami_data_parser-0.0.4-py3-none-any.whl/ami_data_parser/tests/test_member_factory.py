from unittest import TestCase
from ami_data_parser.factories.member_factory import get_members


class MemberFactoryTestCase(TestCase):

    def test_get_members(self):
        received_data = [
            {
                'name': 'SIP/IP1489',
                'has_paused': True,
                'paused_time': 0,
                'logged_time': 0,
                'total_calls': 3,
                'last_call_time': 1912
            },
            {
                'name': 'SIP/IP1490',
                'has_paused': False,
                'paused_time': 0,
                'logged_time': 0,
                'total_calls': 1,
                'last_call_time': 1218
            }
        ]
        queues = get_members(received_data)
        self.assertEqual(len(queues), 2)