import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import graphql_jwt
from graphql_jwt.shortcuts import get_token

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_active", "date_joined")


# Public queries + protected "me"
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)  # protected - requires authentication

    def resolve_all_users(root, info):
        # maybe restrict to staff in production
        return User.objects.all()

    def resolve_user(root, info, id):
        return User.objects.get(pk=id)

    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user


# Mutations
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()

    def mutate(self, info, username, email, password):
        # Basic create user. In production add validation
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
        token = get_token(user)  # returns JWT token string
        return CreateUser(user=user, token=token)


class Mutation(graphene.ObjectType):
    # Registration
    create_user = CreateUser.Field()

    # JWT builtin fields
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()  # login -> get token
    verify_token = graphql_jwt.Verify.Field()           # verify token
    refresh_token = graphql_jwt.Refresh.Field()         # refresh token
