import graphene
import products.schema
import users.schema
import payments.schema



class Query(
    products.schema.Query,
    users.schema.Query,
    payments.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    products.schema.Mutation,
    payments.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
