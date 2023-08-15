from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from chat.models import ChatModel
# Create your tests here.

# BASE SETTINGS

User = get_user_model()
c = Client()

class SubscribersTest(TestCase):
    
    def setUp(self):
        basic_user = User(username='basic', email='basic@basic.com')
        basic_user.set_password('basic')
        basic_user.save()
        self.basic_user = basic_user
        admin_user = User(username='admin', email='admin@admin.com')
        admin_user.set_password('admin')
        admin_user.save()
        self.admin_user = admin_user
        subs_user = User(username='subs', email='subs@subs.com')
        subs_user.set_password('subs')
        subs_user.save()
        self.subs_user = subs_user

    def test_subscribers_model_and_view(self):
        print('Тестирование модуля subscribers - Проверка модели [ ]')
        print('Тестирование модуля subscribers - Проверка импортирования модели для "Подписок" [ ]')
        try:
            from .models import SubscribeModel
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - SubscribeModel')
        print('Тестирование модуля subscribers - Проверка импортирования модели для "Подписок" [x]')
        from django.db.models import ForeignKey
        flag_user = False
        try:
            self_user_field = SubscribeModel._meta.get_field("self_user")
            check_self_user_field = isinstance(self_user_field, ForeignKey)
            other_user_field = SubscribeModel._meta.get_field("other_user")
            check_other_user_field = isinstance(other_user_field, ForeignKey)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле self_user или other_user для модели')
        # test db
        print('Тестирование модуля subscribers - Проверка полей в модели [ ]')
        from django.db.models import ForeignKey
        self_user_field = SubscribeModel._meta.get_field("self_user")
        other_user_field = SubscribeModel._meta.get_field("other_user")
        check_self_user_field = isinstance(self_user_field, ForeignKey)
        check_other_user_field = isinstance(other_user_field, ForeignKey)
        self.assertEqual(check_self_user_field, True, msg='Неправильно указан тип поля для self_user (используйте ForeignKey())')
        self.assertEqual(check_other_user_field, True, msg='Неправильно указан тип поля для other_user (используйте ForeignKey())')
        print('Тестирование модуля subscribers - Проверка полей в модели [x]')
        print('Тестирование модуля subscribers - Проверка модели [x]')
        
        print('Тестирование модуля subscribers - Проверка urls.py для страницы добавления в подписки [ ]')
        from django.urls.exceptions import NoReverseMatch
        from django.urls import reverse
        rev = False
        try:
            get_request = self.client.get(reverse('subscribe', args=(1,)))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для страницы добавления в подписки, правильные значения: name="subscribe"')
        print('Тестирование модуля subscribers - Проверка urls.py для страницы добавления в подписки [x]')
        
        print('Тестирование модуля subscribers - Проверка перенаправления [ ]')
        get_request = self.client.get('/subscribe/1/')
        self.assertRedirects(get_request, '/login/?next=/subscribe/1/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе не авторизированного пользователя на адрес /subscribe/1/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        post_request = self.client.post('/subscribe/1/')
        self.assertRedirects(post_request, '/login/?next=/subscribe/1/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе не авторизированного пользователя на адрес /subscribe/1/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        print('Тестирование модуля subscribers - Проверка перенаправления [x]')
        # test view
        print('Тестирование модуля subscribers - Проверка добавления пользователей в подписки [ ]')
        self.client.login(username='basic', password='basic')
        get_request_auth = self.client.get('/subscribe/1/')
        from django.urls import reverse
        self.assertRedirects(get_request_auth, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе авторизированного пользователя на адрес /subscribe/1/. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        post_request_auth_no_data = self.client.post('/subscribe/1/', {})
        self.assertRedirects(post_request_auth_no_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе авторизированного пользователя на адрес /subscribe/1/. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        chat_model_basic = ChatModel(user=self.basic_user, text='text for basic')
        chat_model_basic.save()
        chat_model_admin = ChatModel(user=self.admin_user, text='text for admin')
        chat_model_admin.save()
        post_request_auth_with_data = self.client.post(f'/subscribe/{self.admin_user.id}/')
        self.assertRedirects(post_request_auth_with_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе c переданными данными для авторизированного пользователя на адрес /subscribe/1/. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        model_data = SubscribeModel.objects.all()
        self.assertEqual(len(model_data), 1, msg='Ошибка при добавлении пользователя в подписчики. Не получилось добавить новую подписку.')
        # user self user
        add_self_to_subs = self.client.post(f'/subscribe/{self.basic_user.id}/')
        self.assertEqual(len(model_data), 1, msg='Ошибка при добавлении себя в подписчики. Нельзя добавлять себя в подписчики (друзья).')
        post_request_auth_with_data = self.client.post(f'/subscribe/{self.admin_user.id}/')
        self.assertEqual(len(model_data), 1, msg='Ошибка при добавлении пользователя в подписчики. Произошло множественное добавление одного и того же пользователя в подписки.')
        post_request_auth_with_data_2 = self.client.post(f'/subscribe/{self.subs_user.id}/')
        model_data = SubscribeModel.objects.all()
        self.assertEqual(len(model_data), 2, msg='Ошибка при добавлении множественных пользователей в подписчики. Не получилось добавить новую подписку.')
        get_request_accounts = self.client.get(reverse('profile'))
        text_content_with_data_admin = 'admin' in str(get_request_accounts.content)
        text_content_with_data_subs = 'subs' in str(get_request_accounts.content)
        self.assertTrue(text_content_with_data_admin and text_content_with_data_subs, msg='Ошибка в шаблоне внутри пользовательского кабинета, вы должны вывести имена всех пользователей, которые находятся в подписках')
        print('Тестирование модуля subscribers - Проверка добавления пользователей в подписки [x]')

    def test_subscribers_filter_1(self):
        print('Тестирование модуля subscribers - Проверка добавления фильтра для отображения определенных пользователей [ ]')
        self.client.login(username='basic', password='basic')
        chat_model_subs = ChatModel.objects.bulk_create([ChatModel(user=self.subs_user, text=f'text for subs {i}') for i in range(5)])
        get_request_index = self.client.get('?filter=3')  
        self.assertEqual(str(get_request_index.content).count('<mark>subs'), 5, msg='Ошибка в использовании фильтрации для отображения определенных пользователей')
        chat_model_admin = ChatModel.objects.bulk_create([ChatModel(user=self.admin_user, text=f'text for admin {i}') for i in range(15)])
        get_request_index = self.client.get('?filter=2')  
        self.assertEqual(str(get_request_index.content).count('<mark>admin'), 15, msg='Ошибка в использовании фильтрации для отображения определенных пользователей')
        print('Тестирование модуля subscribers - Проверка добавления фильтра для отображения определенных пользователей [x]')

    def test_subscribers_filter_2(self):
        print('Тестирование модуля subscribers - Проверка добавления фильтра для отображения только пользователей на которых есть подписка [ ]')
        self.client.login(username='basic', password='basic')
        chat_model_subs = ChatModel.objects.bulk_create([ChatModel(user=self.subs_user, text=f'text for subs {i}') for i in range(3)])
        chat_model_admin = ChatModel.objects.bulk_create([ChatModel(user=self.admin_user, text=f'text for admin {i}') for i in range(5)])
        post_request_auth_with_data = self.client.post(f'/subscribe/{self.subs_user.id}/')
        get_request_index = self.client.get('?sub=yes')  
        self.assertEqual(str(get_request_index.content).count('<mark>admin'), 0, msg='Ошибка в использовании фильтрации для отображения только пользователей на которых есть подписка.')
        self.assertEqual(str(get_request_index.content).count('<mark>subs'), 3, msg='Ошибка в использовании фильтрации для отображения только пользователей на которых есть подписка.')
        get_request_index = self.client.get('')
        self.assertEqual(str(get_request_index.content).count('<mark>admin'), 5, msg='Ошибка в использовании фильтрации для отображения только пользователей на которых есть подписка.')
        self.assertEqual(str(get_request_index.content).count('<mark>subs'), 3, msg='Ошибка в использовании фильтрации для отображения только пользователей на которых есть подписка.')
        print('Тестирование модуля subscribers - Проверка добавления фильтра для отображения только пользователей на которых есть подписка [x]')
        print('Тестирование модуля subscribers - Все тесты пройдены успешно!')

