def make_it_beautiful(context:dict)->str:
    translate_dict = {'choice' : 'Тип документов',
                      'name_latin' : 'Имя латиницей',
                      'name_cyrill' : 'Имя кириллицей',
                      'birth_date' : 'Дата рождения',
                      'passport_number' : 'Номер паспорта',
                      'passport_given' : 'Дата выдачи паспорта',
                      'passport_ends' : 'Дата окончания паспорта',
                      'contract_begins' : 'Дата начала контракта',
                      'contract_ends' : 'Дата окончания контракта',
                      'registration_address' : 'Адрес регистрации',
                      'telephone' : 'Номер телефона',
                      }
    out_string = ''
    for key, value in context.items():
        out_string += f"<b>{translate_dict[key]}</b>: <i>{value}</i>\n"
    return out_string
