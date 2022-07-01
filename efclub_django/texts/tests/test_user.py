import os
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'efclub_django.settings')
import django

django.setup()

from unittest import TestCase

from texts.models import SourceData, Statuses
from texts.services.user import DBIUser

with open('data/users.json', mode='r') as f:
    data = json.load(f)

data = [DBIUser.model(**value.get('fields')) for value in data if value.get('fields')]

test_user_exclude = (
    '212548351', '248315054', '237683447', '236479560', '225202295', '220929923', '224902483',
    '231483230', '226607696', '227879422', '224845395', '219652221', '233415652', '231376495',
    '229395950', '231874196', '232584792', '235668877', '211391054', '210897724', '210093085',
    '194882210', '196506331', '190738910', '205797921', '199560684', '199642798', '195695915',
    '190738921', '195865571', '192084356', '192102779', '192022862', '191890869', '191534149',
    '191977761', '191981452', '192034585', '191970980', '191307148', '194692857', '194692310',
    '192215750', '192130771', '192129375', '192275206', '192211102', '192186719', '192219995',
    '192116161', '212762563', '205053657', '219563502', '192164476', '199175158', '206041070',
    '192116523', '194688162', '192592632', '192589662', '192601552', '194696002', '194688125',
    '192620031', '194689304', '192531973', '192274036', '212265629', '192279415', '209479415',
    '192438842', '254375230', '192312840', '192562147', '211042616', '212433276', '192256634',
    '175213187', '190738914', '177656972', '192181259', '207138153', '206020135', '206149242',
    '210788630', '179086831', '206489098', '206222629', '208994293', '176235272', '176190241',
    '177824342', '177622522', '177678006', '176235456', '178561297', '177741603', '177691111',
    '177911375', '178085534', '178650986', '239285208', '239315039', '242865008', '237875240',
    '192292757', '225068797', '189005818', '244475931', '232790393', '195598271', '194879830',
    '189218027', '189060063', '194940195', '191427142', '190738917', '190637170', '189800267',
    '190780135', '190738916', '190738919', '190738907', '189240644', '192068119', '192054307',
    '192017503', '191349159', '190738920', '191199057', '213950282', '192043915', '188996909',
    '184666229', '184649922', '185568006', '189071827', '188996496', '189000307', '184690383',
    '178501165', '254866303', '192598972', '236952098', '176155194', '205867458', '237675027',
    '194846542', '239283146', '247921094', '214414886', '188996010', '242761762', '242569664',
    '227566383', '192036613', '206489916', '191196028', '255279007', '238517447', '246403420',
    '212549361', '237856267', '246534737', '241574115', '239320293', '239318977', '244622675',
    '241200312', '236921015', '220262462', '202798627', '213929605', '219602243', '220651881',
    '236181482', '235826552', '235692938', '236068870', '236940092', '236156392', '236149835',
    '235932898', '189280664', '189599623', '239306477', '238905173', '238648343', '239410494',
    '239288272', '189237956', '239302011', '232726034', '250745297', '251730725', '253593504',
    '255510011', '176247932', '199632769', '223652708', '238737823', '247832671', '238510228',
    '248309027', '223855178', '239281116', '177652291', '240678120', '235587002', '237801653',
    '237803558', '238407730', '237115242', '252192072', '242643886', '255224950', '255301156',
    '238494293', '247889881', '238720880', '239328592', '242816559', '240560991', '236295177',
    '237002782', '239318716', '239335177', '239376610', '245870207', '247763972', '248269099',
    '248704842', '249898651', '239290684', '241191213', '254335259', '255097271', '255296528',
    '248644004', '248753642', '248838794', '248926330', '249945167', '250763109')

test_user_update_club = [
    {"getcourse_id": "236479560", "phone": "+11111111111", "telegram_id": 116449537, "status": "entered"},
    {"getcourse_id": "177656972", "phone": "+79623603517", "telegram_id": 357437952, "status": "entered"},
    {"getcourse_id": "223", "phone": "+34617110421"},
    {"getcourse_id": "000000", "phone": "79106719973", "telegram_id": 290242664, "status": "entered"},
    {"getcourse_id": "224902483", "phone": "79853325125", "telegram_id": 156703135, "status": "entered"},
    {"getcourse_id": "231483230", "phone": "+79263960060", "telegram_id": 116130028, "status": "entered"},
    {"getcourse_id": "226607696", "phone": "7967127713111", "telegram_id": 972433920, "status": "entered"},
]


class TestDBIUser(TestCase):
    def setUp(self) -> None:
        DBIUser.model.objects.bulk_create(data)
        self.users = test_user_exclude
        self.test_user_update_club = test_user_update_club

    def test_get_list_users_for_exclude(self):
        exclude_users = DBIUser.get_list_users_for_exclude(self.users)
        print(exclude_users)
        self.assertEqual(exclude_users, (12345,))

    def test_get_users_by_telegram_id(self):
        user = DBIUser.get_users_by_telegram_id(290242664)
        self.assertEqual(user.phone, "79106719973")

    def test_get_user_by_phone(self):
        user = DBIUser.get_user_by_phone('79268199776')
        self.assertEqual(user.telegram_id, 325696676)

    def test_update_users_by_club(self):
        DBIUser.update_users(self.test_user_update_club, SourceData.club)
        user_by_phone = DBIUser.get_user_by_phone('1111111111')
        self.assertEqual(user_by_phone.telegram_id, 116449537)
        self.assertIn(user_by_phone.status, [Statuses.entered, Statuses.returned])
        user_by_telegram_id = DBIUser.get_users_by_telegram_id(290242664)
        self.assertEqual(user_by_telegram_id.getcourse_id, '000000')
        self.assertIn(user_by_telegram_id.status, [Statuses.entered, Statuses.returned])
        user_by_phone = DBIUser.get_user_by_phone('34617110421')
        self.assertEqual(user_by_phone.getcourse_id, '223')
        self.assertIn(user_by_phone.status, [Statuses.entered, Statuses.returned])

    def test_update_users_by_waiting_list(self):
        DBIUser.update_users(self.test_user_update_club, SourceData.waiting_list)
        user_by_phone = DBIUser.get_user_by_phone('7967127713111')
        self.assertEqual(user_by_phone.telegram_id, 972433920)
        self.assertEqual(user_by_phone.status, Statuses.waiting)
        user_by_telegram_id = DBIUser.get_users_by_telegram_id(290242664)
        self.assertEqual(user_by_telegram_id.getcourse_id, '000000')
        self.assertEqual(user_by_telegram_id.status, Statuses.waiting)
        user_by_phone = DBIUser.get_user_by_phone('34617110421')
        self.assertEqual(user_by_phone.getcourse_id, '223')
        self.assertEqual(user_by_phone.status, Statuses.waiting)

    # def test_update_users_from_club(self):
    #     self.fail()
    # #
    # def test_update_users_from_waiting_list(self):
    #     self.fail()

    def test_add_challenger(self):
        DBIUser.add_challenger(phone='1234512348', telegram_id=111111111)
        user_by_phone = DBIUser.get_user_by_phone('1234512348')
        self.assertEqual(user_by_phone.telegram_id, 111111111)
        self.assertEqual(user_by_phone.status, Statuses.challenger)
        DBIUser.add_challenger(phone='79645571500', telegram_id=25998401711)
        user_by_telegram_id = DBIUser.get_users_by_telegram_id(25998401711)
        self.assertEqual(user_by_telegram_id.phone, '79645571500')

    def test_exclude_user_by_getcourse_id(self):
        all = DBIUser.model.objects.filter(status__in=[Statuses.entered, Statuses.returned]).count()
        count = DBIUser.exclude_user_by_getcourse_id(['175213187', '237683447'])
        self.assertEqual(all, count + 2)
        user_by_phone = DBIUser.get_user_by_phone("79268199776")
        self.assertEqual(user_by_phone.status, Statuses.entered)
        user_by_phone = DBIUser.get_user_by_phone("79039778528")
        self.assertEqual(user_by_phone.status, Statuses.excluded)


    def test_delete_user_from_waiting_list_by_getcourse_id(self):
        DBIUser.delete_user_from_waiting_list_by_getcourse_id()
        # self.fail()
    #
    # def test_get_users_from_waiting_list(self):
    #     self.fail()
    #
    # def test_get_users_for_mailing_new_status(self):
    #     self.fail()
    #
    # def test_un_set_status_updated_except_members(self):
    #     self.fail()
    #
    # def test_get_members_for_mailing_new_status(self):
    #     self.fail()
    #
    # def test_un_set_status_updated_for_members(self):
    #     self.fail()
    #
    # def test_get_users_which_can_be_chat(self):
    #     self.fail()
    #
    # def test_add_privileged_status_by_telegram_id(self):
    #     self.fail()
    #
    # def test_got_invited(self):
    #     self.fail()

    def tearDown(self) -> None:
        pass
        DBIUser.model.objects.all().delete()
