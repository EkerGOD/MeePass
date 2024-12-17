# 查询组
import logging
from collections import deque
from db import get_session
from models.groups import Groups

logger = logging.getLogger(__name__)

def select_groups():
    session = get_session()
    rows = session.query(Groups).all()
    session.close()
    return rows

def insert_groups(name, parent_id, notes):
    logger.info("正在插入组...")
    session = get_session()

    try:
        group = Groups(
            name=name,
            parent_id=parent_id,
            notes=notes
        )
        session.add(group)
        session.commit()
        logger.info("插入完毕")
    except Exception as e:
        session.rollback()
        logger.error(f"插入组失败，错误: {e}")
    finally:
        session.close()

def delete_groups(group_id):
    delete_num = 0
    session = get_session()
    queue =deque([group_id])

    # 删除根节点
    delete_num += session.query(Groups).filter(Groups.id == group_id).delete()

    while queue:
        parent_id = queue.popleft()
        child_nodes = session.query(Groups).filter_by(parent_id=parent_id).all()

        queue.extend([node.id for node in child_nodes])

        delete_num += session.query(Groups).filter_by(parent_id=parent_id).delete()

    session.commit()
    session.close()
    return delete_num

def update_groups(group_id, name, parent_id, notes):
    session = get_session()
    session.query(Groups).filter_by(id=group_id).update(
        {Groups.name: name, Groups.parent_id: parent_id, Groups.notes: notes}
    )
    session.commit()
    session.close()


