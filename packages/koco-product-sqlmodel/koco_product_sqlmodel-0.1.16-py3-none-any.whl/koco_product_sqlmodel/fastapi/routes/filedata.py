from fastapi import APIRouter, Depends, HTTPException, Request

import koco_product_sqlmodel.fastapi.routes.security as sec
import koco_product_sqlmodel.dbmodels.definition as sqlm
import koco_product_sqlmodel.mdb_connect.filedata as mdb_file
import koco_product_sqlmodel.mdb_connect.generic_object_connect as mdb_gen
import koco_product_sqlmodel.mdb_connect.changelog as mdb_change

router = APIRouter(
    dependencies=[Depends(sec.get_current_active_user)],
    tags=["Endpoints to FILE-data"],
)


@router.get("/")
def get_files(
    entity_id: int = None, entity_type: str = None
) -> list[sqlm.CFileDataGet]:
    files: list[sqlm.CFileData] = mdb_file.get_files_db(
        entity_id=entity_id, entity_type=entity_type
    )
    files_get = []
    for f in files:
        files_get.append(sqlm.CFileDataGet(**f.model_dump()))
    return files_get


@router.get("/{id}/")
def get_file_by_id(id) -> sqlm.CFileDataGet:
    file = mdb_file.get_file_db_by_id(id)
    if file != None:
        return sqlm.CFileDataGet(**file.model_dump())
    return None


@router.post("/", dependencies=[Depends(sec.has_post_rights)])
async def create_filedata(
    filedata: sqlm.CFileDataPost, request: Request
) -> sqlm.CFileDataGet:
    filedata.user_id = await sec.get_user_id_from_request(request=request)
    new_filedata = mdb_file.create_filedata(sqlm.CFileData(**filedata.model_dump()))
    return await get_and_log_updated_model(request=request, updated_object=new_filedata)


@router.patch(
    "/{id}/",
    dependencies=[
        Depends(sec.has_post_rights),
    ],
)
async def update_catalog(
    id: int, filedata: sqlm.CFileDataPost, request: Request
) -> sqlm.CFileDataGet:
    filedata.user_id = await sec.get_user_id_from_request(request=request)
    updated_filedata = mdb_file.update_filedata(id=id, filedata=filedata)
    if updated_filedata == None:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return await get_and_log_updated_model(
        request=request, updated_object=updated_filedata
    )


async def get_and_log_updated_model(
    request: Request, updated_object: sqlm.CFileData
) -> sqlm.CFileData:
    user_id = await sec.get_user_id_from_request(request=request)
    entity_type = "cfiledata"
    result = sqlm.CFileDataGet(**updated_object.model_dump())
    mdb_change.log_results_to_db(
        entity_id=result.id,
        entity_type=entity_type,
        action=request.method,
        user_id=user_id,
        new_values=str(result.model_dump_json(exclude=("insdate", "upddate"))),
    )
    return result


@router.delete("/{id}/", dependencies=[Depends(sec.has_post_rights)])
async def delete_fildata_by_id(id: int, request: Request = None) -> dict[str, bool]:
    """
    Delete an object item by cobject.id.
    """
    res = mdb_gen.delete_object(db_obj_type=sqlm.CFileData, id=id)
    if res == None:
        raise HTTPException(status_code=404, detail="Object not found")
    user_id = await sec.get_user_id_from_request(request=request)
    mdb_change.log_results_to_db(
        entity_type="cfiledata",
        entity_id=id,
        action="DELETE",
        user_id=user_id,
        new_values=None,
    )
    return {"ok": True}


# "33d01ba467678caacc835c91fdfc6d91a15961bc37919396b444ebd38227c318"


def main():
    pass


if __name__ == "__main__":
    main()
