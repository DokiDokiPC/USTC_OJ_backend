def get_some_rows(orm_object_name, row_list, offset, limit):
    rows = orm_object_name.query.with_entities(*row_list).offset(offset).limit(limit).all()
    info = [tuple(row) for row in rows]
    return info
