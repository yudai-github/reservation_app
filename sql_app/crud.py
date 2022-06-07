from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

#read
#ユーザー一覧を取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#会議室一覧を取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

#予約一覧を取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

#create
#ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(username = user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#会議室登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name = room.room_name, capacity = room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

#ユーザー登録
def create_booking(db: Session, booking: schemas.Booking):
    # 重複するデータを探す
    db_booked = db.query(models.Booking).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()
    # 重複するデータがない場合の処理
    if len(db_booked) == 0:
        db_booking = models.Booking(
            user_id = booking.user_id,
            room_id = booking.room_id,
            booked_num = booking.booked_num,
            start_datetime = booking.start_datetime,
            end_datetime = booking.end_datetime
            )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail="Already booked")
