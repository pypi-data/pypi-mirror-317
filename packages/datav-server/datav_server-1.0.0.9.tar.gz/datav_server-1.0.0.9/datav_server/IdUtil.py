import uuid


def genUUID():
    return str(uuid.uuid4()).replace("-", "")
