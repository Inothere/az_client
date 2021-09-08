import sqlalchemy as sa
import typing


class VendorCreator:
    def __init__(self, conn: sa.engine.base.Connection) -> None:
        self._pk = None
        self.conn = conn

    @property
    def vendor_pk(self) -> int:
        if self._pk:
            return self._pk
        r = self.conn.execute("select max(entry) from creature_template;")
        row = r.fetchone()
        self._pk = row[0] + 1
        return self._pk

    def name_exists(self, name: str):
        r = self.conn.execute(
            sa.text("select name from creature_template where name = :name"), name=name
        )
        return bool(r.fetchone())

    def get_item_ids(self, item_list: typing.Set[str]) -> typing.List[int]:
        sql = sa.text(
            """
        select 
        entry, name
        from item_template
        where
        name in :item_list
        """
        )
        r = self.conn.execute(sql, item_list=tuple(item_list))
        rows = r.fetchall()
        fetched_names = {x[1] for x in rows}
        delta = item_list - fetched_names
        if delta:
            raise Exception(f"无法找到items: {delta}")
        return [x[0] for x in rows]

    def create_creature_template(self, name: str) -> int:
        if self.name_exists(name):
            raise Exception(f"{name} 已存在")
        sql = sa.text(
            """
        insert into creature_template
        (
            `entry`, 
            modelid1,
            `name`,
            IconName,
            minlevel,
            maxlevel,
            faction,
            npcflag,
            `type`,
            InhabitType,
            VerifiedBuild,
            scale
        ) values 
        (
            :vendor_pk, -- entry
            16541, -- modelid1
            :name, -- name
            "Buy", -- IconName
            80,  -- minlevel
            80,  -- maxlevel
            2006, -- faction
            128, -- npcflag
            7, -- type
            3, -- InhabitType
            1, -- VerifiedBuild
            2 -- scale, 供应商尺寸应该放大
        )
        """
        )
        self.conn.execute(sql, name=name, vendor_pk=self.vendor_pk)
        return self.vendor_pk

    def delete_creature_template(self, vendor_pk=None):
        entry = vendor_pk or self.vendor_pk
        sql = sa.text("delete from creature_template where entry = :entry")
        self.conn.execute(sql, entry=entry)

    def delete_npc_vendors(self, vendor_pk=None):
        sql = sa.text(
            """
        delete from npc_vendor where `entry` = :vendor_pk
        """
        )
        vendor_pk = vendor_pk or self.vendor_pk
        self.conn.execute(sql, vendor_pk=vendor_pk)

    def insert_npc_vendors(self, item_ids: typing.List[int]):
        sql = sa.text(
            """
        insert into npc_vendor
        (
            `entry`,
            item
        ) values (:entry, :item);
        """
        )
        for item_id in item_ids:
            self.conn.execute(sql, entry=self.vendor_pk, item=item_id)

    def do_create(self, name: str, item_list: typing.Iterable[str]):
        try:
            item_ids = self.get_item_ids(set(item_list))
            self.create_creature_template(name)
            self.delete_npc_vendors()
            self.insert_npc_vendors(item_ids)
        except Exception:
            """
            world db 表都是MyISAM引擎，需要手动回滚
            """
            self.delete_npc_vendors()
            self.delete_creature_template()
            print("Rollback")
            raise

    def do_teardown(self, name: str):
        sql = sa.text("""
        select entry from creature_template where name = :name
        """)
        r = self.conn.execute(sql, name=name).fetchone()
        if not r:
            return
        vendor_pk = r[0]
        self.delete_npc_vendors(vendor_pk)
        self.delete_creature_template(vendor_pk)
