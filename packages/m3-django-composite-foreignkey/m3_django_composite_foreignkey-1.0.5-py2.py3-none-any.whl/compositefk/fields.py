import collections
import logging
import operator
from collections import (
    OrderedDict,
)
from dataclasses import (
    dataclass,
)
from functools import (
    reduce,
    wraps,
)
from typing import (
    List,
)

from compositefk.related_descriptors import (
    CompositeForwardManyToOneDescriptor,
)
from django.core import (
    checks,
)
from django.core.exceptions import (
    FieldDoesNotExist,
)
from django.db.models import (
    DateField,
    FilteredRelation,
    Q,
)
from django.db.models.deletion import (
    Collector,
)
from django.db.models.fields.related import (
    ForeignObject,
)
from django.db.models.fields.related_descriptors import (
    ReverseOneToOneDescriptor,
)
from django.db.models.sql.where import (
    AND,
    WhereNode,
)
from django.utils.translation import (
    gettext_lazy as _,
)


logger = logging.getLogger(__name__)


class CompositeForeignKey(ForeignObject):
    requires_unique_target = False

    def __init__(self, to, **kwargs):
        """
        create the ForeignObject, but use the to_fields as a dict which will later used as form_fields and to_fields
        """
        to_fields = kwargs["to_fields"]
        self.null_if_equal = kwargs.pop("null_if_equal", [])
        nullable_fields = kwargs.pop("nullable_fields", {})
        if not isinstance(nullable_fields, dict):
            nullable_fields = {v: None for v in nullable_fields}
        self.nullable_fields = nullable_fields

        # a list of tuple : (fieldnaem, value) . if fielname = value, then the field react as if fieldnaem_id = None
        self._raw_fields = self.compute_to_fields(to_fields)
        # hiro nakamura should have said «very bad guy. you are vilain»
        if "on_delete" in kwargs:
            kwargs["on_delete"] = self.override_on_delete(kwargs["on_delete"])

        kwargs["to_fields"], kwargs["from_fields"] = zip(*(
            (k, v.value)
            for k, v in self._raw_fields.items()
            if v.is_local_field
        ))
        super(CompositeForeignKey, self).__init__(to, **kwargs)

    def override_on_delete(self, original):

        @wraps(original)
        def wrapper(collector, field, sub_objs, using):
            res = original(collector, field, sub_objs, using)
            # we make something nasty : we update the collector to
            # skip the local field which does not have a dbcolumn
            try:
                del collector.field_updates[self.model][(self, None)]
            except KeyError:
                pass
            return res

        wrapper._original_fn = original

        return wrapper

    def check(self, **kwargs):
        errors = super(CompositeForeignKey, self).check(**kwargs)
        errors.extend(self._check_null_with_nullifequal())
        errors.extend(self._check_nullifequal_fields_exists())
        errors.extend(self._check_to_fields_local_valide())
        errors.extend(self._check_to_fields_remote_valide())
        errors.extend(self._check_recursion_field_dependecy())
        errors.extend(self._check_bad_order_fields())
        return errors

    def _check_bad_order_fields(self):
        res = []
        try:
            dependents = list(self.local_related_fields)
        except FieldDoesNotExist:
            return []  # the errors shall be raised befor by _check_recursion_field_dependecy

        for field in self.model._meta.get_fields():
            try:
                dependents.remove(field)
            except ValueError:
                pass
            if field == self:
                if dependents:
                    # we met the current fields, but all dependent fields is not
                    # passed befor : we will have a problem in the init of some objects
                    # where the rest of dependents fields will override the
                    # values set by the current one (see Model.__init__)
                    res.append(
                        checks.Error(
                            "the field %s depend on the fields %s which is defined after. define them befor %s" %
                            (self.name, ",".join(f.name for f in dependents), self.name),
                            hint=None,
                            obj=self,
                            id='compositefk.E006',
                        ))
                break
        return res

    def _check_recursion_field_dependecy(self):
        res = []
        for local_field in self._raw_fields.values():
            try:
                f = self.model._meta.get_field(local_field.value)
                if isinstance(f, CompositeForeignKey):
                    res.append(
                        checks.Error(
                            "the field %s depend on the field %s which is another CompositeForeignKey" %
                            (self.name, local_field),
                            hint=None,
                            obj=self,
                            id='compositefk.E005',
                        )
                    )
            except FieldDoesNotExist:
                pass  # _check_to_fields_local_valide already raise errors for this
        return res

    def _check_to_fields_local_valide(self):
        res = []
        for local_field in self._raw_fields.values():
            if isinstance(local_field, LocalFieldValue):
                try:
                    self.model._meta.get_field(local_field.value)
                except FieldDoesNotExist:
                    res.append(
                        checks.Error(
                            "the field %s does not exists on the model %s" % (local_field, self.model),
                            hint=None,
                            obj=self,
                            id='compositefk.E003',
                        )
                    )
        return res

    def _check_to_fields_remote_valide(self):
        res = []
        for remote_field in self._raw_fields.keys():
            try:
                self.related_model._meta.get_field(remote_field)
            except FieldDoesNotExist:
                res.append(
                    checks.Error(
                        "the field %s does not exists on the model %s" % (remote_field, self.model),
                        hint=None,
                        obj=self,
                        id='compositefk.E004',
                    )
                )
        return res

    def _check_null_with_nullifequal(self):
        if self.null_if_equal and not self.null:
            return [
                checks.Error(
                    "you must set null=True to field %s.%s if null_if_equal is given" %
                    (self.model.__class__.__name__, self.name),
                    hint=None,
                    obj=self,
                    id='compositefk.E001',
                )
            ]
        return []

    def _check_nullifequal_fields_exists(self):
        res = []
        for field_name, value in self.null_if_equal:
            try:
                self.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                res.append(
                    checks.Error(
                        "the field %s does not exists on the model %s" % (field_name, self.model),
                        hint=None,
                        obj=self,
                        id='compositefk.E002',
                    )
                )
        return res

    def deconstruct(self):
        name, path, args, kwargs = super(CompositeForeignKey, self).deconstruct()
        del kwargs["from_fields"]
        if "on_delete" in kwargs:
            kwargs["on_delete"] = kwargs["on_delete"]._original_fn
        kwargs["to_fields"] = self._raw_fields
        kwargs["null_if_equal"] = self.null_if_equal
        return name, path, args, kwargs

    def get_extra_descriptor_filter(self, instance):
        return {
            k: v.value for k, v in self._raw_fields.items()
            if isinstance(v, RawFieldValue)
        }

    def get_extra_restriction(self, where_class, alias, related_alias):
        constraint = WhereNode(connector=AND)
        for remote, local in self._raw_fields.items():
            lookup = local.get_lookup(self, self.related_model._meta.get_field(remote), alias)
            if lookup:
                constraint.add(lookup, AND)
        if constraint.children:
            return constraint
        else:
            return None

    def compute_to_fields(self, to_fields):
        """
        compute the to_fields parameterse to make it uniformly a dict of CompositePart
        :param set[unicode]|dict[unicode, unicode] to_fields: the list/dict of fields to match
        :return: the well formated to_field containing only subclasses of CompositePart
        :rtype: dict[str, CompositePart]
        """
        # for problem in trim_join, we must try to give the fields in a consistent order with others models...
        # see #26515 at  https://code.djangoproject.com/ticket/26515

        return OrderedDict(
            (k, (v if isinstance(v, CompositePart) else LocalFieldValue(v)))
            for k, v in (to_fields.items() if isinstance(to_fields, dict) else zip(to_fields, to_fields))
        )

    def db_type(self, connection):
        # A CompositeForeignKey don't have a column in the database
        # so return None.
        return None

    def db_parameters(self, connection):
        return {"type": None, "check": None}

    def contribute_to_class(self, cls, name, **kwargs):
        super(ForeignObject, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, CompositeForwardManyToOneDescriptor(self))

    def get_instance_value_for_fields(self, instance, fields):
        # we override this method to provide the feathur of converting
        # some special values of teh composite local fields into a
        # None pointing field.
        # ie, if company is '   ' and it mean that the current field
        # point to nothing (as if it was None) => we transform this
        # '   ' into a true None to let django das as if it was None
        res = super(CompositeForeignKey, self).get_instance_value_for_fields(instance, fields)
        if self.null_if_equal:
            for field_name, exception_value in self.null_if_equal:
                val = getattr(instance, field_name)
                if val == exception_value:
                    # we have field_name that is equal to the bad value
                    # currently, it is enouth since the django implementation check at first
                    # if there is a None in the result
                    return (None,)
        return res

    def get_path_info(self, filtered_relation=None):
        """Дополняет атрибут filtered_relation класса PathInfo.

        При отсутствии filtered_relation Django убирает фильтрацию по полю,
        которое является частью CompositeForeignKey. В результате становится
        невозможной фильтрация по индексам, часть которых находится в
        CompositeForeignKey.

        Attrs:
            filtered_relation: Объект класса FilteredRelation
        """
        if not filtered_relation:
            filtered_relation = FilteredRelation(self.attname)
            filtered_relation.alias = self.remote_field.model._meta.db_table

        return super().get_path_info(filtered_relation)


class CompositeOneToOneField(CompositeForeignKey):
    # Field flags
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = True

    related_accessor_class = ReverseOneToOneDescriptor

    description = _("One-to-one relationship")

    def __init__(self, to, **kwargs):
        kwargs['unique'] = True
        super(CompositeOneToOneField, self).__init__(to, **kwargs)
        self.remote_field.multiple = False

    def deconstruct(self):
        name, path, args, kwargs = super(CompositeOneToOneField, self).deconstruct()
        if "unique" in kwargs:
            del kwargs['unique']
        return name, path, args, kwargs


class CompositePart(object):
    is_local_field = True

    def __init__(self, value):
        self.value = value

    def deconstruct(self):
        module_name = self.__module__
        name = self.__class__.__name__
        return (
            '%s.%s' % (module_name, name),
            (self.value,),
            {}
        )

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.value == other.value

    def get_lookup(self, main_field, for_remote, alias):
        """
        create a fake field for the lookup capability
        :param CompositeForeignKey main_field: the local fk
        :param Field for_remote: the remote field to match
        :return:
        """


class RawFieldValue(CompositePart):
    """
    represent a raw value for  a field.
    """
    is_local_field = False

    def get_lookup(self, main_field, for_remote, alias):
        """
        create a fake field for the lookup capability
        :param CompositeForeignKey main_field: the local fk
        :param Field for_remote: the remote field to match
        :return:
        """
        lookup_class = for_remote.get_lookup("exact")
        return lookup_class(for_remote.get_col(alias), self.value)


class FunctionBasedFieldValue(RawFieldValue):
    def __init__(self, func):
        self._func = func

    def deconstruct(self):
        module_name = self.__module__
        name = self.__class__.__name__
        return (
            '%s.%s' % (module_name, name),
            (self._func,),
            {}
        )

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self._func == other._func

    @property
    def value(self):
        return self._func()

    @value.setter
    def value(self):
        pass


class LocalFieldValue(CompositePart):
    """
    implicitly used, represent the value of a local field
    """
    is_local_field = True


@dataclass
class CompositeRelatedField:
    """ Правило соответствия составного поля модели для уточняющей фильтрации
    зависимых записей при удалении основных записей.
    Например: Модель TaxesReestr(T) имеет составной ключ charge на модель InOutCharge(I) c отношением полей:
    T.charge_id = I.id  и  T.period_date = I.period_date.  Например если есть необходимость при удалении записей из модели I
    каскадно удалять записи из модели T с уточненной фильтрацией по полю period_date из I, следует в модели T определить
    поле атрибут collector_extra_filter_fields = [CompositeRelatedField(composite_field=charge, related_fields=['period_date'])]
    В related_fields указываются поля из модели Т, в которой определен составной ключ на модель I
    """
    slots = [
        'composite_field', 'related_fields'
    ]
    # ссылка на составное поле
    composite_field: CompositeForeignKey
    # список названий полей в связанной модели
    related_fields: List[str]


class CompositeFKCollector(Collector):
    """ Специальный коллектор для партицированных моделей для поддержки каскадного удаления """
    def related_objects(self, related_model, related_fields, objs):
        """
        Переопределяет правило создания фильтра для подтягивания записей,
        ссылающихся на партицированную модель


        Args:
            related_model: Модель связанного объекта, который собирается коллектором
            related_fields: Ссылочные поля модели связанного объекта
            objs: Объекты для которых собираются связанные объекты

        Returns:
            QuerySet с дополненной фильтрацей по составным FK
        """

        field_filters = []

        for related_field in related_fields:

            if isinstance(related_field, CompositeForeignKey):
                deleted_model_pk_name = related_field.related_model._meta.pk.name
                from_field_index = related_field.to_fields.index(deleted_model_pk_name)
                field_name = related_field.from_fields[from_field_index]
                field_filters.append(Q(**{'%s__in' % field_name: [obj.pk for obj in objs]}))
                self._extend_conditions(related_model, objs, field_filters)
            else:
                field_name = related_field.name
                field_filters.append(Q(**{'%s__in' % field_name: objs}))

            detail_filter_fields = getattr(related_model, 'detail_filter_fields', None)
            detail_filter_fields = detail_filter_fields() if detail_filter_fields else {}
            # добавление уточняющей фильтрации (для присоединяемых таблиц или join в values)
            for field_name, value in detail_filter_fields.items():
                if isinstance(value, collections.Callable):
                    value = value()

                field_filters.append(Q(**{field_name: value}))

        predicate = reduce(operator.and_, field_filters)

        return related_model._base_manager.using(self.using).filter(predicate)

    @staticmethod
    def _extend_conditions(related_model, deleted_records, field_filters):
        """
        Дополнение уточняющей фильтрацией связанной внешней модели
        Args:
            related_model: связанная с удаляемыми данными модель
            deleted_records: удаляемые данные
            field_filters: дополняемый queryset фильтр для связанной модели
        """
        collector_extra_filter_fields = getattr(related_model, 'collector_extra_filter_fields', [])
        for collector_extra_filter_field in collector_extra_filter_fields:
            reverse_related_fields = related_model._meta.get_field(
                collector_extra_filter_field.composite_field.attname
            ).reverse_related_fields
            # формирование списка соотношений поля удяляемых записей и поля зависимых записей
            fields = [
                (parent_field, related_field)
                for parent_field, related_field in reverse_related_fields
                if related_field.attname in collector_extra_filter_field.related_fields
            ]
            for parent_field, related_field in fields:
                parent_values = {getattr(obj, parent_field.attname) for obj in deleted_records}
                if isinstance(parent_field, DateField):
                    # Для поля с типом Дата вычисляется диапазон дат из списка удаляемых объектов objs
                    # FIXME Скорей всего можно обойтись без диапазона для даты, используя простое условие IN
                    min_date = min(parent_values)
                    max_date = max(parent_values)
                    field_filters.append(
                        Q(**{
                            f'{related_field.attname}__gte': min_date,
                            f'{related_field.attname}__lte': max_date,
                        })
                    )
                else:
                    field_filters.append(Q(**{f'{related_field.attname}__in': parent_values}))
