from urllib import response
from urllib.parse import scheme_chars
from .. import models, schemas, oauth2
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine, get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/sqlachemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.ORM_Post).all()
    return {'data' : posts}

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.ORM_Post).filter(models.ORM_Post.title.contains(search)).limit(limit).offset(skip).all()
    
    result = db.query(models.ORM_Post, func.count(models.ORM_Vote.post_id).label("votes")).join(
        models.ORM_Vote, models.ORM_Vote.post_id == models.ORM_Post.id, isouter=True).group_by(
            models.ORM_Post.id).filter(models.ORM_Post.title.contains(search)).limit(limit).offset(skip).all()

    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000)
    # my_posts.append(post_dict)
    print(current_user.id)
    new_post = models.ORM_Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):
    # print(type(id))
    # post = find_post(id)
    print(limit)
    # post = db.query(models.ORM_Post).filter(models.ORM_Post.id == id).first()

    post = db.query(models.ORM_Post, func.count(models.ORM_Vote.post_id).label("votes")).join(
        models.ORM_Vote, models.ORM_Vote.post_id == models.ORM_Post.id, isouter=True).group_by(
            models.ORM_Post.id).filter(models.ORM_Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id: {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")
        
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that has required id
    #my_posts.pop(index)
    # index = find_index_post(id)
    # my_posts.pop(index)
    post_query = db.query(models.ORM_Post).filter(models.ORM_Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} does't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # index = find_index_post(id)
    post_query = db.query(models.ORM_Post).filter(models.ORM_Post.id == id)
    post = post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post
