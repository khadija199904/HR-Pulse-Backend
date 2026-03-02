from pydantic import BaseModel, Field
from typing import Optional

class JobProfile(BaseModel):
    job_title: str = Field(default="Data Scientist", alias="Job Title")
    job_description: str = Field(
        default="Nous recherchons un Data Scientist expérimenté en Python, SQL et Machine Learning.", 
        alias="Job Description"
    )
    rating: float = Field(default=4.0, alias="Rating", ge=-1, le=5)
    company_name: str = Field(default="Tech Solutions", alias="Company Name")
    location: str = Field(default="Paris, FR", alias="Location")
    headquarters: Optional[str] = Field(default="Paris, FR", alias="Headquarters")
    size: str = Field(default="201 to 500 employees", alias="Size")
    founded: int = Field(default=2010, alias="Founded")
    type_of_ownership: str = Field(default="Company - Private", alias="Type of ownership")
    industry: str = Field(default="IT Services", alias="Industry")
    sector: str = Field(default="Information Technology", alias="Sector")
    revenue: str = Field(default="$50 to $100 million (USD)", alias="Revenue")

    class Config:
        populate_by_name = True