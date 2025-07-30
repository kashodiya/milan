

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date
import models
import schemas
from auth import get_password_hash

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        profile_complete=False,
        account_status="active",
        registration_date=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_last_login(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db_user.last_login = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user

# Profile CRUD operations
def create_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    db_profile = models.UserProfile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    # Update user's profile_complete status
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user.profile_complete = True
    db.commit()
    
    return db_profile

def get_profile(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def update_profile(db: Session, user_id: int, profile: schemas.ProfileUpdate):
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if db_profile:
        update_data = profile.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

# Photo CRUD operations
def create_photo(db: Session, photo: schemas.PhotoCreate, profile_id: int):
    db_photo = models.Photo(**photo.dict(), profile_id=profile_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_photos(db: Session, profile_id: int):
    return db.query(models.Photo).filter(models.Photo.profile_id == profile_id).all()

def update_photo(db: Session, photo_id: int, photo: schemas.PhotoUpdate):
    db_photo = db.query(models.Photo).filter(models.Photo.photo_id == photo_id).first()
    if db_photo:
        update_data = photo.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_photo, key, value)
        db.commit()
        db.refresh(db_photo)
    return db_photo

def delete_photo(db: Session, photo_id: int):
    db_photo = db.query(models.Photo).filter(models.Photo.photo_id == photo_id).first()
    if db_photo:
        db.delete(db_photo)
        db.commit()
        return True
    return False

# Match Preference CRUD operations
def create_match_preference(db: Session, preference: schemas.MatchPreferenceCreate, user_id: int):
    db_preference = models.MatchPreference(**preference.dict(), user_id=user_id)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference

def get_match_preference(db: Session, user_id: int):
    return db.query(models.MatchPreference).filter(models.MatchPreference.user_id == user_id).first()

def update_match_preference(db: Session, user_id: int, preference: schemas.MatchPreferenceUpdate):
    db_preference = db.query(models.MatchPreference).filter(models.MatchPreference.user_id == user_id).first()
    if db_preference:
        update_data = preference.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_preference, key, value)
        db.commit()
        db.refresh(db_preference)
    return db_preference

# Family Detail CRUD operations
def create_family_detail(db: Session, family: schemas.FamilyDetailCreate, user_id: int):
    db_family = models.FamilyDetail(**family.dict(), user_id=user_id)
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

def get_family_detail(db: Session, user_id: int):
    return db.query(models.FamilyDetail).filter(models.FamilyDetail.user_id == user_id).first()

def update_family_detail(db: Session, user_id: int, family: schemas.FamilyDetailUpdate):
    db_family = db.query(models.FamilyDetail).filter(models.FamilyDetail.user_id == user_id).first()
    if db_family:
        update_data = family.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_family, key, value)
        db.commit()
        db.refresh(db_family)
    return db_family

# Connection CRUD operations
def create_connection(db: Session, connection: schemas.ConnectionCreate, sender_id: int):
    db_connection = models.Connection(
        sender_id=sender_id,
        receiver_id=connection.receiver_id,
        status=connection.status,
        connection_date=datetime.now(),
        last_updated=datetime.now()
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def get_connection(db: Session, connection_id: int):
    return db.query(models.Connection).filter(models.Connection.connection_id == connection_id).first()

def get_connections_by_user(db: Session, user_id: int, status: str = None):
    query = db.query(models.Connection).filter(
        or_(
            models.Connection.sender_id == user_id,
            models.Connection.receiver_id == user_id
        )
    )
    if status:
        query = query.filter(models.Connection.status == status)
    return query.all()

def update_connection(db: Session, connection_id: int, connection: schemas.ConnectionUpdate):
    db_connection = db.query(models.Connection).filter(models.Connection.connection_id == connection_id).first()
    if db_connection:
        db_connection.status = connection.status
        db_connection.last_updated = datetime.now()
        db.commit()
        db.refresh(db_connection)
    return db_connection

# Message CRUD operations
def create_message(db: Session, message: schemas.MessageCreate, sender_id: int):
    db_message = models.Message(
        sender_id=sender_id,
        receiver_id=message.receiver_id,
        message_text=message.message_text,
        sent_date=datetime.now()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, user1_id: int, user2_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == user1_id, models.Message.receiver_id == user2_id),
            and_(models.Message.sender_id == user2_id, models.Message.receiver_id == user1_id)
        )
    ).order_by(models.Message.sent_date.desc()).offset(skip).limit(limit).all()

def mark_message_as_read(db: Session, message_id: int):
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if db_message and not db_message.read_date:
        db_message.read_date = datetime.now()
        db.commit()
        db.refresh(db_message)
    return db_message

# Membership CRUD operations
def create_membership(db: Session, membership: schemas.MembershipCreate, user_id: int):
    db_membership = models.Membership(
        user_id=user_id,
        membership_type=membership.membership_type,
        start_date=datetime.now(),
        end_date=membership.end_date,
        payment_status=membership.payment_status
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

def get_membership(db: Session, user_id: int):
    return db.query(models.Membership).filter(models.Membership.user_id == user_id).first()

def update_membership(db: Session, user_id: int, membership: schemas.MembershipUpdate):
    db_membership = db.query(models.Membership).filter(models.Membership.user_id == user_id).first()
    if db_membership:
        update_data = membership.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_membership, key, value)
        db.commit()
        db.refresh(db_membership)
    return db_membership

# Success Story CRUD operations
def create_success_story(db: Session, story: schemas.SuccessStoryCreate, user_id: int):
    db_story = models.SuccessStory(
        user_id=user_id,
        partner_id=story.partner_id,
        story_title=story.story_title,
        story_content=story.story_content,
        wedding_date=story.wedding_date,
        story_date=datetime.now(),
        is_featured=False,
        is_approved=False
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_success_story(db: Session, story_id: int):
    return db.query(models.SuccessStory).filter(models.SuccessStory.story_id == story_id).first()

def get_success_stories(db: Session, approved_only: bool = True, featured_only: bool = False, skip: int = 0, limit: int = 100):
    query = db.query(models.SuccessStory)
    if approved_only:
        query = query.filter(models.SuccessStory.is_approved == True)
    if featured_only:
        query = query.filter(models.SuccessStory.is_featured == True)
    return query.offset(skip).limit(limit).all()

def update_success_story(db: Session, story_id: int, story: schemas.SuccessStoryUpdate):
    db_story = db.query(models.SuccessStory).filter(models.SuccessStory.story_id == story_id).first()
    if db_story:
        update_data = story.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_story, key, value)
        db.commit()
        db.refresh(db_story)
    return db_story

# Success Story Photo CRUD operations
def create_success_story_photo(db: Session, photo: schemas.SuccessStoryPhotoCreate, story_id: int):
    db_photo = models.SuccessStoryPhoto(
        story_id=story_id,
        photo_url=photo.photo_url,
        upload_date=datetime.now()
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_success_story_photos(db: Session, story_id: int):
    return db.query(models.SuccessStoryPhoto).filter(models.SuccessStoryPhoto.story_id == story_id).all()

# Match finding operations
def find_matches(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    # Get the user's profile and preferences
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    user_preferences = db.query(models.MatchPreference).filter(models.MatchPreference.user_id == user_id).first()
    
    if not user_profile or not user_preferences:
        return []
    
    # Calculate age from date of birth
    today = date.today()
    user_age = today.year - user_profile.date_of_birth.year - ((today.month, today.day) < (user_profile.date_of_birth.month, user_profile.date_of_birth.day))
    
    # Get opposite gender
    opposite_gender = "female" if user_profile.gender == "male" else "male"
    
    # Build the query based on preferences
    query = db.query(models.UserProfile).join(models.User).filter(
        models.User.account_status == "active",
        models.User.profile_complete == True,
        models.UserProfile.gender == opposite_gender
    )
    
    # Apply age filter if specified
    if user_preferences.min_age and user_preferences.max_age:
        min_dob = date(today.year - user_preferences.max_age, today.month, today.day)
        max_dob = date(today.year - user_preferences.min_age, today.month, today.day)
        query = query.filter(models.UserProfile.date_of_birth.between(min_dob, max_dob))
    
    # Apply height filter if specified
    if user_preferences.height_min:
        query = query.filter(models.UserProfile.height >= user_preferences.height_min)
    if user_preferences.height_max:
        query = query.filter(models.UserProfile.height <= user_preferences.height_max)
    
    # Apply religion filter if specified
    if user_preferences.religion:
        query = query.filter(models.UserProfile.religion == user_preferences.religion)
    
    # Apply location filter if specified and it's a simple country match
    if user_preferences.location_preferences and "country" in user_preferences.location_preferences.lower():
        query = query.filter(models.UserProfile.location_country == user_profile.location_country)
    
    # Exclude the user themselves and any blocked connections
    blocked_connections = db.query(models.Connection).filter(
        or_(
            and_(models.Connection.sender_id == user_id, models.Connection.status == "blocked"),
            and_(models.Connection.receiver_id == user_id, models.Connection.status == "blocked")
        )
    ).all()
    
    blocked_ids = [conn.receiver_id if conn.sender_id == user_id else conn.sender_id for conn in blocked_connections]
    blocked_ids.append(user_id)  # Add the user's own ID to the exclusion list
    
    query = query.filter(~models.UserProfile.user_id.in_(blocked_ids))
    
    # Order by last login time to prioritize active users
    query = query.join(models.User).order_by(models.User.last_login.desc().nullslast())
    
    return query.offset(skip).limit(limit).all()

