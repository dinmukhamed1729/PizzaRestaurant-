from ninja import Schema


def update_model_instance(instance, data: Schema):
    data_dict = data.dict(exclude_unset=True)
    for attr, value in data_dict.items():
        if hasattr(instance, attr):
            field = instance._meta.get_field(attr)
            if field.many_to_many:
                getattr(instance, attr).set(value or [])
            else:
                setattr(instance, attr, value)

    instance.save()
    return instance
