from typing import Dict
from typing import List

import yaml
from openai_redis_vectorstore.base import RedisVectorStore

from django.db import models
from django.db import transaction
from django.utils.safestring import mark_safe


class WithVectorStoreIndex(models.Model):
    no_update_vectorstore_index_flag_key = (
        "_with_vectorstore_index_no_update_vectorstore_index_flag"
    )
    # 是否自动索引，即每次在记录保存时进行索引
    # 默认：启用自动索引
    enable_auto_do_vectorstore_index = True

    vectorstore_updated = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="已更新向量数据库",
        help_text="None：表示待处理。<br />True：表示索引成功。<br />False：表示索引失败。",
    )
    vectorstore_uids_data = models.TextField(
        null=True,
        blank=True,
        verbose_name="向量数据库记录编号",
        help_text=mark_safe(
            "添加至向量数据库后返回的编号。用于后续向量数据库的数据维护。"
        ),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if self.enable_auto_do_vectorstore_index and (
            not self.is_no_update_vectorstore_index_flag_marked()
        ):
            transaction.on_commit(self.update_vectorstore_index)
        return result

    def is_no_update_vectorstore_index_flag_marked(self):
        return getattr(self, self.no_update_vectorstore_index_flag_key, False)

    def mark_no_update_vectorstore_index_flag(self):
        setattr(self, self.no_update_vectorstore_index_flag_key, True)

    def update_vectorstore_index(self, save=True):
        # 对象已经触发了索引，则不能再次触发。
        # 需要重新从数据库查询生成新的实例才能再次触发索引。
        self.mark_no_update_vectorstore_index_flag()
        if self.get_enable_vectorstore_index_flag():
            self.upsert_index(save=False)
        else:
            self.delete_index(save=False)
        self.vectorstore_updated = True
        if save:
            self.save()

    #  vectorstore_uids属性处理
    def get_vectorstore_uids(self):
        if not self.vectorstore_uids_data:
            return []
        else:
            return yaml.safe_load(self.vectorstore_uids_data)

    def set_vectorstore_uids(self, value):
        if not value:
            self.vectorstore_uids_data = None
        else:
            self.vectorstore_uids_data = yaml.safe_dump(value)

    vectorstore_uids = property(get_vectorstore_uids, set_vectorstore_uids)

    def get_enable_vectorstore_index_flag(self) -> bool:
        """判断是否需要创建索引"""
        # 一般来说数据记录中应该有enabled或deleted等字段
        # 表示是否启用索引
        raise NotImplementedError()

    def get_vectorstore_index_names(self) -> List[str]:
        # 如果有多个index_name表示：
        # 本数据记录需要在多个向量数据库中建立索引
        raise NotImplementedError()

    def get_vectorstore_index_contents(self) -> List[str]:
        # 向量数据库有索引长度的限制
        # 所以一般文档内容需要分片后进行索引
        # 这里返回分片列表
        raise NotImplementedError()

    def get_vectorstore_index_metas(self, contents=None) -> List[Dict[str, str]]:
        if contents is None:
            contents = self.get_vectorstore_index_contents()
        meta = self.get_vectorstore_index_meta()
        return [meta] * len(contents)

    def get_vectorstore_index_meta(self) -> Dict[str, str]:
        return {
            "app_label": self._meta.app_label,
            "model_name": self._meta.model_name,
            "id": self.id,
        }

    def delete_index(self, save=False):
        if self.vectorstore_uids:
            vs = RedisVectorStore()
            vs.delete_many(self.vectorstore_uids)
            self.vectorstore_uids = None
            if save:
                self.save()

    def upsert_index(self, save=False):
        vs = RedisVectorStore()
        texts = self.get_vectorstore_index_contents()
        metas = self.get_vectorstore_index_metas()
        # 先删除
        self.delete_index(save=False)
        # 后添加
        uids = []
        index_names = self.get_vectorstore_index_names()
        if isinstance(index_names, str):
            index_names = [index_names]
        for index_name in index_names:
            uids += vs.insert_many(
                texts=texts,
                metas=metas,
                index_name=index_name,
            )
        # 更新数据库记录
        self.vectorstore_uids = uids
        if save:
            self.save()
