def get_some_rows(orm_object_name, row_name_list, offset, limit):
    row_list = [getattr(orm_object_name, row_name)
                for row_name in row_name_list]
    rows_result = orm_object_name.query.with_entities(
        *row_list).offset(offset).limit(limit).all()
    list_rows = [list(row) for row in rows_result]

    info = [{row_name: row_value for row_name,
             row_value in zip(row_name_list, rows)} for rows in list_rows]
    return info
