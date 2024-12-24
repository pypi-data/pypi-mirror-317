import os
import logging
from datetime import datetime
from peewee import SqliteDatabase, Model, DateTimeField, AutoField, CharField, TextField

from utils_hj3415 import helpers
peewee_logger = helpers.setup_logger('peewee_logger', logging.WARNING)

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.db')
log_db = SqliteDatabase(LOG_PATH)


class LogBase(Model):
    id = AutoField(primary_key=True)
    timestamp = DateTimeField(default=datetime.now())
    level = CharField(max_length=10, default='INFO')  # 예: 'INFO', 'ERROR'
    message = TextField()

    class Meta:
        database = log_db


class Dart(LogBase):
    pass

class Mongo(LogBase):
    pass

class Cli(LogBase):
    pass


class LogManager:
    """
    로그 레코드 관리 클래스.
    """

    def __init__(self, table: str):
        """
        table - dart, mongo, cli
        """
        if table == 'dart':
            self.table = Dart
        elif table == 'mongo':
            self.table = Mongo
        elif table == 'cli':
            self.table = Cli
        else:
            raise Exception(f"table setting error: {table}")
        self.db = log_db
        self._initialize_db()

    def _initialize_db(self):
        """데이터베이스와 테이블 초기화."""
        self.db.connect(reuse_if_open=True)
        self.db.create_tables([self.table], safe=True)
        peewee_logger.info("데이터베이스 초기화 완료")

    def save(self, level, message):
        """새로운 로그 레코드 생성."""
        record = self.table.create(level=level, message=message)
        peewee_logger.info(f"레코드 생성: ID={record.id}, LEVEL={record.level}, MSG={record.message}")
        return record

    def get_all(self):
        """모든 레코드 조회."""
        all_records = self.table.select()
        peewee_logger.info("모든 레코드 조회:")
        for r in all_records:
            peewee_logger.info(f"ID={r.id}, TIME={r.timestamp}, LEVEL={r.level}, MSG={r.message}")
        return list(all_records)

    def update(self, record_id, new_level=None, new_message=None):
        """특정 레코드 업데이트."""
        query = self.table.update(
            level=new_level if new_level else self.table.level,
            message=new_message if new_message else self.table.message
        ).where(self.table.id == record_id)

        updated_count = query.execute()
        if updated_count > 0:
            peewee_logger.info(f"ID={record_id} 레코드 업데이트 성공")
        else:
            peewee_logger.info(f"ID={record_id} 레코드 업데이트 실패(존재하지 않음)")

    def delete(self, record_id):
        """특정 레코드 삭제."""
        deleted_count = self.table.delete().where(self.table.id == record_id).execute()
        if deleted_count > 0:
            peewee_logger.info(f"ID={record_id} 레코드 삭제 성공")
        else:
            peewee_logger.info(f"ID={record_id} 레코드 삭제 실패(존재하지 않음)")

    def reset(self):
        # 모든 레코드 삭제
        query = self.table.delete()
        deleted_count = query.execute()  # 삭제된 레코드 수 반환
        print(f"삭제된 레코드 수: {deleted_count}")

    def close(self):
        """데이터베이스 연결 종료."""
        if not self.db.is_closed():
            self.db.close()
            peewee_logger.info("데이터베이스 연결 종료")

