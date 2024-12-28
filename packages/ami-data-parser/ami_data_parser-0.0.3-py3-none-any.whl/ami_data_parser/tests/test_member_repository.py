from unittest import TestCase
from ami_data_parser.entities.member import Member
from ami_data_parser.factories.member_factory import get_members
from ami_data_parser.repositories.member_repository import MemberRepository


class MemberRepositoryTestCase(TestCase):

    def test_member_repository_set(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        repository = MemberRepository()
        member = Member(**received_data)
        repository.set(member)
        self.assertEqual(member, repository._objects.get('SIP/IP1489'))
    
    def test_member_repository_set_exception(self):
        repository = MemberRepository()
        self.assertRaises(
            ValueError,
            repository.set,
            {'name': 'teste'}
        )
    
    def test_member_repository_get(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        repository = MemberRepository()
        member = Member(**received_data)
        repository.set(member)
        self.assertEqual(member, repository.get('SIP/IP1489'))

    def test_member_repository_get_exception(self):
        repository = MemberRepository()
        self.assertRaises(
            Member.DoesExists,
            repository.get,
            'SIP/IP-100'
        )
    
    def test_member_repository_exists(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        repository = MemberRepository()
        self.assertFalse(repository.exists('SIP/IP1489'))
        member = Member(**received_data)
        repository.set(member)
        self.assertTrue(repository.exists('SIP/IP1489'))
    
    def test_member_repository_delete(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        repository = MemberRepository()
        member = Member(**received_data)
        repository.set(member)
        repository.delete('SIP/IP1489')
        self.assertFalse(repository.exists('SIP/IP1489'))
    
    def test_member_repository_equal(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        member = Member(**received_data)
        repository1 = MemberRepository()
        repository2 = MemberRepository()
        repository1.set(member)
        repository2.set(member)
        self.assertTrue(repository1 == repository2)
    
    def test_member_repository_not_equal(self):
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': False,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        member1 = Member(**received_data)
        received_data = {
            'name': 'SIP/IP1489',
            'has_paused': True,
            'paused_time': 0,
            'logged_time': 0,
            'total_calls': 3,
            'last_call_time': 1912
        }
        member2 = Member(**received_data)
        repository1 = MemberRepository()
        repository2 = MemberRepository()
        repository1.set(member1)
        repository2.set(member2)
        self.assertFalse(repository1 == repository2)
    
    def test_member_repository_diff(self):
        repository = MemberRepository()
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
        members = get_members(received_data)
        repository.set(members)
        self.assertListEqual(repository.diff(), [('SIP/IP1489', 'added'), ('SIP/IP1490', 'added')])
        self.assertListEqual(repository.diff(), [])
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
                'has_paused': True,
                'paused_time': 0,
                'logged_time': 0,
                'total_calls': 1,
                'last_call_time': 1218
            }
        ]
        members = get_members(received_data)
        repository.set(members)
        self.assertListEqual(repository.diff(), [('SIP/IP1490', 'changed')])