from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import validators
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import csv
import os


app = FastAPI()

# configuring the database connection
DATABASE_URL = 'mysql+mysqlconnector://root:Vijay$555@localhost:3306/rubixe_emp'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))

@app.get("/extract_urls")
async def extract_urls(url: str):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags and extract the href attribute (URLs)
        urls = [a['href'] for a in soup.find_all('a', href=True)]

        # validating urls
        validated_urls=[]
        for url in urls:
            if validators.url(url):
                validated_urls.append(url)
               
        db = SessionLocal()
        db.commit()

        # Getting existing URLs from the database
        existing_urls = [result[0] for result in db.query(URL.url).all()]

        # Deleting existing records from the urls table
        db.query(URL).delete()
        db.commit()

        for url in validated_urls:
            db_url= URL(url=url)
            db.add(db_url)

        db.commit()

        # Saving URLs to csv file
        save_urls_to_csv(validated_urls)

        return {"urls": validated_urls, "Message":"URLs saved to CSV file successfully"}

    except Exception as e:
        return {"error": str(e)}

def save_urls_to_csv(urls):
    with open("urls.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URLs'])
        writer.writerows([[url] for url in urls])

