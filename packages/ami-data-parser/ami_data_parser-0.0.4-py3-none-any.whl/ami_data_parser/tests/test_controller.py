from unittest import TestCase
from ami_data_parser.controller import Controller
from ami_data_parser.entities.peer import Peer
from ami_data_parser.entities.queue import Queue


class ControllerTestCase(TestCase):

    def test_peer_update(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: 104@BLF_3           : SIP/IP-104-7QmO5      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 2 hints registered\r\n']
        expected_data = [{'exten': '104', 'peername': 'SIP/IP-104-IJ8vP', 'state': 'Unavailable', 'presence': 'not_set', 'watchers': 0, 'type': 'peer', 'event': 'added'}, {'exten': '104', 'peername': 'SIP/IP-104-7QmO5', 'state': 'Unavailable', 'presence': 'not_set', 'watchers': 0, 'type': 'peer', 'event': 'added'}]
        controller = Controller()
        peers = controller.peer_update(received_data)
        self.assertListEqual(peers, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: 104@BLF_3           : SIP/IP-104-7QmO5      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 2 hints registered\r\n']
        expected_data = []
        peers = controller.peer_update(received_data)
        self.assertListEqual(peers, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Idle     Presence:not_set         Watchers  0\r\n', 'Output: 104@BLF_3           : SIP/IP-104-7QmO5      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 2 hints registered\r\n']
        expected_data = [{'exten': '104', 'peername': 'SIP/IP-104-IJ8vP', 'state': 'Idle', 'presence': 'not_set', 'watchers': 0, 'type': 'peer', 'event': 'changed'}]
        peers = controller.peer_update(received_data)
        self.assertListEqual(peers, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Idle     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 1 hints registered\r\n']
        expected_data = [{'peername': 'SIP/IP-104-7QmO5', 'type': 'peer', 'event': 'removed'}]
        peers = controller.peer_update(received_data)
        self.assertEqual(peers, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Inuse     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 1 hints registered\r\n']
        expected_data = [{'exten': '104', 'peername': 'SIP/IP-104-IJ8vP', 'state': 'Inuse', 'presence': 'not_set', 'watchers': 0, 'type': 'peer', 'event': 'changed'}]
        peers = controller.peer_update(received_data)
        self.assertEqual(peers, expected_data)

    def test_queue_update(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2930362 secs ago) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']
        expected_data = [{'queuename': 'Queue_11', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0, 'members': [{'name': 'SIP/IP-100-CdFaT', 'has_paused': True, 'paused_time': 2930362, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0, 'type': 'member'}, {'name': 'SIP/IP-101', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0, 'type': 'member'}], 'waiting_calls': [], 'type': 'queue', 'event': 'added'}, {'queuename': 'Queue_27', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0, 'members': [], 'waiting_calls': [], 'type': 'queue', 'event': 'added'}, {'queuename': 'Queue_44', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0, 'members': [{'name': 'SIP/IP-100-boazN', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0, 'type': 'member'}, {'name': 'SIP/IP-101-Iathq', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0, 'type': 'member'}], 'waiting_calls': [], 'type': 'queue', 'event': 'added'}, {'queuename': 'Queue_47', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0, 'members': [], 'waiting_calls': [], 'type': 'queue', 'event': 'added'}]
        controller = Controller()
        queues = controller.queue_update(received_data)
        self.assertListEqual(queues, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']        
        expected_data = [{'queuename': 'Queue_11', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0, 'members': [{'name': 'SIP/IP-101', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0, 'type': 'member'}], 'waiting_calls': [], 'type': 'queue', 'event': 'changed'}]
        queues = controller.queue_update(received_data)
        self.assertListEqual(queues, expected_data)
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']        
        expected_data = [{'queuename': 'Queue_11', 'type': 'queue', 'event': 'removed'}]
        queues = controller.queue_update(received_data)
        self.assertListEqual(queues, expected_data)

    def test_get_peer(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000003\r\n', 'Message: Command output follows\r\n', 'Output: \r\n', 'Output:     -= Registered Asterisk Dial Plan Hints =-\r\n', 'Output: 104@BLF_1           : SIP/IP-104-IJ8vP      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: 104@BLF_3           : SIP/IP-104-7QmO5      State:Unavailable     Presence:not_set         Watchers  0\r\n', 'Output: ----------------\r\n', 'Output: - 2 hints registered\r\n']
        controller = Controller()
        controller.peer_update(received_data)
        peer = controller.get('SIP/IP-104-IJ8vP', 'peer')
        self.assertEqual(peer.peername, 'SIP/IP-104-IJ8vP')
    
    def test_get_queue(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2930362 secs ago) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']
        controller = Controller()
        controller.queue_update(received_data)
        queue = controller.get('Queue_11', 'queue')
        self.assertEqual(queue.queuename, 'Queue_11')
    
    def test_get_invalid_type(self):
        controller = Controller()
        self.assertRaises(
            TypeError,
            controller.get,
            'Queue_11', 
            'queue1'
        )
    
    def test_get_peer_not_exists(self):
        controller = Controller()
        self.assertRaises(
            Peer.DoesExists,
            controller.get,
            'SIP/IP-104-IJ8vP', 
            'peer'
        )
    
    def test_get_queue_not_exists(self):
        controller = Controller()
        self.assertRaises(
            Queue.DoesExists,
            controller.get,
            'Queue_11', 
            'queue'
        )