import unittest

from db_hj3415 import mypeewee


class LogManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_dart = mypeewee.LogManager('dart')

    def setUp(self):
        self.log_dart.save('INFO', '기본 로그1')
        self.log_dart.save('ERROR', '기본 로그2')

    @classmethod
    def tearDownClass(cls):
        cls.log_dart.reset()
        cls.log_dart.close()

    def test_save(self):
        record1 = self.log_dart.save('INFO', '서버 시작')
        record2 = self.log_dart.save('ERROR', 'DB 연결 실패')
        print(record1, record2)

    def test_get_all(self):
        for item in self.log_dart.get_all():
            print(f"ID={item.id}, TIME={item.timestamp}, LEVEL={item.level}, MSG={item.message}")


    def test_update(self):
        all_records = self.log_dart.get_all()
        if all_records:
            first_record_id = all_records[0].id
            self.log_dart.update(first_record_id, new_message='서버 시작 - 정상 작동')

            # READ after UPDATE
        self.log_dart.get_all()

    def test_delete(self):
        all_records = self.log_dart.get_all()
        if len(all_records) > 1:
            second_record_id = all_records[1].id
            self.log_dart.delete(second_record_id)

        # READ after DELETE
        self.log_dart.get_all()