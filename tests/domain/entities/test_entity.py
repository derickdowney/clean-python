from clean_python.domain.entities.entity import Entity


def test_Entity_can_init():
    entity: Entity = Entity()
    assert isinstance(entity, Entity)
