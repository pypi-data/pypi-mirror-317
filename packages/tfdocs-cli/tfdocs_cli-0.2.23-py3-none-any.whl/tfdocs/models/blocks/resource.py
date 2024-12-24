from tfdocs.models.block import Block


class Resource(Block):

    @classmethod
    def from_name(cls, name: str) -> "Resource":
        res = cls._db.sql(
            """
            SELECT block_id, block_name FROM block 
            WHERE block_type == 'Resource' 
            AND block_name == ?;                    
         """,
            (name,),
        ).fetchone()
        r = Resource(type="Resource", hash=res[0], name=res[1])
        return r
