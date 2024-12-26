import traceback
from datetime import datetime

from funutil import getLogger
from sqlalchemy import String, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

logger = getLogger("fundb")


class BaseTable(DeclarativeBase):
    uid: Mapped[str] = mapped_column(String(128), comment="唯一ID", unique=True)

    gmt_modified: Mapped[datetime] = mapped_column(
        comment="修改时间", default=datetime.now, onupdate=datetime.now
    )

    gmt_create: Mapped[datetime] = mapped_column(
        comment="创建时间", default=datetime.now
    )
    id: Mapped[int] = mapped_column(
        primary_key=True, comment="主键", autoincrement=True
    )

    @property
    def get_uid(self):
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    def _to_dict(self) -> dict:
        res = self.to_dict()
        res.update(
            {
                # "id": self.id,
                # "gmt_create": self.gmt_create,
                # "gmt_update": self.gmt_update,
                "uid": self.uid,
            }
        )
        for key in list(res.keys()):
            if res[key] is None:
                res.pop(key)
        return res

    def child(self):
        return BaseTable

    def exists(self, session: Session):
        sql = select(self.child()).where(self.child().uid == self.uid)
        return session.execute(sql).first() is not None

    def upsert(self, session: Session, update_data=False):
        try:
            if not self.exists(session):
                logger.debug(f"uid={self.uid} not exists, insert it.")
                session.execute(insert(self.child()).values(**self._to_dict()))
            elif update_data:
                logger.debug(f"uid={self.uid} exists, update it.")
                session.execute(
                    update(self.child())
                    .where(self.child().uid == self.uid)
                    .values(**self._to_dict())
                )
        except Exception as e:
            logger.error(f"upsert error: {e}:{traceback.format_exc()}")
