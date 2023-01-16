from sqlalchemy.exc import IntegrityError

from menu.models import engine, Menu, Submenu, Dish
from sqlalchemy import func, distinct, and_
from sqlalchemy.orm import sessionmaker


class DBsessionSingleton(object):
    _session = None

    def __new__(cls, *args, **kwargs):
        _instance = object.__new__(cls, *args, **kwargs)
        if cls._session is None:
            cls._conf = sessionmaker()
            cls._conf.configure(bind=engine)
            cls._session = cls._conf()
        _instance._connect = cls._session
        return _instance


class MenuSession(DBsessionSingleton):

    @classmethod
    def get_connect(cls):
        return cls()

    def get_elem(self, id: int = 0):
        result = self._connect.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)) \
            .outerjoin(Submenu, Menu.id == Submenu.menu_id) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .filter(Menu.id == id) \
            .group_by(Menu.id)
        if result.first() is None:
            return {}
        return self._get_dict(result.first())

    def get_elems(self):
        result = self._connect.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)) \
            .outerjoin(Submenu, Menu.id == Submenu.menu_id) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .group_by(Menu.id)
        if result.first() is None:
            return []
        return self._serializer(result)

    def _serializer(self, elements):
        result_list = []
        for element in elements:
            result_list.append(self._get_dict(element))
        return result_list

    def _get_dict(self, element):
        first, second, thread = element
        return {
            'id': str(first.id),
            'title': first.title,
            'description': first.description,
            'submenus_count': second,
            'dishes_count': thread
        }

    def delete(self, id: int) -> bool:
        result = self._connect.query(Menu).filter(Menu.id == id ).delete()
        if result:
            self._connect.commit()
        return bool(result)

    def create(self, instance: Menu):
        self._connect.add(instance)
        self._connect.commit()
        return instance

    def update(self, id: int, fields: dict) -> Menu | None:
        result = self._connect.query(Menu).filter(Menu.id == id)
        if result.first():
            result.update(fields)
            self._connect.commit()
            return self.get_elem(id)





class SubmenuSession(DBsessionSingleton):

    @classmethod
    def get_connect(cls):
        return cls()

    def get_elem(self, menu_id: int, submenu_id: int):
        result = self._connect.query(Submenu, func.count(Dish.id)) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .filter(and_(Submenu.menu_id == menu_id, Submenu.id == submenu_id)) \
            .group_by(Submenu.id)
        if result.first() is None:
            return None
        return self._get_dict(*result.first())

    def get_elems(self, menu_id: int):
        result = self._connect.query(Submenu, func.count(Dish.id)) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .filter(Submenu.menu_id == menu_id) \
            .group_by(Submenu.id)
        if result.first() is None:
            return []
        return self._serializer(result)

    def _get_dict(self,first, second ):
        return {
            'id': str(first.id),
            'title': first.title,
            'description': first.description,
            'dishes_count': second
        }

    def _serializer(self, elements):
        result_list = []
        for element in elements:
            result_list.append(self._get_dict(*element))
        return result_list

    def create(self, instance: Submenu):
        self._connect.add(instance)
        try:
            self._connect.commit()
        except IntegrityError:
            return None
        return instance

    def delete(self, menu_id: int, submenu_id: int) -> bool:
        result = self._connect.query(Submenu).filter(and_(Submenu.menu_id == menu_id, Submenu.id == submenu_id )).delete()
        if result:
            self._connect.commit()
        return bool(result)


    def update(self, menu_id: int, submenu_id: int, fields: dict) -> Menu | None:
        result = self._connect.query(Submenu).filter(and_(Submenu.menu_id == menu_id, Submenu.id == submenu_id ))
        if result.first():
            result.update(fields)
            self._connect.commit()
            return self.get_elem(menu_id, submenu_id)

class DishSession(DBsessionSingleton):

    @classmethod
    def get_connect(cls):
        return cls()

    def get_elem(self, menu_id: int, submenu_id: int, dish_id: int):
        result = self._connect.query(Dish)\
            .filter(and_(Dish.submenu_id == submenu_id, Dish.id == dish_id))
        if result.first() is None:
            return None
        return self._get_dict(result.first())

    def get_elems(self, menu_id: int, submenu_id: int):
        result = self._connect.query(Dish) \
            .filter(Dish.submenu_id == submenu_id)
        if result.first() is None:
            return []
        return self._serializer(result)

    def _get_dict(self, first):
        return {
            'id': str(first.id),
            'title': first.title,
            'description': first.description,
            'price': str(first.price)
        }

    def _serializer(self, elements):
        result_list = []
        for element in elements:
            result_list.append(self._get_dict(element))
        return result_list

    def create(self, instance: Dish):
        self._connect.add(instance)
        try:
            self._connect.commit()
        except IntegrityError:
            return None
        return instance

    def delete(self, menu_id: int, submenu_id: int, dish_id: int)-> bool:
        result = self._connect.query(Dish).filter(
            and_(Dish.submenu_id == submenu_id, Dish.id == dish_id)).delete()
        if result:
            self._connect.commit()
        return bool(result)

    def update(self, menu_id: int, submenu_id: int, dish_id: int, fields: dict) -> Menu | None:
        result = self._connect.query(Dish).filter(and_(Dish.submenu_id == submenu_id, Dish.id == dish_id))
        if result.first():
            result.update(fields)
            self._connect.commit()
            return self._get_dict(result.first())

a = DishSession.get_connect()
l = Dish(
    title='BANANA1',
    description='title',
    submenu_id=123,
    price=11.233
)
# l1 = {
#     'title': 'OJFFFFFFFF'
# }
print(a.delete(1, 2, 2))
#