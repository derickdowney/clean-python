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
