from menu.models import engine, Menu, Submenu, Dish
from sqlalchemy import insert, select, func, distinct
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
    key_list = ['id', 'title', 'descrition', 'submenus_count', "dishes_count"]

    @classmethod
    def get_connect(cls):
        return cls()

    def create(self, *args, **kwargs):
        return self._connect.execute(*args, **kwargs)

    def get_elem(self, id: int = 0):
        result = self._connect.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)) \
            .outerjoin(Submenu, Menu.id == Submenu.menu_id) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .filter(Menu.id == id) \
            .group_by(Menu.id)
        print(result)
        if result.first() is None:
            return {}
        return self._get_dict(result[0])

    def get_elems(self):
        result = self._connect.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)) \
            .outerjoin(Submenu, Menu.id == Submenu.menu_id) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id) \
            .group_by(Menu.id)
        return self._serializer(result)

    def _serializer(self, elements):
        result_list = []
        for element in elements:
            result_list.append(self._get_dict(element))
        return result_list

    def _get_dict(self, element):
        first, second, thread = element
        return dict(zip(
            self.key_list,
            [first.id, first.title, first.description, second, thread]
        ))

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



    @property
    def connect(self):
        return self._connect



a = MenuSession.get_connect()
print(a.update(18, {
    'description': None
}))