import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

from workers.models import Worker, City_Choices
from certs.models import Cerificate


# ТОФК
class TOFK(models.Model):
    tofk_number = models.CharField(max_length=4, verbose_name='Номер ТОФК', unique=True)
    tofk_city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
    tofk_address = models.CharField(max_length=255, verbose_name='Адрес ТОФК', unique=True)

    def __str__(self):
        return "%s - %s" % (self.tofk_number, self.get_tofk_city_display())

    def clean(self):
        if not str(self.tofk_number).isdigit():
            raise ValidationError({'tofk_number': "ТОФК должен содержать только цифры!"})

    class Meta:
        ordering = ['tofk_number']
        verbose_name = 'ТОФК'
        verbose_name_plural = 'ТОФК'


# Данные получателя
class Subject(models.Model):
    help_text = models.TextField(verbose_name='ВНИМАНИЕ!', blank=True, default='Для подтягивания значений из '
                                                                               '"Работника" нажмите "Сохранить и '
                                                                               'продолжить"!\nДля изменения '
                                                                               'заблокированных полей измените '
                                                                               'данные работника!')
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, verbose_name='Работник')
    tofk_number = models.ForeignKey(TOFK, on_delete=models.PROTECT, verbose_name='Номер ТОФК')
    city_1 = models.CharField(max_length=200, verbose_name='Город', blank=True)
    passport_path = models.CharField(max_length=255, verbose_name='Путь до паспорта', blank=True, null=True)
    passport_series = models.CharField(max_length=4, verbose_name='Серия паспорта', validators=[MinLengthValidator(4)], blank=True, null=True)
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта', validators=[MinLengthValidator(6)], blank=True, null=True)
    passport_from = models.CharField(max_length=200, verbose_name='Кем выдан', blank=True, null=True)
    passport_from_date = models.DateField(verbose_name='Когда выдан', blank=True, null=True)
    passport_from_code = models.CharField(max_length=7, verbose_name='Код места выдачи', validators=[MinLengthValidator(6)], blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, verbose_name='Место рождения', blank=True, null=True)
    gender = models.CharField(max_length=6, verbose_name='Пол', blank=True, null=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', blank=True, null=True)
    first_name = models.CharField(max_length=200, verbose_name='Имя', blank=True, null=True)
    patronymic = models.CharField(max_length=200, verbose_name='Отчество', blank=True, null=True)
    inn = models.CharField(max_length=12, verbose_name='ИНН', validators=[MinLengthValidator(10)], blank=True, null=True)
    snils = models.CharField(max_length=14, verbose_name='СНИЛС', validators=[MinLengthValidator(11), MaxLengthValidator(14)], blank=True, null=True)
    job = models.CharField(max_length=200, verbose_name='Должность', blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name='Почта', blank=True, null=True, default='ikdomashenko@kkck.ru')
    city_2 = models.CharField(max_length=200, verbose_name='Населенный пункт', blank=True, null=True)
    document_name = models.CharField(max_length=200, verbose_name='Название документа', blank=True, null=True)
    document_date = models.DateField(verbose_name='Дата документа', blank=True, null=True)
    document_number = models.CharField(max_length=200, verbose_name='Номер документа', blank=True, null=True)
    document_path = models.CharField(max_length=255, verbose_name='Путь до документа', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.worker.last_name, self.worker.first_name, self.patronymic)

    def clean(self):
        if self.inn and not self.inn is None:
            if not str(self.inn).isdigit():
                raise ValidationError({'inn': "ИНН должен содержать только цифры!"})

        if self.snils and not self.snils is None:
            print(f'snils', self.snils)
            if not str(self.snils).isdigit():
                snils = str(self.snils).replace('-', '').replace(' ', '')
                self.snils = snils
                if not str(self.snils).isdigit():
                    raise ValidationError({'snils': "СНИЛС должен содержать только цифры!"})

        if self.passport_series and not self.passport_series is None:
            if not str(self.passport_series).isdigit():
                raise ValidationError({'passport_series': "Серия паспорта должна содержать только цифры!"})

        if self.passport_number and not self.passport_number is None:
            if not str(self.passport_number).isdigit():
                raise ValidationError({'passport_number': "Номер паспорта должен содержать только цифры!"})

        if self.passport_from_code and not self.passport_from_code is None:
            if not '-' in str(self.passport_from_code):
                raise ValidationError({'passport_from_code': "Код места выдачи паспорта должен содержать только цифры и"
                                                         " тире!"})

        if self.passport_from_code and not self.passport_from_code is None:
            if not str(self.passport_from_code).isdigit():
                passport_from_code = str(self.passport_from_code).replace('-', '')
                if not passport_from_code.isdigit():
                    raise ValidationError({'passport_from_code': "Код места выдачи паспорта должен содержать только цифры и"
                                                             " тире!"})

    class Meta:
        ordering = ['worker']
        verbose_name = 'Субъект'
        verbose_name_plural = 'Субъекты'


# Данные сотрудника
class Application(models.Model):
    Application_Type = (
        ('new', 'Новый'),
        ('reload', 'Перевыпуск'),
    )
    city = models.CharField(max_length=200, verbose_name='Город', blank=True)
    a_type = models.CharField(max_length=6, choices=Application_Type, default=Application_Type[0],
                              verbose_name='Тип запроса')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='Получатель')
    req_formed = models.BooleanField(default=False, verbose_name='Запрос сф-н')
    req_name = models.CharField(max_length=200, verbose_name='Имя файла запроса', blank=True, unique=True, help_text='Имя папки на носителе, созданной после генерации запроса')
    req_url = models.URLField(verbose_name='Ссылка на черновик запроса', blank=True, unique=True)
    req_code = models.CharField(max_length=10, verbose_name='Номер запроса', blank=True, unique=True)
    doc_requested = models.BooleanField(default=False, verbose_name='Выписка запрошена')
    doc_requested_data = models.DateField(verbose_name='Дата запроса', blank=True, null=True)
    doc_signed = models.BooleanField(default=False, verbose_name='Выписка подписана')
    doc_signed_data = models.DateField(verbose_name='Дата подписания', blank=True, null=True)
    doc_path = models.CharField(max_length=500, verbose_name='Путь до выписки', blank=True, null=True)
    ap_formed = models.BooleanField(default=False, verbose_name='Заявление сф-но')
    ap_sent = models.BooleanField(default=False, verbose_name='Заявление передано получателю')
    ap_sent_data = models.DateField(verbose_name='Дата передачи з-я', blank=True, null=True)
    ap_signed = models.BooleanField(default=False, verbose_name='Заявление подп-но')
    ap_path = models.CharField(max_length=500, verbose_name='Путь до заявления', blank=True, null=True)
    req_send = models.BooleanField(default=False, verbose_name='Запрос отпр-н')
    req_approved = models.BooleanField(default=False, verbose_name='Запрос одобрен')
    need_go = models.BooleanField(default=False, verbose_name='Сказано сходить для передачи документов')
    need_go_to = models.DateField(verbose_name='Сходить до', blank=True, null=True)
    cert_done = models.BooleanField(default=False, verbose_name='Серт. готов')
    need_go_2 = models.BooleanField(default=False, verbose_name='Сказано сходить для получения')
    need_go_to_2 = models.DateField(verbose_name='Уведомил сотрудника', blank=True, null=True)
    cert_get = models.BooleanField(default=False, verbose_name='Сер-т получен')
    certificate = models.ForeignKey(Cerificate, on_delete=models.PROTECT, verbose_name='Сертификат', blank=True, null=True)
    token_done = models.BooleanField(default=False, verbose_name='Токен готов')
    Token_Type = (
        ('etoken', 'Етокен'),
        ('rutoken', 'Рутокен'),
        ('req', 'Реестр'),
    )
    token_type = models.CharField(max_length=7, choices=Token_Type, default=Token_Type[0],
                                  verbose_name='Тип токена')
    token_sn = models.CharField(max_length=500, verbose_name='Серийный номер токена', blank=True, null=True)
    sign_done = models.BooleanField(default=False, verbose_name='ЭП уст-на')
    sign_1c_done = models.BooleanField(default=False, verbose_name='ЭП доб-на в 1С')
    certificate_done = models.BooleanField(default=False, verbose_name='✔', help_text='Заявление считается завершенным, если все этапы пройдены, включая установку на ПК, но без учета добавления в 1С')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True)
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        return '%s на "%s" от %s' % (self.get_a_type_display(), self.subject, datetime.date.strftime(self.created_at, '%d.%m.%Y'))

    def clean(self):
        if self.req_name != '' and self.req_formed == False:
            raise ValidationError({'req_formed': "Укажите признак формирования запроса в случае указания его имени!"})

        if self.req_url != '' and self.req_formed == False:
            raise ValidationError({'req_formed': "Укажите признак формирования запроса в случае указания ссылки на него!"})

        if self.req_code != '' and self.req_formed == False:
            raise ValidationError({'req_formed': "Укажите признак формирования запроса в случае указания кода запроса!"})

        if self.req_formed and self.req_name == '':
            raise ValidationError({'req_name': "Заполните имя файла запроса с носителя!"})

        if self.req_formed and self.req_url == '':
            raise ValidationError({'req_url': "Укажите ссылку на черновик запроса!"})

        if self.req_formed and self.req_code == '':
            raise ValidationError({'req_code': "Укажите код запроса!"})

        if self.a_type != "reload":
            if self.need_go and self.need_go_to is None:
                raise ValidationError({'need_go_to': "Заполните дату крайней подачи документов в ТОФК!"})

            if self.ap_formed and not self.req_formed:
                raise ValidationError({'req_formed': "Заявление уже сформировано!"})

            if self.ap_signed and not self.ap_formed:
                raise ValidationError({'ap_formed': "Заявление уже подписано!"})

            if self.req_send and not self.ap_signed:
                raise ValidationError({'ap_signed': "Запрос уже отправлен!"})

            if self.req_approved and not self.req_send:
                raise ValidationError({'ap_send': "Запрос уже одобрен!"})

            if self.need_go and not self.req_approved:
                raise ValidationError({'req_approved': "Уже сказано сходить!"})

            if self.cert_done and not self.need_go:
                raise ValidationError({'need_go': "Сертификат уже готов!"})

            if self.need_go_2 and not self.cert_done:
                raise ValidationError({'cert_done': "Сертификат уже получен!"})

            if self.cert_get and not self.need_go_2:
                raise ValidationError({'need_go_2': "Сертификат уже получен!"})

            if self.cert_get and self.token_done and not self.certificate:
                raise ValidationError({'certificate': "Укажите полученный сертификат!"})

            if self.certificate and not self.cert_get:
                raise ValidationError({'cert_get': "Сертификат уже указан!"})

            if self.token_done and not self.cert_get:
                raise ValidationError({'cert_get': "Токен уже был изготовлен!"})

            if self.sign_done and not self.token_done:
                raise ValidationError({'token_done': "ЭП уже была установлена сотруднику!"})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'

