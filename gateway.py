from fastapi import FastAPI
from mongo_app.database import MongoDatabase


def gateway(app: FastAPI, db: MongoDatabase):
    @app.post(Routes.ASSET, response_model=schemas.AssetMetaDataResponseModel)
    async def upload_asset(
            file: UploadFile,
            user_id=Depends(auth_handler.auth_wrapper),
    ) -> schemas.AssetMetaDataResponseModel:
        return await file_manager_modules.upload_asset_module(
            file=file,
            user_id=user_id,
            db=db,
        )