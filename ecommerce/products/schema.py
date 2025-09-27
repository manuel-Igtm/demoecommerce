import graphene
from graphene_django import DjangoObjectType
from .models import Product, Category


# ------------------------------
# Category Schema
# ------------------------------
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, slug):
        category = Category.objects.create(name=name, slug=slug)
        return CreateCategory(category=category)


# ------------------------------
# Product Schema
# ------------------------------
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "category")


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)
        category_id = graphene.ID(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, description, price, category_id):
        category = Category.objects.get(pk=category_id)
        product = Product.objects.create(
            name=name, description=description, price=price, category=category
        )
        return CreateProduct(product=product)


# ------------------------------
# Queries
# ------------------------------
class Query(graphene.ObjectType):
    # Products
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID(required=True))

    # Categories
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))

    def resolve_all_products(root, info):
        return Product.objects.select_related("category").all()

    def resolve_product(root, info, id):
        return Product.objects.get(pk=id)

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_category(root, info, id):
        return Category.objects.get(pk=id)


# ------------------------------
# Mutations
# ------------------------------
class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_category = CreateCategory.Field()
