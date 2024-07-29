import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token, get_user_by_token
from graphene_django.types import DjangoObjectType
from .utils import generate_stream_token
import cloudinary
import cloudinary.uploader
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from django.contrib.auth import authenticate
from .models import CustomUser
from .authentication import generate_token
# from .scalars import CloudinaryImage

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "avatar")
        
    firstName = graphene.String()
    lastName = graphene.String()
    # avatar = CloudinaryImage()
    avatarUrl = graphene.String()

    def resolve_firstName(self, info):
        return self.first_name

    def resolve_lastName(self, info):
        return self.last_name
    
    def resolve_avatarUrl(self, info):
        # return self.avatar.url if self.avatar else None
        if self.avatar:
            return self.avatar
        return None

class SignupMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        username = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)
    userToken = graphene.String()

    def mutate(self, info, email, password, username):
        user = User(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save()
        token = get_token(user)
        userToken=generate_token(user)
        return SignupMutation(user=user, token=token, userToken=userToken)

    
class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    token = graphene.String()
    user = graphene.Field(lambda: UserType)  # Replace with your user type
    userToken = graphene.String()

    def mutate(self, info, email, password):
        user = authenticate(email=email, password=password)
        if user is None:
            raise Exception('Invalid credentials')

        # Generate the token
        token = get_token(user)
        userToken=generate_token(user)
        print(f"Generated userToken: {userToken}")

        return LoginMutation(success=True, token=token, user=user, userToken=userToken)
    
class GenerateStreamToken(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    token = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id):
        # Here you might want to add authentication to ensure the user is allowed to generate a token
        user = User.objects.get(id=user_id)
        if user:
            token = generate_stream_token(user_id)
            return GenerateStreamToken(token=token)  
        raise Exception("User not found")  

class LogoutMutation(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        # Invalidate the token here if you have token storage
        return LogoutMutation(success=True) 

class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        username = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, first_name=None, last_name=None, email=None, username = None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if username:
            user.username = username
        
        user.save()
        return UpdateProfileMutation(user=user)


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
    generate_stream_token = GenerateStreamToken.Field()
    update_profile = UpdateProfileMutation.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user
    
    def resolve_all_users(self, info):
        return User.objects.all()
    
schema = graphene.Schema(query=Query, mutation=Mutation)