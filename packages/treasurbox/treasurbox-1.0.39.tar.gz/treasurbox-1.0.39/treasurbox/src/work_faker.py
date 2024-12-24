#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-09-30 15:43:18
# @Author: Alan
# @File: work_faker.py
# @Describe: faker data

import datetime
import time
from faker import Factory, Faker
from fake_useragent import UserAgent
import numpy as np


fake = Faker(locale="zh_CN")


class FakerMaker:

    def username(self, count):
        """
        username
        """
        user_name = [fake.user_name() for i in range(count)]
        return user_name

    def password(self, count):
        """
        password
        """
        pass_word = [fake.password(special_chars=False) for i in range(count)]
        return pass_word

    def date_time(self, count=1):
        """
        random date time
        """
        my_list = []
        get_date = [fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=None) for i in range(count)]
        for i in get_date:
            get_datetime = i.strftime('%Y-%m-%d %X')
            my_list.append(get_datetime)
        return my_list

    def datetime_before_days(self, count):
        """
        the date before some days
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(days=count)).strftime("%Y-%m-%d %X")
        return f'the date before {count} day: {datebefore}'

    def datetime_before_hours(self, count):
        """
        the date before some hours
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(hours=count)).strftime("%Y-%m-%d %X")
        return f'the date before {count}h: {datebefore}'

    def datetime_before_minutes(self, count):
        """
        the date before some minutes
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(minutes=count)).strftime("%Y-%m-%d %X")
        return f'the date before {count}m: {datebefore}'

    def datetime_before_seconds(self, count):
        """
        the date before some second
        """
        datebefore = (datetime.datetime.now() -
                      datetime.timedelta(seconds=count)).strftime("%Y-%m-%d %X")
        return f'the date before {count}s: {datebefore}'

    def datetime_today(self):
        """daytime now like 2018-03-22 15:22:31
        """
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        my_today = time.strftime(ISOTIMEFORMAT, time.localtime())
        return f'daytime now: {my_today}'

    def date_before(self, count):
        """the date before some day"""
        my_datebefore = (datetime.date.today() +
                         datetime.timedelta(days=-count)).strftime('%Y-%m-%d')
        return f'the date before {count} day: {my_datebefore}'

    def date_today(self):
        """date today like 2018-03-22 """
        my_today = datetime.date.today()
        return f'date today: {my_today}'

    def ipv4(self, count):
        """
        ipv4 address
        """
        ip_addr = [fake.ipv4(network=False) for i in range(count)]
        return ip_addr

    def ipv6(self, count):
        """
        ipv6 address
        """
        ip_addr = [fake.ipv6(network=False) for i in range(count)]
        return ip_addr

    def url(self, count):
        """
        url
        """
        my_url = [fake.url() for i in range(count)]
        return my_url

    def mac(self, count):
        """
        mac address
        """
        my_mac = [fake.mac_address() for i in range(count)]
        return my_mac

    def email_addr(self, count=1):
        """
        email
        fake.safe_email()
        fake.company_email()
        fake.free_email()
        """
        if count > 1:
            email = [fake.free_email() for i in range(count)]
        else:
            email = fake.free_email()
        return email

    def phonenumber(self, count):
        """
        phone number
        """
        my_phone = [fake.phone_number() for i in range(count)]
        return my_phone

    def idcard(self, count):
        """
        id card
        """
        my_id = [fake.ssn(min_age=18, max_age=90) for i in range(count)]
        return my_id

    def en_name(self, count):
        """
        English Name
        """
        my_enname = [fake.romanized_name() for i in range(count)]
        return my_enname

    def cn_name(self, count):
        """
        Chinese Name include male and female
        fake.first_name_male()   # male name
        fake.name_male()  # female name
        """
        my_cnname = [fake.name() for i in range(count)]
        return my_cnname

    def random_int(self, count):
        """
        random int
        """
        my_int = [fake.pyint() for i in range(count)]
        return my_int

    def random_str(self, count):
        """
        random string
        fake.pystr(min_chars=None, max_chars=20): A random string of custom length
        """
        my_str = [fake.pystr() for i in range(count)]
        return my_str

    def postcode(self, count):
        """
        postcode
        """
        my_postcode = [fake.postcode() for i in range(count)]
        return my_postcode

    def addrss(self, count):
        """
        address
        """
        my_addr = [fake.address() for i in range(count)]
        return my_addr

    def iban(self, count):
        """
        iban
        """
        my_iban = [fake.iban() for i in range(count)]
        return my_iban

    def credit_card(self, count):
        """
        credit card
        """
        my_credit = [fake.credit_card_number() for i in range(count)]
        return my_credit

    def company(self, count):
        """
        company name
        """
        my_company = [fake.company() for i in range(count)]
        return my_company

    def sentences(self, count):
        """
        sentences
        """
        my_sentences = [fake.sentences(nb=3, ext_word_list=None)
                        for i in range(count)]
        return my_sentences

    def paragraph(self, count):
        """
        paragraph
        """
        my_paragraph = [fake.paragraph(
            nb_sentences=3, variable_nb_sentences=True, ext_word_list=None) for i in range(count)]
        return my_paragraph

    def paragraphs(self, count):
        """
        make up by some paragraph
        """
        my_paragraphs = [fake.paragraphs(
            nb=3, ext_word_list=None) for i in range(count)]
        return my_paragraphs

    def len_int(self, len, count):
        """
        len must be 8 or 13
        """
        my_randomint = [fake.ean(length=len) for i in range(count)]
        return my_randomint

    def time_stamp_second(self, count):
        """
        timestramp 8
        """
        my_timestamp = [fake.unix_time(
            end_datetime=None, start_datetime=None) for i in range(count)]
        return my_timestamp

    def time_stamp_millisecond(self):
        """
        timestramp 13
        """
        return str(round(time.time() * 1000))

    def money(self, count):
        """
        like money
        """
        ran = np.random.RandomState()
        return [round(ran.uniform(-0.1, 100.1), 2) for i in range(count)]

    def country(self, count):
        """
        country
        """
        my_country = [fake.country() for i in range(count)]
        return my_country

    def user_agent(self):
        """
        UserAgent
        """
        my_user_agent = UserAgent()
        return my_user_agent.random
