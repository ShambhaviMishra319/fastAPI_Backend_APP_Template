import fastapi

from src.models.db.account import Account
from src.models.schemas.account import AccountInCreate,AccountInLogin,AccountInResponse,AccountInUpdate,AccountWithToken
from backend.src.repository.crud.accounts import AcountCRUDRepository
from src.securities.authorization.jwt import JWTGenerator
from src.api.dependencies.repository import get_repository

router =fastapi.APIRouter(prefix="/auth",tags=["authentication"])

@router.post(
    path="/signup",
    response_model=AccountInResponse,
    )
async def signup(
    account_create:AccountInCreate,
    account_repo:AcountCRUDRepository=fastapi.Depends(get_repository(repo_type=AcountCRUDRepository))

)->AccountInResponse:
    
    try:
        await account_repo.is_username_taken(username=account_create.username)
        await account_repo.is_email_taken(email=account_create.email)
    except:
        raise Exception("already there")
    
    new_account=await account_repo.create_account(create_account=account_create)
    access_token=await JWTGenerator.generate_access_token(account=new_account)

    return AccountInResponse(
        id=new_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=new_account.username,
            email=new_account.email,  # type: ignore
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at,
            updated_at=new_account.updated_at
        ),
    )
    
    





@router.post(path="signin")