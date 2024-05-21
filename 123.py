from docx import Document
import os
contract_filename = ''
petition_filename = ''
context = {}
context['name_latin'] = 'Akgamov Agajan'
for file in os.listdir(f'drivers/{context["name_latin"]}'):
    if file.endswith(f'{context["name_latin"]}.docx'):
        doc_contract = Document(f'drivers/{context["name_latin"]}/{file}')
    if file.endswith(f'{context["name_latin"].split(" ")[0].upper()}.docx'):
        doc_petition = Document(f'drivers/{context["name_latin"]}/{file}')
context['name_cyrill'] = doc_contract.tables[1].column_cells(2)[0].text.split('\n')[1]
context['birth_date'] = doc_petition.tables[1].column_cells(0)[2].text.split('\n')[1]
context['passport_number'] = doc_petition.tables[1].column_cells(0)[3].text.split('\n')[1]
context['passport_given'] = doc_petition.tables[1].column_cells(2)[3].text.split('\n')[1].split('-')[0]
context['passport_ends'] = doc_petition.tables[1].column_cells(2)[3].text.split('\n')[1].split('-')[1]
print(context)
