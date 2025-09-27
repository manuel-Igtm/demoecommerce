import pytest
from graphene.test import Client
from django.contrib.auth import get_user_model
from ecommerce.schema import schema  # root schema
from django.test import Client as DjangoClient

User = get_user_model()

@pytest.mark.django_db
def test_register_and_me_query():
    client = Client(schema)

    # 1) Register (mutation returns token and user)
    register_mutation = """
    mutation Register($username: String!, $email: String!, $password: String!) {
      createUser(username: $username, email: $email, password: $password) {
        token
        user {
          id
          username
          email
        }
      }
    }
    """

    variables = {"username": "gqluser", "email": "gql@example.com", "password": "pass1234"}
    executed = client.execute(register_mutation, variable_values=variables)
    assert "errors" not in executed
    payload = executed["data"]["createUser"]
    assert payload["user"]["username"] == "gqluser"
    token = payload["token"]
    assert token is not None and token != ""

    # 2) Query 'me' with token in headers
    # graphene.test.Client requires passing context_value simulating request
    from django.test import RequestFactory
    rf = RequestFactory()
    req = rf.post("/graphql/")
    req.META["HTTP_AUTHORIZATION"] = f"JWT {token}"

    executed_me = client.execute(
        """
        query { me { id username email } }
        """,
        context_value=req
    )
    assert "errors" not in executed_me
    me = executed_me["data"]["me"]
    assert me["username"] == "gqluser"


@pytest.mark.django_db
def test_token_auth_mutation_login():
    # Create user manually
    user = User.objects.create_user(username="loginuser", email="login@example.com", password="mypassword")
    c = Client(schema)

    # Use tokenAuth mutation to get token
    login_mutation = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
      }
    }
    """

    executed = c.execute(login_mutation, variable_values={"username": "loginuser", "password": "mypassword"})
    assert "errors" not in executed
    assert executed["data"]["tokenAuth"]["token"] is not None
