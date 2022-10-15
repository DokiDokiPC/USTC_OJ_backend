def get_some_rows(ORM_Object_name,row_list,offset,limit):
    rows=ORM_Object_name.query.with_entities(*row_list).offset(offset).limit(limit).all()
    info=[tuple(row) for row in rows]
    return info
    