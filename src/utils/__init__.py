from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends , HTTPException , status
from typing import TypeVar , Type , List , Dict
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from src.core.base import get_db

from sqlalchemy import select


ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType" , bound=BaseModel)

def get_base_service(db: AsyncSession = Depends(get_db)):
    return BaseService(db=db)





class BaseService:
    def __init__(self , db:AsyncSession = Depends(get_db)):
        self.db : AsyncSession = db

    async def create(
            self,
            model: Type[ModelType],
            db_obj: SchemaType
        ) -> ModelType:
            try:
                if not isinstance(db_obj, BaseModel):
                    raise ValueError("db_obj must be a Pydantic model")


                new_item = model(**db_obj.model_dump(exclude_unset=True))
                self.db.add(new_item)
                await self.db.commit()
                await self.db.refresh(new_item)
                return new_item

            except ValueError as ve:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Validation error: {str(ve)}"
                )
            
            except SQLAlchemyError as se:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {str(se)}"
                )
            
            except Exception as e:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(e)}"
                )
            
    async def get_by_id(
            self,
            model: Type[ModelType],
            item_id: int,
            user_id: int | None = None,
        ) -> ModelType:
            try:
                if not isinstance(item_id, int) or item_id <= 0:
                    raise ValueError("item_id must be a positive integer")

                stmt = select(model).where(model.id == item_id)
                if user_id is not None:
                    stmt = stmt.where(model.user_id == user_id)
                result = await self.db.execute(stmt)
                item = result.scalars().first()
                if not item:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{model.__name__} with ID {item_id} not found"
                    )

                return item

            except ValueError as ve:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Validation error: {str(ve)}"
                )

            except SQLAlchemyError as se:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {str(se)}"
                )

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(e)}"
                )
            
    async def get_all(
            self,
            model: Type[ModelType],
            user_id: int | None = None,
            limit: int | None = 15,
            offset: int | None = 0,
            search: Dict[str , any] | None = None,
    )->List[ModelType]:
         
        try:
            if limit is not None and limit <= 0:
                raise ValueError("Limit must be a positive integer")
            if offset is not None and offset < 0:
                raise ValueError("Offset must be a non-negative integer")
            
            stmt = select(model)
            if user_id is not None:
                    stmt = stmt.where(model.user_id == user_id)

            if search:
                for column , value in search.items():
                    if hasattr(model, column):
                        stmt = stmt.filter(getattr(model , column) == value)
                    else:
                        raise ValueError(f"Invalid search column: {column}")
            
            stmt = stmt.limit(limit).offset(offset)

            result = await self.db.execute(stmt)
            items = result.scalars().all()

            return items
         
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(ve)}"
            )

        except SQLAlchemyError as se:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(se)}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        
    async def get_by_field(
            self,
            model: Type[ModelType],
            field_name: str,
            field_value: any 
    ):
        try:
            if not field_name or not isinstance(field_name , str):
                raise ValueError("Field name must be a non-empty string")
            
            if not hasattr(model , field_name):
                raise ValueError(f"Invalid field name: {field_name}")
            
            stmt = select(model).where(getattr(model, field_name) == field_value)
            result = await self.db.execute(stmt)
            item = result.scalars().first()

            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{model.__name__} with {field_name}={field_value} not found"
                )
            return item
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(ve)}"
            )

        except SQLAlchemyError as se:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(se)}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    
    async def update(
            self,
            model: Type[ModelType],
            db_obj: SchemaType,
            item_id: int ,
            user_id: int | None = None,
    )-> ModelType:
        try:
            
            if not isinstance(item_id, int) or item_id <= 0:
                raise ValueError("item_id must be a positive integer")
            if not isinstance(db_obj, BaseModel):
                raise ValueError("db_obj must be a Pydantic model")


            stmt = select(model).where(model.id == item_id)
            if user_id is not None:
                    stmt = stmt.where(model.user_id == user_id)
            result = await self.db.execute(stmt)
            item = result.scalars().first()

            
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{model.__name__} with ID {item_id} not found"
                )

            # Update fields from Pydantic schema
            update_data = db_obj.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if value in ("string" , 0, "" , None):
                    continue
                if hasattr(item, key):
                    setattr(item, key, value)
                else:
                    raise ValueError(f"Invalid field for {model.__name__}: {key}")

            
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)

            return item

        except ValueError as ve:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(ve)}"
            )

        except SQLAlchemyError as se:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(se)}"
            )

        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        
    async def delete(
            self,
            model: Type[ModelType],
            item_id: int,
            user_id: int | None = None,
        ) -> ModelType:
            try:
            
                if not isinstance(item_id, int) or item_id <= 0:
                    raise ValueError("item_id must be a positive integer")

                
                stmt = select(model).where(model.id == item_id)
                if user_id is not None:
                    stmt = stmt.where(model.user_id == user_id)
                result = await self.db.execute(stmt)
                item = result.scalars().first()


                if not item:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{model.__name__} with ID {item_id} not found"
                    )

                # Delete the item
                await self.db.delete(item)
                await self.db.commit()

                return item

            except ValueError as ve:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Validation error: {str(ve)}"
                )

            except SQLAlchemyError as se:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {str(se)}"
                )

            except Exception as e:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(e)}"
                )
            
