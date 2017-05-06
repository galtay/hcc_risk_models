coef_files = [
    'C1209J2Y', 'C2110H2R', 'C2211L4P', # 2015 models
    'C2211L4P', 'C2110H2R',             # 2016 models
    'C2214O5P', 'C2110H2R',             # 2017 models
]


form_files = [
    'F1213H1Y', 'F2113J1R', 'F2213L2P', # 2015 models
    'F221690P', 'F211690R',             # 2016 models
    'F2217O1P', 'F2117H1R',             # 2017 models
 ]



coef_files = set(coef_files)
form_files = set(form_files)



base_path = '/folders/myfolders/sasuser.v94/cms_hcc_binary'
with open('unobfuscate_all.sas', 'w') as fp:
    fp.write('/* dump coefficient files to csv and sas7bdat */\n\n')
    for cf in coef_files:
        path = '{}/{}'.format(base_path, cf)
        line = 'filename inc "{}";'.format(path)
        fp.write(line+'\n')
        line = 'libname incoef "{}";'.format(base_path)
        fp.write(line+'\n')
        line = 'proc cimport data=incoef.{} infile=inc;'.format(cf)
        fp.write(line+'\n')
        fp.write('run;\n')

        line = 'proc export data=incoef.{}'.format(cf)
        fp.write(line+'\n')
        line = 'outfile="{}.csv"'.format(path)
        fp.write(line+'\n')
        fp.write('dbms=csv\n')
        fp.write('replace;\n')
        fp.write('run;\n')

        fp.write('\n')

    fp.write('/* dump format files to csv and sas7bdat */\n\n')
    for ff in form_files:
        path = '{}/{}'.format(base_path, ff)
        line = 'filename inf "{}";'.format(path)
        fp.write(line+'\n')

        line = 'libname cmshccfm "{}";'.format(base_path)
        fp.write(line+'\n')

        line = 'proc cimport library=cmshccfm infile=inf;'
        fp.write(line+'\n')
        fp.write('run;\n')

        line = 'proc format lib=cmshccfm.formats cntlout=cmshccfm.{};'.format(ff)
        fp.write(line+'\n')

        line = 'select a-zzzzzzzz  $a-$zzzzzzzz;'
        fp.write(line+'\n')
        fp.write('run;\n')

        line = 'proc export data=cmshccfm.{}'.format(ff)
        fp.write(line+'\n')

        line = 'outfile="{}.csv"'.format(path)
        fp.write(line+'\n')
        fp.write('dbms=csv\n')
        fp.write('replace;\n')
        fp.write('run;\n')

        fp.write('\n')
