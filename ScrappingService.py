from facebook_scraper import get_posts
from fastapi import FastAPI
import uvicorn

router  = FastAPI()
@router.get("/")  
async def root(): 

# Get the first 3 posts from a Facebook page
 for post in get_posts('GuinnessWorldRecords', pages=3):
   
    print(post['text'][:99])
    print(post['time']) 
    print(post['likes'])
    print(post['shares'])
    print(post['comments'])  
    print('\n')
    
 return {"message": "End of scrapping"}
  
#if __name__ == '__main__':
#   uvicorn.run(router,port=8000,host="0.0.0.0")