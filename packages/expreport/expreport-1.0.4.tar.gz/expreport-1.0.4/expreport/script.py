#%%
import os
import argparse
from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate




def datapath(path:str):
    """
    Constructs an absolute path to a file located in the 'data' directory 
    relative to the current script's location.

    Args:
        path (str): A relative path to a file or directory within the 'data' directory.

    Returns:
        str: An absolute path to the specified file or directory.
    """

    _ROOT = Path(__file__).parent
    return os.path.join(_ROOT,'data',path)

def name(context):
    """
    Construct a filename and other strings from context data.

    Returns a tuple of four strings: 
        - a filename with the structure name and date
        - the ministry name
        - the governorate name
        - the date

    Args:
        context (dict): A dictionary of strings obtained from a row in the data CSV.
    """
    first_part = context['p6'].replace('(','').replace(')','')
    gov = context['p2'].split('بولاية')[1] 
    second_part = 'بولاية' + gov
    ministry ='وزارة' + context['p2'].split('لوزارة')[1].split('بولاية')[0]
    date = context['p1'].replace('تونس في','').replace('/','-').strip()
    return f'{first_part.strip()} {second_part.strip()} .docx' , ministry.strip() , gov.strip(),date

def to_excel_data(context):
    """
    Construct a dictionary from context data for use in an Excel spreadsheet.

    The returned dictionary has the following keys:
        - structure: the structure name and governorate
        - gov: the governorate name
        - instance: the instance name
        - information: the information string
        - date: the date

    Args:
        context (dict): A dictionary of strings obtained from a row in the data CSV.

    Returns:
        dict: A dictionary of strings with the specified keys.
    """
    gov = context['p2'].split('بولاية')[1]
    date = context['p1'].replace('تونس في','').replace('/','-').strip()
    first_part = context['p6'].replace('(','').replace(')','')
    second_part = 'بولاية' + gov
    structure = f'{first_part.strip()} {second_part.strip()}'
    information = context['p12']
    instance = context['p13']

    return {'structure' : structure.strip() ,'gov' : gov , 'instance' : instance.strip() , 'information' : information , 'date' : date }

def generate_doc(template='data/template.docx',path='data/src.csv',out='out'):
    """
    Generate a set of documents from a CSV file, using a template for the document structure.

    Args:
        template (str): The path to the template file.
        path (str): The path to the CSV file containing the data.
        out (str): The path to the directory where the generated documents should be written.

    """
    data = pd.read_csv(path,encoding='cp1256',header=None)

    l_context = []
    for l in range(len(data)):

        item = data.iloc[l]

        context = {}
        for i,x in enumerate(item):
            if(i == 3):
                context["p" + str(i+1)] = 'رئاسة الحكومة'
            else:
                context["p" + str(i+1)] = x
        l_context.append(context)


    for i,c in enumerate(l_context):
        doc = DocxTemplate(template)
        doc.render(context=c,autoescape=True)
        n,ministry,gov,date = name(c)
        pathdir = os.path.join(out,date,ministry,gov)
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        doc.save(os.path.join(pathdir,f'{i}-{n}') )

def generate_excel(path='data/src.csv',out='data/out.xlsx'):
    """
    Generate an Excel file from a CSV file, with a separate sheet for each governorate.

    Args:
        path (str): The path to the CSV file containing the data.
        out (str): The path to the Excel file that should be written.

    """
    data = pd.read_csv(path,encoding='cp1256',header=None)

    columns = ['المؤسسة أو الهيكل','الولاية','المصلحة','الملاحظات','التاريخ']

    l_context = []
    for l in range(len(data)):

        item = data.iloc[l]

        context = {}
        for i,x in enumerate(item):
            context["p" + str(i+1)] = x

        l_context.append(context)
    re = {}
    for d in l_context:
        d = to_excel_data(d)
        re.setdefault(d['gov'],[]).append(d)

    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:

        workbook  = writer.book
        wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'vcenter'})


        for key in re.keys():
            data = pd.DataFrame(re[key])
            data.columns = columns
            data.to_excel(writer,key,index=False, startcol=1,startrow=2)

            worksheet = writer.sheets[key]
            worksheet.right_to_left()
            worksheet.set_column('B:B', 30, wrap_format)
            worksheet.set_column('C:C', 8, wrap_format)
            worksheet.set_column('D:D', 40, wrap_format)
            worksheet.set_column('E:E', 60, wrap_format)
            worksheet.set_column('F:F', 10, wrap_format)

def cli():
    """
    Command line interface for expreport.

    This function uses the argparse module to parse command line arguments and
    execute the expreport script.

    The following arguments are supported:

        --data: path of source data
        --template: path of template to generate document
        --out: path of exported document
        --excel: export excel file

    If the --excel flag is set, the generate_excel function is called. Otherwise,
    the generate_doc function is called.

    If any of the required files do not exist (i.e. the source data file, the
    template file, or the output directory), a TypeError is raised.
    """
    parser = argparse.ArgumentParser(
        prog ="export data to word document",
        description="Arguments for expreport",
        usage = "",
        allow_abbrev=True
    )

    parser.add_argument(
        "--data",
        type=str,
        help="path of source data"
    )

    parser.add_argument(
        "--template",
        type=str,
        help="path of template to generate document",
        default=datapath("template.docx")
    )

    parser.add_argument(
        "--out",
        type=str,
        help="path of exported document",
        default=""
    )


    parser.add_argument(
        "--excel",
        type=bool,
        help="export excel file",
        default=False
    )

    args = parser.parse_args()


    if not os.path.exists(args.data):
        raise TypeError('File source not found please check your params --data')
    
    if not os.path.exists(args.out):
        raise TypeError('Folder to export document not found please check your params --out')
    
    if not os.path.exists(args.template):
        raise TypeError('Template file not exist please check your params --template or dont use it at all')
    
    if args.excel:
        generate_excel(args.data,os.path.join(args.out,'out.xlsx'))
    else:
        generate_doc(args.template,args.data,args.out)

    print('Done')