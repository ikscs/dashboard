class ExternalDBRouter:
    """
    Роутер для маршрутизации запросов к внешним базам данных
    """
    def db_for_read(self, model, **hints):
        """
        Определяет базу данных для чтения
        """
        if hasattr(model, '_meta') and hasattr(model._meta, 'db_table'):
            table_name = model._meta.db_table.lower()
            if table_name.startswith('cp_'):
                return 'cp_db'
            elif table_name.startswith('mk_'):
                return 'mk_db'
            elif table_name.startswith('log_'):
                return 'log_db'
            elif table_name.startswith('cnt_'):
                return 'cnt_db'
            elif table_name.startswith('external_'):
                return 'external_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Определяет базу данных для записи
        """
        if hasattr(model, '_meta') and hasattr(model._meta, 'db_table'):
            table_name = model._meta.db_table.lower()
            if table_name.startswith('cp_'):
                return 'cp_db'
            elif table_name.startswith('mk_'):
                return 'mk_db'
            elif table_name.startswith('log_'):
                return 'log_db'
            elif table_name.startswith('cnt_'):
                return 'cnt_db'
            elif table_name.startswith('external_'):
                return 'external_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешает отношения между объектами
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Определяет, можно ли применять миграции к базе данных
        """
        if model_name:
            model_name = model_name.lower()
            if db == 'cp_db' and model_name.startswith('cp_'):
                return True
            elif db == 'mk_db' and model_name.startswith('mk_'):
                return True
            elif db == 'log_db' and model_name.startswith('log_'):
                return True
            elif db == 'cnt_db' and model_name.startswith('cnt_'):
                return True
            elif db == 'external_db' and model_name.startswith('external_'):
                return True
        return None 