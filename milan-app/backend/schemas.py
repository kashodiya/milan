
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    profile_complete: Optional[bool] = None
    account_status: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    profile_complete: bool
    account_status: str
    registration_date: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Profile schemas
class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    height: Optional[float] = None
    religion: Optional[str] = None
    caste: Optional[str] = None
    mother_tongue: Optional[str] = None
    marital_status: str
    about_me: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    income_bracket: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None
    profile_photo: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[float] = None
    religion: Optional[str] = None
    caste: Optional[str] = None
    mother_tongue: Optional[str] = None
    marital_status: Optional[str] = None
    about_me: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    income_bracket: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None
    profile_photo: Optional[str] = None

class ProfileResponse(ProfileBase):
    profile_id: int
    user_id: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# Photo schemas
class PhotoBase(BaseModel):
    photo_url: str
    is_primary: bool = False
    visibility: str = "all"

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    photo_url: Optional[str] = None
    is_primary: Optional[bool] = None
    visibility: Optional[str] = None

class PhotoResponse(PhotoBase):
    photo_id: int
    profile_id: int
    upload_date: datetime

    class Config:
        from_attributes = True

# Match Preference schemas
class MatchPreferenceBase(BaseModel):
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    height_min: Optional[float] = None
    height_max: Optional[float] = None
    religion: Optional[str] = None
    caste_preferences: Optional[str] = None
    education_level: Optional[str] = None
    income_min: Optional[float] = None
    location_preferences: Optional[str] = None
    other_preferences: Optional[str] = None

class MatchPreferenceCreate(MatchPreferenceBase):
    pass

class MatchPreferenceUpdate(MatchPreferenceBase):
    pass

class MatchPreferenceResponse(MatchPreferenceBase):
    preference_id: int
    user_id: int

    class Config:
        from_attributes = True

# Family Detail schemas
class FamilyDetailBase(BaseModel):
    father_occupation: Optional[str] = None
    mother_occupation: Optional[str] = None
    siblings_count: Optional[int] = None
    family_type: Optional[str] = None
    family_values: Optional[str] = None
    about_family: Optional[str] = None

class FamilyDetailCreate(FamilyDetailBase):
    pass

class FamilyDetailUpdate(FamilyDetailBase):
    pass

class FamilyDetailResponse(FamilyDetailBase):
    family_id: int
    user_id: int

    class Config:
        from_attributes = True

# Connection schemas
class ConnectionBase(BaseModel):
    receiver_id: int
    status: str = "pending"

class ConnectionCreate(ConnectionBase):
    pass

class ConnectionUpdate(BaseModel):
    status: str

class ConnectionResponse(BaseModel):
    connection_id: int
    sender_id: int
    receiver_id: int
    status: str
    connection_date: datetime
    last_updated: datetime

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    receiver_id: int
    message_text: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    message_text: str
    sent_date: datetime
    read_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# Membership schemas
class MembershipBase(BaseModel):
    membership_type: str
    end_date: datetime
    payment_status: str = "pending"

class MembershipCreate(MembershipBase):
    pass

class MembershipUpdate(BaseModel):
    membership_type: Optional[str] = None
    end_date: Optional[datetime] = None
    payment_status: Optional[str] = None

class MembershipResponse(MembershipBase):
    membership_id: int
    user_id: int
    start_date: datetime

    class Config:
        from_attributes = True

# Success Story schemas
class SuccessStoryBase(BaseModel):
    partner_id: int
    story_title: str
    story_content: str
    wedding_date: date

class SuccessStoryCreate(SuccessStoryBase):
    pass

class SuccessStoryUpdate(BaseModel):
    story_title: Optional[str] = None
    story_content: Optional[str] = None
    wedding_date: Optional[date] = None
    is_featured: Optional[bool] = None
    is_approved: Optional[bool] = None

class SuccessStoryResponse(SuccessStoryBase):
    story_id: int
    user_id: int
    story_date: datetime
    is_featured: bool
    is_approved: bool

    class Config:
        from_attributes = True

# Success Story Photo schemas
class SuccessStoryPhotoBase(BaseModel):
    photo_url: str

class SuccessStoryPhotoCreate(SuccessStoryPhotoBase):
    pass

class SuccessStoryPhotoResponse(SuccessStoryPhotoBase):
    photo_id: int
    story_id: int
    upload_date: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
