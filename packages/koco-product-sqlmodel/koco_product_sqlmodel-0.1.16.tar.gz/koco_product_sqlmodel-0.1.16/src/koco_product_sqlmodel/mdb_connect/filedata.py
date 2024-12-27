from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select
from koco_product_sqlmodel.dbmodels.definition import (
    CFileData,
    CFileDataGet,
    CFileDataPost,
)


def create_filedata(filedata: CFileData):
    with Session(mdb_engine) as session:
        session.add(filedata)
        session.commit()
        statement = select(CFileData).where(
            CFileData.blake2shash == filedata.blake2shash
        )
    return session.exec(statement=statement).one_or_none()


def update_filedata(id: int | None, filedata: CFileDataPost) -> CFileData | None:
    if id == None:
        return
    with Session(mdb_engine) as session:
        statement = select(CFileData).where(CFileData.id == id)
        fd = session.exec(statement=statement).one_or_none()
        if fd == None:
            return
        fd_data = filedata.model_dump(exclude_unset=True)
        fd = fd.sqlmodel_update(fd_data)
        session.add(fd)
        session.commit()
        session.refresh(fd)
    return fd


def get_files_db(entity_id: int, entity_type: str) -> list[CFileData] | None:
    if entity_id == None and entity_type == None:
        statement = select(CFileData)
    elif entity_id != None and entity_type == None:
        statement = select(CFileData).where(CFileData.entity_id == entity_id)
    elif entity_id == None and entity_type != None:
        statement = select(CFileData).where(CFileData.entity_type == entity_type)
    else:
        statement = (
            select(CFileData)
            .where(CFileData.entity_id == entity_id)
            .where(CFileData.entity_type == entity_type)
        )
    with Session(mdb_engine) as session:
        return session.exec(statement=statement).all()


def get_file_db_by_id(id: int) -> CFileData:
    if not id:
        return
    statement = select(CFileData).where(CFileData.id == id)
    with Session(mdb_engine) as session:
        return session.exec(statement=statement).one_or_none()


# def delete_application_by_id(id: int) -> int | None:
#     statement = select(CApplication).where(CApplication.id == id)
#     with Session(mdb_engine) as session:
#         app = session.exec(statement=statement).one_or_none()
#         if app == None:
#             return
#         session.delete(app)
#         session.commit()
#         return 1


def main() -> None:
    pass


if __name__ == "__main__":
    main()
