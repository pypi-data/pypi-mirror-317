from tfdocs.models.block import Block


class DataSource(Block):

    @classmethod
    def from_name(cls, name: str) -> "DataSource":
        res = cls._db.sql(
            """
            SELECT block_id, block_name FROM block 
            WHERE block_type == 'DataSource' 
            AND block_name == ?;                    
         """,
            (name,),
        ).fetchone()
        r = DataSource(type="DataSource", hash=res[0], name=res[1])
        return r
