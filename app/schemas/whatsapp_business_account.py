from typing import List, Optional
from pydantic import BaseModel, Field

class Text(BaseModel):
    body: str

class Message(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    text: Text
    type: str

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[Contact]
    messages: List[Message]

class Change(BaseModel):
    value: Value
    field: str

class Entry(BaseModel):
    id: str
    changes: List[Change]

class WhatsAppBusinessAccount(BaseModel):
    object: str
    entry: List[Entry]
