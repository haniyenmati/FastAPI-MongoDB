from mongoengine import Document


async def get_object_or_none(_klass: Document, **kwargs):
    obj = _klass.objects(**kwargs)

    if obj:
        return obj.first()
    return None
