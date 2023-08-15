
# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from django.urls import reverse

# Create your tests here.

# BASE SETTINGS

User = get_user_model()
c = Client()

class ChatTest(TestCase):
    
    def setUp(self):
        basic_user = User(username='basic', email='basic@basic.com')
        basic_user.set_password('basic')
        basic_user.save()
        self.basic_user = basic_user
        admin_user = User(username='admin', email='admin@admin.com')
        admin_user.set_password('admin')
        admin_user.save()
        self.admin_user = admin_user

    def test_chat_view_url(self):
        print('Тестирование модуля chat - Проверка urls.py для главной страницы [ ]')
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            get_request = self.client.get(reverse('index'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для главной страницы в urls.py, правильные значения: name="index"')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для стартовой страницы. Правильный путь - ""')
        print('Тестирование модуля chat - Проверка urls.py для главной страницы [x]')
        print('Тестирование модуля chat - Проверка шаблонов [ ]')
        template_names = []
        for t in get_request.templates:
            template_names.append(t.name)
        self.assertEqual('base.html' in template_names, True, msg='Нехватает шаблона base.html, для отображения основного контента')
        self.assertEqual('index.html' in template_names, True, msg='Нехватает шаблона index.html, для отображения основного контента')
        self.assertEqual('navbar.html' in template_names, True, msg='Нехватает шаблона navbar.html, для отображения основной навигационной панели')
        not_auth_login = 'login' in str(get_request.content)
        not_auth_register = 'registration' in str(get_request.content)
        self.assertEqual(not_auth_login, True, msg='Отсутствует ссылка на логин внутри навигационной панели. Используйте имя - login')
        self.assertEqual(not_auth_register, True, msg='Отсутствует ссылка на регистрацию внутри навигационной панели. Используйте имя - registration')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        get_request = self.client.get('')
        auth_account = 'profile' in str(get_request.content)
        auth_logout = 'logout' in str(get_request.content)
        self.assertEqual(auth_account, True, msg='Отсутствует ссылка на профиль для авторизированного пользователя внутри навигационной панели. Используйте имя - profile')
        self.assertEqual(auth_logout, True, msg='Отсутствует ссылка на логаут для авторизированного пользователя внутри навигационной панели. Используйте имя - logout')
        print('Тестирование модуля chat - Проверка шаблонов [x]')

    def test_chat_model(self):
        print('Тестирование модуля chat - Проверка модели [ ]')
        print('Тестирование модуля chat - Проверка импортирования модели для "Чата" [ ]')
        try:
            from .models import ChatModel
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - ChatModel')
        print('Тестирование модуля chat - Проверка импортирования модели для "Чата" [x]')
        from django.db.models import ForeignKey, TextField, DateTimeField
        flag_user = False
        try:
            user_field = ChatModel._meta.get_field("user")
            check_user_field = isinstance(user_field, ForeignKey)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле user для модели')
        flag_text = False
        try:
            text_field = ChatModel._meta.get_field("text")
            check_text_field = isinstance(text_field, TextField)
        except:
            flag_text = True
        self.assertTrue(not flag_text, msg='Отсутствует поле text для модели')
        flag_date = False
        try:
            date_field = ChatModel._meta.get_field("date")
            check_date_field = isinstance(date_field, DateTimeField)
        except:
            flag_date = True
        self.assertTrue(not flag_date, msg='Отсутствует поле date для модели')
        self.assertEqual(check_user_field, True, msg='Неправильно указан тип поля для user (используйте ForeignKey(User))')
        t = ChatModel._meta.get_field("user")
        auth_user = t.deconstruct()[-1].get('to', '')
        self.assertTrue(str(auth_user) == 'auth.user', msg='Не указана модель для пользователя User в поле user. Подробнее ищите в прошлых приложениях.')
        print('Тестирование модуля chat - Проверка модели [x]')
        self.assertEqual(check_text_field, True, msg='Неправильно указан тип поля для text (используйте TextField())')
        self.assertEqual(check_date_field, True, msg='Неправильно указан тип поля для date (используйте DateTimeField(auto_now_add=True))')

    def test_chat_form_and_context(self):
        print('Тестирование модуля chat - Проверка контекста в шаблоне [ ]')
        print('Тестирование модуля chat - Проверка формы [ ]')
        get_request = self.client.get('')
        error_msg = None
        try:
            get_request.context['form']
        except KeyError as k:
            error_msg = type(k)
        self.assertNotEqual(error_msg, KeyError, msg='Ошибка при получении контекста формы на главной странице, используйте имя - form, для контекста')
        input_content = 'type="submit"' in str(get_request.content)
        text_content = 'textarea' in str(get_request.content)
        action_content = 'action="/send/"' in str(get_request.content)
        self.assertEqual(text_content, True, msg='В шаблоне формы отсутствует поле для ввода текста (textarea). Для создания этого тега необходимо использовать виджет для CharField.')
        self.assertEqual(input_content, True, msg='В шаблоне формы отсутствует кнопка подтверждения ввода')
        self.assertEqual(action_content, True, msg='В шаблоне формы отсутствует или неправильно введен адрес для отправления запроса при обработке отправки сообщения. Используйте - /send/')
        print('Тестирование модуля chat - Проверка контекста в шаблоне [x]')

    def test_chat_send_message(self):
        from django.urls import reverse
        from .models import ChatModel
        print('Тестирование модуля chat - Проверка urls.py для отправления сообщений [ ]')
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            get_request = self.client.get(reverse('send-message'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для главной страницы в urls.py, правильные значения: name="send-message"')
        print('Тестирование модуля chat - Проверка urls.py для отправления сообщений [x]')
        print('Тестирование модуля chat - Проверка создания и чтения записей [ ]')
        get_request = self.client.get('/send/')
        self.assertRedirects(get_request, '/login/?next=/send/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе не авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        post_request = self.client.post('/send/')
        self.assertRedirects(post_request, '/login/?next=/send/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе не авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        login_user = self.client.login(username='basic', password='basic')
        get_request_auth = self.client.get('/send/')
        from django.urls import reverse
        self.assertRedirects(get_request_auth, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        post_request_auth_no_data = self.client.post('/send/', {})
        self.assertRedirects(post_request_auth_no_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе авторизированного пользователя на адрес /send/ без отправления данных. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        post_request_auth_with_data = self.client.post('/send/', {'text': 'test'})
        self.assertRedirects(post_request_auth_with_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе авторизированного пользователя на адрес /send/ с отправленными данными. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        obj = ChatModel.objects.all()
        self.assertEquals(len(obj), 1, msg='Ошибка создания записи в чат - Не удалось создать запись')
        from django.utils import timezone
        now = timezone.now()
        self.assertEquals(obj[0].user.username, 'basic', msg='Ошибка создания записи в чат - Неправильное сохранение в поле user')
        self.assertEquals(obj[0].text, 'test', msg='Ошибка создания записи в чат - Неправильное сохранение в поле text')
        self.assertEquals(obj[0].date.date(), now.date(), msg='Ошибка создания записи в чат - Неправильное сохранение в поле date')
        post_request_auth_with_data = self.client.post('/send/', {'text': 'test template render'})
        get_request_index = self.client.get(reverse('index'))
        text_content_with_data = 'test template render' in str(get_request_index.content)
        self.assertTrue(text_content_with_data, msg='Ошибка отображения записей в чат - Нет текста сообщения на главной странице')
        print('Тестирование модуля chat - Проверка создания и чтения записей [x]')
        print('Тестирование модуля chat - Все тесты пройдены успешно!')
