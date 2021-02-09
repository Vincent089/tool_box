from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, select

from common.date_tool import timestamp
from net_tools.gdn_circuit_mapper_v2.classes.device import Device


class DeviceRepository:
    db_file = r"C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_db_repo\devices.db"

    def __init__(self):
        """Create a simple DB called "deviceconfig" using SQLite and SQLAlchemy"""
        self.device_model = self._get_device_model()

    def _get_repo_engine(self):
        return create_engine('sqlite:///%s' % self.db_file, echo=False)

    def _get_device_model(self):
        engine = self._get_repo_engine()
        metadata = MetaData()

        devices = Table('devices', metadata,
                        Column('hostname', String, primary_key=True),
                        Column('ip', String),
                        Column('os', String),
                        Column('config', String),
                        Column('timestamp', DateTime))

        metadata.create_all(engine)

        return devices

    def get_device_by_hostname(self, hostname):
        with self._get_repo_engine().connect() as conn:
            query = select([self.device_model]).where(self.device_model.c.hostname == hostname)
            return conn.execute(query).fetchone()

    def add_device(self, device: Device):
        with self._get_repo_engine().connect() as conn:
            query = self.device_model.insert().values(hostname=device.hostname,
                                                      ip=device.ip,
                                                      os=device.os,
                                                      config=device.config,
                                                      timestamp=timestamp())
            conn.execute(query)
