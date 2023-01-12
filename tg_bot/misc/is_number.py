async def is_number(value):
    try:
        return int(value)
    except Exception as ex:
        print(ex)
