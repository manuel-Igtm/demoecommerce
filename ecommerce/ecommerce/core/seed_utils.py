# ecommerce/core/seed_utils.py

def seed_model(model, data_list, unique_field=None):
    """
    Generic seeding utility for any model.
    - model: The Django model to seed
    - data_list: List of dicts with model data
    - unique_field: Optional field to prevent duplicates
    """
    created_objects = []
    for data in data_list:
        if unique_field:
            obj, _ = model.objects.get_or_create(
                **{unique_field: data[unique_field]},
                defaults=data
            )
        else:
            obj = model.objects.create(**data)
        created_objects.append(obj)
    return created_objects
