from datetime import datetime
# from typing import Any


class QueryConstructor:
    """
    "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "period": query_period,
            "period_description": 'Период для формирования запроса. Может состоять из одной или двух дат',

            "is_admin": stat_kwargs.get('is_admin', None),
            "is_admin_description": 'Является ли пользователь админом.'
                                    'Если является - в запросе опускается часть с id пользователя',

            "location": stat_kwargs.get('location', None),
            "location_description": 'location_id локации по которой выполняется запрос'
                                    'Если отсутствует или None - в запросе опускается часть с location_id',

            'act_number': None, '', int, str
            "act_number_description": 'Если отсутствует или None - в запросе опускается часть с location_id',
        }
    """

    # user_id: Any[str, int]
    # table_name: str
    # type_query: str
    # user_data_dict: Any[dict, None]
    # action: str
    # subject: str
    # conditions: Any[dict, None]
    # period: Any[dict, str, None]
    # is_admin: bool
    # location: Any[str, None]
    # act_number: Any[str, int, None]
    # query: Any[str, None]
    # part_period: list or None
    # main_part: Any[str, None]
    # part_user: Any[str, None]
    # part_location: Any[str, None]
    # part_act_number: Any[str, None]
    # date_start: Any[str, None]
    # date_stop: Any[str, None]

    def __init__(self, chat_id: str, table_name: str, **kwargs):
        self.exception = [None, 'all', 'not', ]

        self.user_id = chat_id
        self.table_name = table_name

        self.type_query = kwargs.get('type_query', None)
        self.user_data_dict = kwargs.get('user_data_dict', None)

        self.action = kwargs.get('action', None)
        self.subject = kwargs.get('user_data_dict', None)

        self.conditions = kwargs.get('conditions', None)
        self.period: dict = self.conditions.get('period', None)
        self.is_admin = self.conditions.get('is_admin', None)
        self.location = self.conditions.get('location', None)
        self.act_number = self.conditions.get('act_number', None)

        self.query = None

        self.part_period = None
        self.main_part = None
        self.part_user = None
        self.part_location = None
        self.part_act_number = None

        self.date_start = None
        self.date_stop = None

    async def prepare_data(self):

        self.action = await self.get_action_part()
        self.subject = await self.get_subject_part()

        self.main_part = await self.get_main_part()
        self.part_user = await self.get_part_user()
        self.part_period = await self.get_part_period()
        self.part_location = await self.get_part_location()
        self.part_act_number = await self.get_part_act_number()

        self.query = await self.get_query()
        return self.query

    async def get_action_part(self) -> str:
        self.action = 'SELECT'.upper()
        return self.action

    async def get_subject_part(self):

        if not self.subject:
            return '*'

    async def get_main_part(self) -> str:
        self.main_part = f'{self.action} {self.subject} FROM `{self.table_name}` '

        if self.conditions:
            self.main_part = f'{self.action} {self.subject} FROM `{self.table_name}` WHERE '

        return self.main_part

    async def get_part_act_number(self) -> str:
        if self.act_number == '':
            return f'(`act_number` = '' or `act_number` is NULL )'
        elif self.act_number:
            return f'`act_number` = {self.act_number} '
        else:
            return ''

    async def get_part_user(self) -> str:
        if self.is_admin:
            return ''

        return f"`user_id` = {self.user_id} "

    async def get_part_period(self) -> str:

        self.date_start, self.date_stop = await self.get_period()

        return f"`created_at` BETWEEN date('{self.date_start}') " \
               f"AND date('{self.date_stop}') "

    async def get_part_location(self) -> str:
        if not self.location:
            return ''

        return f'`location_id` = {self.location}'

    async def get_period(self):

        if isinstance(self.period, list):
            self.date_start, self.date_stop = await self.get_date_list()
            return self.date_start, self.date_stop

        if isinstance(self.period, dict):
            self.date_start, self.date_stop = await self.get_date_dict()
            return self.date_start, self.date_stop

        if isinstance(self.period, str):
            self.period = await self.format_data(self.period)
            return self.period, self.period

    async def get_date_list(self):
        self.date_start = self.period[0]
        self.date_stop = self.period[1]

        self.date_start = await self.format_data(self.date_start)
        self.date_stop = await self.format_data(self.date_stop)

        return self.date_start, self.date_stop

    async def get_date_dict(self):
        self.date_start = self.period.get('date_start', None)
        self.date_stop = self.period.get('date_stop', None)

        self.date_start = await self.format_data(self.date_start)
        self.date_stop = await self.format_data(self.date_stop)

        return self.date_start, self.date_stop

    @staticmethod
    async def format_data(date_item: str) -> str:
        """ Форматирование даты в формат даты БВ
        """

        return datetime.strptime(date_item, "%d.%m.%Y").strftime("%Y-%m-%d")

    async def get_query(self) -> str:
        conditions = [self.part_user, self.part_period, self.part_location, self.part_act_number]
        condition = ' AND '.join(cond for cond in conditions if cond)

        return self.main_part + condition
