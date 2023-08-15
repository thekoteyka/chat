from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Create your tests here.

# BASE SETTINGS

User = get_user_model()
c = Client()

class ProfileTest(TestCase):
    
    def setUp(self):
        basic_user = User(username='basic', email='basic@basic.com')
        basic_user.set_password('basic')
        basic_user.save()
        self.basic_user = basic_user

    def test_account_model(self):
        from django.db.models import OneToOneField
        print('Тестирование модуля accounts - Модель для пользователя [ ]')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [ ]')
        try:
            from .models import UserProfile
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - UserProfile')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [x]')

        flag_user = False
        try:
            user_field = UserProfile._meta.get_field("profile")
            check_user_field = isinstance(user_field, OneToOneField)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле profile для модели')
        t = UserProfile._meta.get_field("profile")
        auth_user = t.deconstruct()[-1].get('to', '')
        self.assertTrue(str(auth_user) == 'auth.user', msg='Не указана модель для пользователя User в поле profile. Подробнее ищите в прошлых приложениях.')
        user_exists = User.objects.filter(username='basic').exists()
        self.assertEqual(user_exists, True, msg='Ошибка в базовых настройках (системное сообщение)')
        user_profile = UserProfile(profile=self.basic_user)
        user_profile.save()
        self.assertEqual(user_profile.profile, self.basic_user, msg='Проверьте настройки accounts/models')
        o2o_f = UserProfile._meta.get_field("profile")
        check_o2o_f = isinstance(o2o_f, OneToOneField)
        self.assertEqual(check_o2o_f, True, msg='Неправильно указан тип поля для profile (используйте OneToOneField())')
        print('Тестирование модуля accounts - Модель для пользователя [x]')

    def test_account_registration_form(self):
        from .models import UserProfile

        print('Тестирование модуля accounts - Проверка формы для регистрации[ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [ ]')
        try:
            from .forms import RegisterForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - RegisterForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = RegisterForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = RegisterForm.declared_fields.get('email', '')
        check_form_field_2 = isinstance(form_field_2, EmailField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для email (используйте CharField())')
        form_field_3 = RegisterForm.declared_fields.get('password', '')
        check_form_field_3 = isinstance(form_field_3, CharField)
        self.assertEqual(check_form_field_3, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для регистрации[x]')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('registration'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для registration в urls.py, правильные значения: name="registration"')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [x]')
        print('Тестирование модуля accounts - Создание пользователя [ ]')
        get_request = self.client.get('/registration/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для регистрации. Правильный путь - registration/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для регистрации. Правильно: templates/accounts/...')
        get_request_form = ('<form' in str(get_request.content), '</form>' in str(get_request.content))
        self.assertEqual(False in get_request_form, False, msg='Ошибка при GET запросе, не отображается форма на шаблоне')
        post_request = self.client.post('/registration/', {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        })
        created_user = UserProfile.objects.filter(profile__username='test')
        self.assertEqual(len(created_user), 1, msg='Ошибка при создании UserProfile')
        created_user = created_user[0]
        self.assertTrue(not created_user.profile.is_staff, msg='Для созданного пользователя необходимо добавить, что он не является сотрудником (staff = False)')
        self.assertEqual(created_user.profile.username, 'test', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(created_user.profile.email, 'test@test.com', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешной регистрации пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Создание пользователя [x]')

    def test_account_login_form(self):
        print('Тестирование модуля accounts - Проверка формы для логина [ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [ ]')
        try:
            from .forms import LoginForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - LoginForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = LoginForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = LoginForm.declared_fields.get('password', '')
        check_form_field_2 = isinstance(form_field_2, CharField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для логина [x]')
        print('Тестирование модуля accounts - Проверка urls.py для логина [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('login'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для login в urls.py, правильные значения: name="login"')
        print('Тестирование модуля accounts - Проверка urls.py для логина [x]')
        print('Тестирование модуля accounts - Логин пользователя [ ]')
        get_request = self.client.get('/login/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для логина. Правильный путь - login/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для логина. Правильно: templates/accounts/...')

        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')

        post_request = self.client.post('/login/', {
            'username': 'not exists',
            'password': 'not exists',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при не успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логин пользователя [x]')

    def test_account_logout_form(self):
        print('Тестирование модуля accounts - Проверка urls.py для логаута [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('logout'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для logout в urls.py, правильные значения: name="logout"')
        print('Тестирование модуля accounts - Проверка urls.py для логаута [x]')
        print('Тестирование модуля accounts - Логаут пользователя [ ]')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        sess_before = len(self.client.session.items())
        get_request = self.client.get('/logout/')
        sess_after = len(self.client.session.items())
        self.assertEquals(sess_before > sess_after and not sess_after, True, msg='Ошибка при логауте пользователя')

        self.assertEqual(get_request.status_code, 302, msg='Ошибка при разлогине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логаут пользователя [x]')

    def test_account_profile_view(self):
        print('Тестирование модуля accounts - Проверка urls.py для профиля [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('profile'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для profile в urls.py, правильные значения: name="profile"')
        print('Тестирование модуля accounts - Проверка urls.py для профиля [x]')
        print('Тестирование модуля accounts - Аутентификация [ ]')
        get_request = self.client.get('/profile/')
        self.assertEqual(get_request.status_code, 302, msg='Ошибка при заходе на страницу профиля без логина пользователя')
        self.assertEqual(get_request.url, '/login/?next=/profile/', msg='Ошибка перенаправления неавторизированного пользователя в приложении, используйте ссылку на - /login/')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        get_request_auth = self.client.get('/profile/')
        self.assertEqual(get_request_auth.status_code, 200, msg='Ошибка захода на страницу профиля с авторизированным логином пользователя')
        self.assertEqual(get_request_auth.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для профиля. Правильно: templates/accounts/...')
        error_msg = None
        try:
            get_request_auth.context['profile']
        except KeyError as k:
            error_msg = type(k)
        self.assertNotEqual(error_msg, KeyError, msg='Ошибка при получении контекста в профиле, используйте имя - profile, для контекста')
        print('Тестирование модуля accounts - Аутентификация [x]')

    def test_account_profile_display(self):
        print('Тестирование модуля accounts - Отображение данных в профиле [ ]')
        from chat.models import ChatModel
        objs = ChatModel.objects.bulk_create([ChatModel(user=self.basic_user, text=f'news - {i}') for i in range(113)])
        login_user = self.client.login(username='basic', password='basic')
        get_request_auth = self.client.get('/profile/')
        input_content = '113' in str(get_request_auth.content)
        self.assertTrue(input_content == True, msg='Ошибка отображения количества сообщений из чата в профиле. Вы должны вывести сообщения принадлежащие только текущему пользователю.')
        print('Тестирование модуля accounts - Отображение данных в профиле [x]')
        print('Тестирование модуля accounts - Все тесты пройдены успешно!')
        


    def test_account_model(self):
        from django.db.models import OneToOneField
        print('Тестирование модуля accounts - Модель для пользователя [ ]')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [ ]')
        try:
            from .models import UserProfile
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - UserProfile')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [x]')

        flag_user = False
        try:
            user_field = UserProfile._meta.get_field("profile")
            check_user_field = isinstance(user_field, OneToOneField)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле profile для модели')
        t = UserProfile._meta.get_field("profile")
        auth_user = t.deconstruct()[-1].get('to', '')
        self.assertTrue(str(auth_user) == 'auth.user', msg='Не указана модель для пользователя User в поле profile. Подробнее ищите в прошлых приложениях.')
        user_exists = User.objects.filter(username='basic').exists()
        self.assertEqual(user_exists, True, msg='Ошибка в базовых настройках (системное сообщение)')
        user_profile = UserProfile(profile=self.basic_user)
        user_profile.save()
        self.assertEqual(user_profile.profile, self.basic_user, msg='Проверьте настройки accounts/models')
        o2o_f = UserProfile._meta.get_field("profile")
        check_o2o_f = isinstance(o2o_f, OneToOneField)
        self.assertEqual(check_o2o_f, True, msg='Неправильно указан тип поля для profile (используйте OneToOneField())')
        print('Тестирование модуля accounts - Модель для пользователя [x]')

    def test_account_registration_form(self):
        from .models import UserProfile

        print('Тестирование модуля accounts - Проверка формы для регистрации [ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [ ]')
        try:
            from .forms import RegisterForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - RegisterForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = RegisterForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = RegisterForm.declared_fields.get('email', '')
        check_form_field_2 = isinstance(form_field_2, EmailField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для email (используйте EmailField())')
        form_field_3 = RegisterForm.declared_fields.get('password', '')
        check_form_field_3 = isinstance(form_field_3, CharField)
        self.assertEqual(check_form_field_3, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для регистрации [x]')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('registration'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для registration в urls.py, правильные значения: name="registration"')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [x]')
        print('Тестирование модуля accounts - Создание пользователя [ ]')
        get_request = self.client.get('/registration/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для регистрации. Правильный путь - registration/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для регистрации. Правильно: templates/accounts/...')
        get_request_form = ('<form' in str(get_request.content), '</form>' in str(get_request.content))
        self.assertEqual(False in get_request_form, False, msg='Ошибка при GET запросе, не отображается форма на шаблоне')
        post_request = self.client.post('/registration/', {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        })
        created_user = UserProfile.objects.filter(profile__username='test')
        self.assertEqual(len(created_user), 1, msg='Ошибка при создании UserProfile')
        created_user = created_user[0]
        self.assertTrue(not created_user.profile.is_staff, msg='Для созданного пользователя необходимо добавить, что он не является сотрудником (staff = False)')
        self.assertEqual(created_user.profile.username, 'test', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(created_user.profile.email, 'test@test.com', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешной регистрации пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Создание пользователя [x]')

    def test_account_login_form(self):
        print('Тестирование модуля accounts - Проверка формы для логина [ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [ ]')
        try:
            from .forms import LoginForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - LoginForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = LoginForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = LoginForm.declared_fields.get('password', '')
        check_form_field_2 = isinstance(form_field_2, CharField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для логина [x]')
        print('Тестирование модуля accounts - Проверка urls.py для логина [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('login'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для login в urls.py, правильные значения: name="login"')
        print('Тестирование модуля accounts - Проверка urls.py для логина [x]')
        print('Тестирование модуля accounts - Логин пользователя [ ]')
        get_request = self.client.get('/login/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для логина. Правильный путь - login/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для логина. Правильно: templates/accounts/...')

        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')

        post_request = self.client.post('/login/', {
            'username': 'not exists',
            'password': 'not exists',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при не успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логин пользователя [x]')

    def test_account_logout_form(self):
        print('Тестирование модуля accounts - Проверка urls.py для логаута [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('logout'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для logout в urls.py, правильные значения: name="logout"')
        print('Тестирование модуля accounts - Проверка urls.py для логаута [x]')
        print('Тестирование модуля accounts - Логаут пользователя [ ]')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        sess_before = len(self.client.session.items())
        get_request = self.client.get('/logout/')
        sess_after = len(self.client.session.items())
        self.assertEquals(sess_before > sess_after and not sess_after, True, msg='Ошибка при логауте пользователя')

        self.assertEqual(get_request.status_code, 302, msg='Ошибка при разлогине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логаут пользователя [x]')

    def test_account_profile_view(self):
        print('Тестирование модуля accounts - Проверка urls.py для профиля [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('profile'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для profile в urls.py, правильные значения: name="profile"')
        print('Тестирование модуля accounts - Проверка urls.py для профиля [x]')
        print('Тестирование модуля accounts - Аутентификация [ ]')
        get_request = self.client.get('/profile/')
        self.assertEqual(get_request.status_code, 302, msg='Ошибка при заходе на страницу профиля без логина пользователя')
        self.assertEqual(get_request.url, '/login/?next=/profile/', msg='Ошибка перенаправления неавторизированного пользователя в приложении, используйте ссылку на - /login/')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        get_request_auth = self.client.get('/profile/')
        self.assertEqual(get_request_auth.status_code, 200, msg='Ошибка захода на страницу профиля с авторизированным логином пользователя')
        self.assertEqual(get_request_auth.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для профиля. Правильно: templates/accounts/...')
        error_msg = None
        try:
            get_request_auth.context['profile']
        except KeyError as k:
            error_msg = type(k)
        self.assertNotEqual(error_msg, KeyError, msg='Ошибка при получении контекста в профиле, используйте имя - profile, для контекста')
        print('Тестирование модуля accounts - Аутентификация [x]')
        print('Тестирование модуля accounts - ЗАВЕРШЕНО!')

