import redis
from fastapi import Depends, APIRouter
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse

from ..app.influxdb.influxdb import InfluxDB
from ..dependencies.get_query_dependencies import CommonQuery
from ..dependencies.db_dependencies import create_get_db
from ..function.General_operate import GeneralOperate


class GeneralRouter(GeneralOperate):
    def __init__(self, module, redis_db: redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker, is_initial=False):
        self.db_session = db_session
        self.is_initial = is_initial
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas
        router = APIRouter(
            prefix=f"/{self.module.name}/table",
            tags=[f"{self.module.name}_table_crud"],
            dependencies=[]
        )

        @router.on_event("startup")
        async def task_startup_event():
            if self.is_initial:
                db = self.db_session()
                GeneralOperate.initial_redis_data(self, db)
                db.close()

        @router.get("/", response_model=list[self.module.main_schemas])
        async def sql_read_all(db: Session = Depends(create_get_db(self.db_session))):
            return JSONResponse(content=GeneralOperate.read_all_data_from_sql(self, db))

        @router.get("/{table_id}", response_model=self.main_schemas)
        async def sql_read(table_id: int, db: Session = Depends(create_get_db(self.db_session))):
            return JSONResponse(content=GeneralOperate.read_data_from_sql_by_id_set(self, db, {table_id})[0])

        @router.get("/multiple/", response_model=list[self.main_schemas])
        async def get_multiple(common: CommonQuery = Depends(),
                               db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                return JSONResponse(content=GeneralOperate.read_all_data_from_redis(self)[common.skip:][:common.limit])
            else:
                id_set = GeneralOperate.execute_sql_where_command(self, db, common.where_command)
                return JSONResponse(
                    content=GeneralOperate.read_from_redis_by_key_set(self, id_set)[common.skip:][:common.limit])

        @router.get("/{table_id}", response_model=self.main_schemas)
        async def get_by_id(table_id):
            return JSONResponse(content=GeneralOperate.read_from_redis_by_key_set(self, {table_id})[0])

        @router.get("/table_count/")
        async def get_table_count():
            return JSONResponse(content=GeneralOperate.read_table_count(self))

        @router.post("/", response_model=self.main_schemas)
        async def create(create_data: create_schemas,
                         db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=GeneralOperate.create_data(self, db, [create_data])[0])

        @router.post("/multiple/", response_model=list[self.main_schemas])
        async def create_multiple(
                create_data_list: list[create_schemas],
                db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=GeneralOperate.create_data(self, db, create_data_list))

        @router.patch("/{table_id}", response_model=self.main_schemas)
        async def update(update_data: update_schemas,
                         table_id: int, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                update_list = [GeneralOperate.add_id_in_update_data(self, update_data, table_id)]
                return JSONResponse(content=GeneralOperate.update_data(self, db, update_list)[0])

        @router.patch("/multiple/", response_model=list[self.main_schemas])
        async def update_multiple(
                update_list: list[multiple_update_schemas],
                db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=GeneralOperate.update_data(self, db, update_list))

        @router.delete("/{table_id}")
        async def delete(table_id: int, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=GeneralOperate.delete_data(self, db, {table_id}))

        @router.delete("/multiple/")
        async def delete_multiple(id_set: set[int], db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=GeneralOperate.delete_data(self, db, id_set))

        @router.get("/reload_table/")
        async def reload_table(db: Session = Depends(create_get_db(self.db_session))):
            GeneralOperate.initial_redis_data(self, db)
            return JSONResponse(content="ok")

        return router
