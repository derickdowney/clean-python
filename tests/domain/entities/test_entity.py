from dataclasses import dataclass
from uuid import UUID

from clean_python.domain.entities.entity import Entity


def test_Entity_can_init():
    entity: Entity = Entity()
    assert isinstance(entity, Entity)


def test_Entity_init_with_id_as_UUID():
    entity: Entity = Entity()
    assert isinstance(entity.id, UUID)


def test_Entity_ids_are_unique():
    id1: UUID = Entity().id
    id2: UUID = Entity().id
    assert id1 != id2


def test_two_Entity_objs_are_equal_if_same_id():
    # @dataclass() # this causes test to fail
    @dataclass(eq=False)  # this causes test to pass
    class SubEntity(Entity):
        extra_attribute: str

    e1: SubEntity = SubEntity("extra1")
    e2: SubEntity = SubEntity("extra2")
    e2.id = e1.id

    assert e1 == e2


def test_Entity_hash_is_based_off_id_only():
    # @dataclass() # this causes test to fail
    @dataclass(eq=False)  # this causes test to pass
    class SubEntity(Entity):
        extra_attribute: str

    entity: Entity = Entity()
    sub_entity: SubEntity = SubEntity("extra")
    sub_entity.id = entity.id

    assert hash(entity) == hash(sub_entity)
