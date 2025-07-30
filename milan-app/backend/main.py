

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path

import crud
import models
import schemas
import auth
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Create upload directories if they don't exist
UPLOAD_DIR = Path("uploads")
PROFILE_PHOTOS_DIR = UPLOAD_DIR / "profile_photos"
SUCCESS_STORY_PHOTOS_DIR = UPLOAD_DIR / "success_story_photos"

PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
SUCCESS_STORY_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Matrimonial Service API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Update last login time
    crud.update_last_login(db, user.user_id)
    
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.put("/users/me/", response_model=schemas.UserResponse)
def update_user_me(user: schemas.UserUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=current_user.user_id, user=user)

# Profile endpoints
@app.post("/profiles/", response_model=schemas.ProfileResponse)
def create_profile(profile: schemas.ProfileCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return crud.create_profile(db=db, profile=profile, user_id=current_user.user_id)

@app.get("/profiles/me/", response_model=schemas.ProfileResponse)
def read_profile_me(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.put("/profiles/me/", response_model=schemas.ProfileResponse)
def update_profile_me(profile: schemas.ProfileUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return crud.update_profile(db=db, user_id=current_user.user_id, profile=profile)

@app.get("/profiles/{user_id}", response_model=schemas.ProfileResponse)
def read_profile(user_id: int, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

# Photo endpoints
@app.post("/photos/", response_model=schemas.PhotoResponse)
async def upload_photo(
    file: UploadFile = File(...),
    is_primary: bool = Form(False),
    visibility: str = Form("all"),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if user has a profile
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Save the uploaded file
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{current_user.user_id}_{datetime.now().timestamp()}{file_extension}"
    file_path = PROFILE_PHOTOS_DIR / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create photo record in database
    photo_data = schemas.PhotoCreate(
        photo_url=f"/uploads/profile_photos/{filename}",
        is_primary=is_primary,
        visibility=visibility
    )
    
    # If this is the primary photo, update the profile
    if is_primary:
        crud.update_profile(
            db=db,
            user_id=current_user.user_id,
            profile=schemas.ProfileUpdate(profile_photo=f"/uploads/profile_photos/{filename}")
        )
    
    return crud.create_photo(db=db, photo=photo_data, profile_id=db_profile.profile_id)

@app.get("/photos/me/", response_model=List[schemas.PhotoResponse])
def read_my_photos(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return crud.get_photos(db, profile_id=db_profile.profile_id)

@app.get("/photos/{user_id}", response_model=List[schemas.PhotoResponse])
def read_user_photos(user_id: int, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return crud.get_photos(db, profile_id=db_profile.profile_id)

@app.delete("/photos/{photo_id}")
def delete_photo(photo_id: int, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    # Verify the photo belongs to the current user
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    photos = crud.get_photos(db, profile_id=db_profile.profile_id)
    photo_ids = [photo.photo_id for photo in photos]
    
    if photo_id not in photo_ids:
        raise HTTPException(status_code=403, detail="Not authorized to delete this photo")
    
    result = crud.delete_photo(db, photo_id=photo_id)
    if not result:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    return {"detail": "Photo deleted successfully"}

# Match Preference endpoints
@app.post("/preferences/", response_model=schemas.MatchPreferenceResponse)
def create_match_preference(preference: schemas.MatchPreferenceCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_preference = crud.get_match_preference(db, user_id=current_user.user_id)
    if db_preference:
        raise HTTPException(status_code=400, detail="Match preferences already exist")
    return crud.create_match_preference(db=db, preference=preference, user_id=current_user.user_id)

@app.get("/preferences/me/", response_model=schemas.MatchPreferenceResponse)
def read_match_preference_me(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_preference = crud.get_match_preference(db, user_id=current_user.user_id)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="Match preferences not found")
    return db_preference

@app.put("/preferences/me/", response_model=schemas.MatchPreferenceResponse)
def update_match_preference_me(preference: schemas.MatchPreferenceUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_preference = crud.get_match_preference(db, user_id=current_user.user_id)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="Match preferences not found")
    return crud.update_match_preference(db=db, user_id=current_user.user_id, preference=preference)

# Family Detail endpoints
@app.post("/family/", response_model=schemas.FamilyDetailResponse)
def create_family_detail(family: schemas.FamilyDetailCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_family = crud.get_family_detail(db, user_id=current_user.user_id)
    if db_family:
        raise HTTPException(status_code=400, detail="Family details already exist")
    return crud.create_family_detail(db=db, family=family, user_id=current_user.user_id)

@app.get("/family/me/", response_model=schemas.FamilyDetailResponse)
def read_family_detail_me(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_family = crud.get_family_detail(db, user_id=current_user.user_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    return db_family

@app.put("/family/me/", response_model=schemas.FamilyDetailResponse)
def update_family_detail_me(family: schemas.FamilyDetailUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_family = crud.get_family_detail(db, user_id=current_user.user_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    return crud.update_family_detail(db=db, user_id=current_user.user_id, family=family)

@app.get("/family/{user_id}", response_model=schemas.FamilyDetailResponse)
def read_family_detail(user_id: int, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_family = crud.get_family_detail(db, user_id=user_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    return db_family

# Connection endpoints
@app.post("/connections/", response_model=schemas.ConnectionResponse)
def create_connection(connection: schemas.ConnectionCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    # Check if connection already exists
    connections = crud.get_connections_by_user(db, user_id=current_user.user_id)
    for conn in connections:
        if (conn.sender_id == current_user.user_id and conn.receiver_id == connection.receiver_id) or \
           (conn.receiver_id == current_user.user_id and conn.sender_id == connection.receiver_id):
            raise HTTPException(status_code=400, detail="Connection already exists")
    
    return crud.create_connection(db=db, connection=connection, sender_id=current_user.user_id)

@app.get("/connections/", response_model=List[schemas.ConnectionResponse])
def read_connections(status: Optional[str] = None, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_connections_by_user(db, user_id=current_user.user_id, status=status)

@app.put("/connections/{connection_id}", response_model=schemas.ConnectionResponse)
def update_connection(connection_id: int, connection: schemas.ConnectionUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_connection = crud.get_connection(db, connection_id=connection_id)
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    # Only the receiver can update the connection status
    if db_connection.receiver_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this connection")
    
    return crud.update_connection(db=db, connection_id=connection_id, connection=connection)

# Message endpoints
@app.post("/messages/", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    # Check if there's a connection between users
    connections = crud.get_connections_by_user(db, user_id=current_user.user_id)
    can_message = False
    
    # Check if user has premium membership
    membership = crud.get_membership(db, user_id=current_user.user_id)
    is_premium = membership and membership.membership_type in ["premium", "gold"] and membership.end_date > datetime.now()
    
    if is_premium:
        can_message = True
    else:
        for conn in connections:
            if ((conn.sender_id == current_user.user_id and conn.receiver_id == message.receiver_id) or 
                (conn.receiver_id == current_user.user_id and conn.sender_id == message.receiver_id)) and conn.status == "accepted":
                can_message = True
                break
    
    if not can_message:
        raise HTTPException(status_code=403, detail="Cannot message this user without an accepted connection or premium membership")
    
    return crud.create_message(db=db, message=message, sender_id=current_user.user_id)

@app.get("/messages/{user_id}", response_model=List[schemas.MessageResponse])
def read_messages(user_id: int, skip: int = 0, limit: int = 100, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_messages(db, user1_id=current_user.user_id, user2_id=user_id, skip=skip, limit=limit)

@app.put("/messages/{message_id}/read")
def mark_message_read(message_id: int, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    message = crud.mark_message_as_read(db, message_id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.receiver_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to mark this message as read")
    return {"detail": "Message marked as read"}

# Membership endpoints
@app.post("/memberships/", response_model=schemas.MembershipResponse)
def create_membership(membership: schemas.MembershipCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_membership = crud.get_membership(db, user_id=current_user.user_id)
    if db_membership:
        raise HTTPException(status_code=400, detail="Membership already exists")
    return crud.create_membership(db=db, membership=membership, user_id=current_user.user_id)

@app.get("/memberships/me/", response_model=schemas.MembershipResponse)
def read_membership_me(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_membership = crud.get_membership(db, user_id=current_user.user_id)
    if db_membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    return db_membership

@app.put("/memberships/me/", response_model=schemas.MembershipResponse)
def update_membership_me(membership: schemas.MembershipUpdate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    db_membership = crud.get_membership(db, user_id=current_user.user_id)
    if db_membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    return crud.update_membership(db=db, user_id=current_user.user_id, membership=membership)

# Success Story endpoints
@app.post("/success-stories/", response_model=schemas.SuccessStoryResponse)
def create_success_story(story: schemas.SuccessStoryCreate, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.create_success_story(db=db, story=story, user_id=current_user.user_id)

@app.get("/success-stories/", response_model=List[schemas.SuccessStoryResponse])
def read_success_stories(approved_only: bool = True, featured_only: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_success_stories(db, approved_only=approved_only, featured_only=featured_only, skip=skip, limit=limit)

@app.get("/success-stories/{story_id}", response_model=schemas.SuccessStoryResponse)
def read_success_story(story_id: int, db: Session = Depends(get_db)):
    db_story = crud.get_success_story(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Success story not found")
    return db_story

@app.post("/success-stories/{story_id}/photos", response_model=schemas.SuccessStoryPhotoResponse)
async def upload_success_story_photo(
    story_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if story exists and belongs to the user
    db_story = crud.get_success_story(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Success story not found")
    if db_story.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to add photos to this story")
    
    # Save the uploaded file
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"story_{story_id}_{datetime.now().timestamp()}{file_extension}"
    file_path = SUCCESS_STORY_PHOTOS_DIR / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create photo record in database
    photo_data = schemas.SuccessStoryPhotoCreate(
        photo_url=f"/uploads/success_story_photos/{filename}"
    )
    
    return crud.create_success_story_photo(db=db, photo=photo_data, story_id=story_id)

@app.get("/success-stories/{story_id}/photos", response_model=List[schemas.SuccessStoryPhotoResponse])
def read_success_story_photos(story_id: int, db: Session = Depends(get_db)):
    db_story = crud.get_success_story(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Success story not found")
    return crud.get_success_story_photos(db, story_id=story_id)

# Match finding endpoints
@app.get("/matches/", response_model=List[schemas.ProfileResponse])
def find_matches(skip: int = 0, limit: int = 20, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    # Check if user has completed profile and preferences
    db_profile = crud.get_profile(db, user_id=current_user.user_id)
    if db_profile is None:
        raise HTTPException(status_code=400, detail="Please complete your profile first")
    
    db_preference = crud.get_match_preference(db, user_id=current_user.user_id)
    if db_preference is None:
        raise HTTPException(status_code=400, detail="Please set your match preferences first")
    
    return crud.find_matches(db, user_id=current_user.user_id, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=56396)

