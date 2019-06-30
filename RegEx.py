import csv
import re

pattern_string = '([А-Я][a-я]+)[,\s]*([А-Я][а-я]*)[,\s]*([А-Я][а-я]*)*,*([А-Яа-я]*),*' \
                 '([\sa-zА-Яа-я\s–]*),*([-\d\sа-я\.\(\)+]*),*([\.A-Za-z\d@]*)'
pattern_phone = '(\+7|8)[\s\(]*(\d{3})[\)\s-]*(\d{3})-*(\d{2})-*(\d{2}\s*)\(*(доб.)*\s*(\d*)\)*'


def open_phonebook_to_clean(file_path):
    with open(file_path) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        global headers
        headers = contacts_list.pop(0)
        strings_list = []
        for line in contacts_list:
            string = ','.join(line)
            strings_list.append(string)
    return strings_list


# TODO 1: выполните пункты 1-3 ДЗ


def clean_phonebook(file_path):
    contacts_dict = {}

    for string in open_phonebook_to_clean(file_path):
        contact = {}
        result_string = re.search(pattern_string, string)
        result_phone = re.sub(pattern_phone, r"+7(\2)\3-\4-\5\6\7", result_string.group(6))
        lastname = result_string.group(1)
        contact[headers[0]] = lastname
        contact[headers[1]] = result_string.group(2)
        contact[headers[2]] = result_string.group(3)
        contact[headers[3]] = result_string.group(4)
        contact[headers[4]] = result_string.group(5)
        contact[headers[5]] = result_phone
        contact[headers[6]] = result_string.group(7)

        if contacts_dict.get(lastname):
            for key, value in contacts_dict[lastname].items():
                if value == '':
                    contacts_dict[lastname][key] = contact[key]
        else:
            contacts_dict[lastname] = contact

    global contacts_list_cleaned
    contacts_list_cleaned = [headers, ]
    for key, value in contacts_dict.items():
        contacts_list_cleaned.append(value.values())
    return contacts_list_cleaned


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV


def write_phonebook_cleaned(file_path):
    with open(file_path, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_cleaned)


if __name__ == '__main__':
    clean_phonebook("phonebook_raw.csv")
    write_phonebook_cleaned("phonebook.csv")
