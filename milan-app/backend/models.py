
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Date, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    profile_complete = Column(Boolean, default=False)
    account_status = Column(String, default="active")  # active, inactive, suspended
    registration_date = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    preferences = relationship("MatchPreference", back_populates="user", uselist=False)
    family_details = relationship("FamilyDetail", back_populates="user", uselist=False)
    sent_connections = relationship("Connection", foreign_keys="Connection.sender_id", back_populates="sender")
    received_connections = relationship("Connection", foreign_keys="Connection.receiver_id", back_populates="receiver")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    membership = relationship("Membership", back_populates="user", uselist=False)
    success_stories = relationship("SuccessStory", foreign_keys="SuccessStory.user_id", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)  # male, female, other
    date_of_birth = Column(Date)
    height = Column(Float)
    religion = Column(String)
    caste = Column(String)
    mother_tongue = Column(String)
    marital_status = Column(String)  # never_married, divorced, widowed, separated
    about_me = Column(Text)
    occupation = Column(String)
    education = Column(String)
    income_bracket = Column(String)
    location_city = Column(String)
    location_state = Column(String)
    location_country = Column(String)
    profile_photo = Column(String)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
    photos = relationship("Photo", back_populates="profile")

class Photo(Base):
    __tablename__ = "photos"
    
    photo_id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.profile_id"))
    photo_url = Column(String)
    is_primary = Column(Boolean, default=False)
    visibility = Column(String, default="all")  # all, connected, premium
    upload_date = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="photos")

class MatchPreference(Base):
    __tablename__ = "match_preferences"
    
    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    min_age = Column(Integer)
    max_age = Column(Integer)
    height_min = Column(Float)
    height_max = Column(Float)
    religion = Column(String)
    caste_preferences = Column(Text)
    education_level = Column(String)
    income_min = Column(Float)
    location_preferences = Column(Text)
    other_preferences = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="preferences")

class FamilyDetail(Base):
    __tablename__ = "family_details"
    
    family_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    father_occupation = Column(String)
    mother_occupation = Column(String)
    siblings_count = Column(Integer)
    family_type = Column(String)  # nuclear, joint, other
    family_values = Column(String)  # traditional, moderate, liberal
    about_family = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="family_details")

class Connection(Base):
    __tablename__ = "connections"
    
    connection_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    receiver_id = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String)  # pending, accepted, rejected, blocked
    connection_date = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_connections")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_connections")

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    receiver_id = Column(Integer, ForeignKey("users.user_id"))
    message_text = Column(Text)
    sent_date = Column(DateTime, default=func.now())
    read_date = Column(DateTime)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

class Membership(Base):
    __tablename__ = "memberships"
    
    membership_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    membership_type = Column(String)  # free, premium, gold
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    payment_status = Column(String)  # paid, pending, failed
    
    # Relationships
    user = relationship("User", back_populates="membership")

class SuccessStory(Base):
    __tablename__ = "success_stories"
    
    story_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    partner_id = Column(Integer, ForeignKey("users.user_id"))
    story_title = Column(String)
    story_content = Column(Text)
    wedding_date = Column(Date)
    story_date = Column(DateTime, default=func.now())
    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="success_stories")
    partner = relationship("User", foreign_keys=[partner_id])
    photos = relationship("SuccessStoryPhoto", back_populates="story")

class SuccessStoryPhoto(Base):
    __tablename__ = "success_story_photos"
    
    photo_id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("success_stories.story_id"))
    photo_url = Column(String)
    upload_date = Column(DateTime, default=func.now())
    
    # Relationships
    story = relationship("SuccessStory", back_populates="photos")
