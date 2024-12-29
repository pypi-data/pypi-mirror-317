
""" last update on server: 04.09.2024."""

month={
	"Jan":"01",
	"Feb":"02",
	"Mar":"03",
	"Apr":"04",
	"May":"05",
	"Jun":"06",
	"Jul":"07",
	"Aug":"08",
	"Sep":"09",
	"Oct":"10",
	"Nov":"11",
	"Dec":"12"
}

periodic_table_dict={'1':'H','2':'He','3':'Li','4':'Be','5':'B','6':'C',
					 '7':'N','8':'O','9':'F','10':'Ne','11':'Na','12':'Mg',
					 '13':'Al','14':'Si','15':'P','16':'S','17':'Cl',
					 '18':'Ar','19':'K','20':'Ca','21':'Sc','22':'Ti',
					 '23':'V','24':'Cr','25':'Mn','26':'Fe','27':'Co',
					 '28':'Ni','29':'Cu','30':'Zn','31':'Ga','32':'Ge',
					 '33':'As','34':'Se','35':'Br','36':'Kr','37':'Rb',
					 '38':'Sr','39':'Y','40':'Zr','41':'Nb','42':'Mo',
					 '43':'Tc','44':'Ru','45':'Rh','46':'Pd','47':'Ag',
					 '48':'Cd','49':'In','50':'Sn','51':'Sb','52':'Te',
					 '53':'I','54':'Xe','55':'Cs','56':'Ba','57':'La',
					 '58':'Ce','59':'Pr','60':'Nd','61':'Pm','62':'Sm',
					 '63':'Eu','64':'Gd','65':'Tb','66':'Dy','67':'Ho',
					 '68':'Er','69':'Tm','70':'Yb','71':'Lu','72':'Hf',
					 '73':'Ta','74':'W','75':'Re','76':'Os','77':'Ir',
					 '78':'Pt','79':'Au','80':'Hg','81':'Tl','82':'Pb',
					 '83':'Bi','84':'Po','85':'At','86':'Rn','87':'Fr',
					 '88':'Ra','89':'Ac','90':'Th','91':'Pa','92':'U',
					 '93':'Np','94':'Pu','95':'Am','96':'Cm','97':'Bk',
					 '98':'Cf','99':'Es','100':'Fm','101':'Md','102':'No',
					 '103':'Lr','104':'Rf','105':'Db','106':'Sg','107':'Bh',
					 '108':'Hs','109':'Mt'}

atomic_mass={'H': '1', 'He': '2', 'Li': '3', 'Be': '4', 'B': '5', 'C': '6',
             'N': '7', 'O': '8', 'F': '9', 'Ne': '10', 'Na': '11', 'Mg': '12',
             'Al': '13', 'Si': '14', 'P': '15', 'S': '16', 'Cl': '17', 'Ar': '18',
             'K': '19', 'Ca': '20', 'Sc': '21', 'Ti': '22', 'V': '23', 'Cr': '24',
             'Mn': '25', 'Fe': '26', 'Co': '27', 'Ni': '28', 'Cu': '29', 'Zn': '30',
             'Ga': '31', 'Ge': '32', 'As': '33', 'Se': '34', 'Br': '35', 'Kr': '36',
             'Rb': '37', 'Sr': '38', 'Y': '39', 'Zr': '40', 'Nb': '41', 'Mo': '42',
             'Tc': '43', 'Ru': '44', 'Rh': '45', 'Pd': '46', 'Ag': '47', 'Cd': '48',
             'In': '49', 'Sn': '50', 'Sb': '51', 'Te': '52', 'I': '53', 'Xe': '54',
             'Cs': '55', 'Ba': '56', 'La': '57', 'Ce': '58', 'Pr': '59', 'Nd': '60',
             'Pm': '61', 'Sm': '62', 'Eu': '63', 'Gd': '64', 'Tb': '65', 'Dy': '66',
             'Ho': '67', 'Er': '68', 'Tm': '69', 'Yb': '70', 'Lu': '71', 'Hf': '72',
             'Ta': '73', 'W': '74', 'Re': '75', 'Os': '76', 'Ir': '77', 'Pt': '78',
             'Au': '79', 'Hg': '80', 'Tl': '81', 'Pb': '82', 'Bi': '83', 'Po': '84',
             'At': '85', 'Rn': '86', 'Fr': '87', 'Ra': '88', 'Ac': '89', 'Th': '90',
             'Pa': '91', 'U': '92', 'Np': '93', 'Pu': '94', 'Am': '95', 'Cm': '96',
             'Bk': '97', 'Cf': '98', 'Es': '99', 'Fm': '100', 'Md': '101', 'No': '102',
             'Lr': '103', 'Rf': '104', 'Db': '105', 'Sg': '106', 'Bh': '107', 'Hs': '108', 'Mt': '109'}

#TODO-------------------------------------------------------------------------------------------------------------

def checker_gaussian(opened_file, pointer=False, position=0):
    """_summary_

    Args:
        opened_file (_type_): _description_
        pointer (bool, optional): _description_. Defaults to False.
        position (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    from os import SEEK_SET
    
    opened_file.seek(position,SEEK_SET)
    first_five_lines=opened_file.readlines()[:5:1]
    first_five_lines="".join(first_five_lines)
    if first_five_lines.find("Gaussian") != -1:
        if bool(pointer):
            position=opened_file.tell()
            return True, position
        return True
    else:
        return False

def checker_normaltermination(opened_file, position=0, pointer=False):
    """_summary_

    Args:
        opened_file (_type_): _description_
        position (int, optional): _description_. Defaults to 0.
        pointer (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    from os import SEEK_SET
    
    opened_file.seek(position, SEEK_SET)
    line_content=opened_file.readlines()[:-5:-1]
    last_five_lines="".join(line_content)
    if last_five_lines.find("Normal termination") != -1:
        if pointer:
            position = opened_file.tell()
            return True, position
        else:
            return True
    else:
        return False

def checker_job(opened_file, max_lines_to_check=500, specific=[],pointer=False, position=0): # ez meg nincs kesz
    """It checks the termination of the job.

    Args:
        opened_file (str): _description_
        max_lines_to_check (int, optional): _description_. Defaults to 150.
        specific (list): ide kell a maradek keresese, ami nem freq vagy opt
    """
    
    from os import SEEK_SET
    from re import match
    
    opened_file.seek(position, SEEK_SET)
    line_number = 1
    while line_number <= max_lines_to_check:
        line_content = opened_file.readline()
		#mi kell: csak olyan ahol van opt es freq? vagy lenyegtelen?
        if match(" #.*\n", line_content) or match(".*opt.*\n", line_content) or match(".*freq.*\n", line_content):
            if len(specific)==0:
                if pointer:
                    opened_file.seek(1, SEEK_SET)
                    position=opened_file.tell()
                    return True, position
                else:
                    return True
        for i in specific:
            if i=="TD":
                ...
        line_number += 1
    return False

def collector_job(opened_file, max_lines_to_check=500, pointer=False, position=0):
    """_summary_

    Args:
        opened_file (_type_): _description_
        max_lines_to_check (int, optional): _description_. Defaults to 150.
        pointer (bool, optional): _description_. Defaults to False.
        position (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    
    from os import SEEK_SET
    from re import match, compile, search, VERBOSE
    
    pattern_uncompiled= r"""                                                     
(?=.*\#\s*(?P<opt_method>[a-zA-Z0-9\-]{1,})?\s+(?P<opt_basis>[a-zA-Z0-9\-\*\+\(\)\,]{1,}))?
(?=.*EmpiricalDispersion=(?P<emp_dis>[A-Z0-9]{1,5}))? 
(?=.*TD=\((?=nstate[s]*=(?P<nstates>[0-9]+))?(?=.*root=(?P<root>[0-9]{1,}))?(?=.*add=(?P<add>[0-9]{1,}))?(?=.*conver=(?P<conver>[0-9]{1,}))?(?=.*GOccSt=(?P<GOccSt>[0-9]{1,}))?(?=.*GOccEnd=(?P<GOccEnd>[0-9]{1,}))?(?=.*GDEMin=(?P<GDEMin>[0-9]{1,}))?(?=.*DEMin=(?P<DEMin>[0-9]{1,}))?(?=.*IFact=(?P<IFact>[0-9]{1,}))?(?=.*WhenReduce=(?P<WhenReduce>[0-9]{1,}))?.*)?
(?=.*(?P<opt>opt))?    
(?=.*(?P<freq>freq))?                                                     
"""
    pattern=compile(pattern_uncompiled, VERBOSE)
    pattern_start=r"\s*#.*"
    pattern_hyp=r"-+"
    line_number=0
    opened_file.seek(position,SEEK_SET)
    while line_number<max_lines_to_check:
        line_content=opened_file.readline()
        if match(pattern_start, line_content)!=None:
            values=match(pattern, line_content)
            values=values.groupdict()
            line_content=opened_file.readline()
            if match(pattern_hyp, line_content)!=None:
                values1=match(pattern, line_content)
                values1=values1.groupdict()
                values.update(values1)
                del values1
            basis=values["opt_basis"]
            method=values["opt_method"]
            del values['opt_basis']
            del values['opt_method']
            line_number=max_lines_to_check
            if pointer:
                position=opened_file.tell()
                return method, basis, values, position
            return method, basis, values
            opened_file.seek(1,SEEK_SET)
        else:line_number+=1
    
def collector_DateNormalTermination(opened_file, pointer=False, position=0):
    from os import SEEK_SET
    from re import match
    
    pattern_Date_NormalTermination="^ Normal termination of Gaussian [a-zA-Z0-9]* at \w* (?P<month>\w{1,})[\s]* (?P<day>\w{1,}) (?P<hour>\w{1,})\:(?P<min>\w{1,})\:(?P<sec>\w{1,}) (?P<year>\w{1,})\.\n"
    
    line_content=opened_file.readlines()[:-5:-1]
    opened_file.seek(position,SEEK_SET)
    found=True
    i=0
    while found:
        if len(line_content)>i:
            if match(pattern_Date_NormalTermination,line_content[i]) !=None :
                hours=match(pattern_Date_NormalTermination,line_content[i]).group(3)
                mins=match(pattern_Date_NormalTermination,line_content[i]).group(4)
                secs=match(pattern_Date_NormalTermination,line_content[i]).group(5)
                days=match(pattern_Date_NormalTermination,line_content[i]).group(2)
                months=match(pattern_Date_NormalTermination,line_content[i]).group(1)
                years=match(pattern_Date_NormalTermination,line_content[i]).group(6)
                found=False 
                Date_Normaltermination=str(hours)+":"+str(mins)+":"+str(secs)+":"+"_"+str(days)+":"+str(month[months])+":"+str(years)
                if pointer:
                    position=opened_file.tell()
                    return Date_Normaltermination, position
                return Date_Normaltermination
            else:i+=1
        else: 
            found=False
    return 

def collector_es(opened_file, max_iter=10000,es_method=None, es_basis=None, name=None,pointer=False, position=0, cpu_time=False, nm_function=False):

    from pandas import DataFrame
    from os import SEEK_SET
    from re import match
    
    pattern_es="\s* Excited State\s*(?P<excited_state>[0-9]{1,})\:\s*(?P<es_type>[a-zA-Z\-]{1,})\s*(?P<energy_eV>[0-9\.\-]{1,}) eV\s*(?P<wave_length>[0-9\.]{1,}) nm\s*f\=(?P<osc>[0-9\.]{1,}).*\n"
    pattern_jump="\s*(?P<from_jump>[0-9]{1,})\s+->\s+(?P<to_jump>[0-9]{1,})\s*(?P<wahrscheinlichkeit>[0-9\-\.]{1,})\n"

    
    time, number_functions=None,None
    if cpu_time:
        time=cpu_collector(opened_file)
    if nm_function:
        number_functions=function_collector(opened_file)
    opened_file.seek(position, SEEK_SET)
    row=1
    i=0
    found=True
    df=DataFrame(columns=["excited_state","es_method", "es_basis", "geom_method", "geom_basis","es_type","energy_eV", "wave_length", "jump_from","jump_to","jump","Wahrscheinlichkeit","osc"])
    while i<max_iter and found:
        line_content=opened_file.readline()
        if match(pattern_es, line_content)!=None:
            result=match(pattern_es, line_content)
            excited_state=int(result.group(1))
            es_type=str(result.group(2))
            energy_eV=float(result.group(3))
            wave_length=float(result.group(4))
            osc=float(result.group(5))
            i+=1
            
        if match(pattern_jump, line_content)!=None:
            result=match(pattern_jump, line_content)
            df.loc[row,"excited_state"]=excited_state
            df.loc[row,"es_type"]=es_type
            df.loc[row,"energy_eV"]=energy_eV
            df.loc[row,"wave_length"]=wave_length
            df.loc[row,"osc"]=osc
            df.loc[row,"es_method"]=es_method
            df.loc[row,"es_basis"]=es_basis
            df.loc[row,"jump_from"]=int(result.group(1))
            df.loc[row,"jump_to"]=int(result.group(2))
            df.loc[row,"jump"]=int(result.group(2))-int(result.group(1))
            df.loc[row,"Wahrscheinlichkeit"]=2*float(result.group(3))**2
            df.loc[row,"name"]=name
            #!TODO: ide kell meg hogy a fuggvenyek szamat es a cpu idot belerakja a df-be
            if number_functions!=None:
                df.loc[row,"primitive functions"]
                df.loc[row,"gaussian functions"]
                df.loc[row,"primitive functions"]
            if time!=None:
                ...
            row+=1
            i+=1
        if match("\s*This state.*\n", line_content)!=None:
            for m in range(3):
                line_content=opened_file.readline()
  
        i+=1
        if match(".*SavETr\:.*\n", line_content)!=None:
            found=False
    if pointer:
        position=opened_file.tell()
        return df, position
    else:
        return df

def collector_geom(opened_file, pointer=False, position=0, dframe=False):
    from pandas import DataFrame
    from os import SEEK_SET
    from re import match
    import numpy as np
    
    pattern_g_XYZ="[\s]*(?P<center_number>\d{1,})[\s]*(?P<atomic_number>\d{1,})[\s]*(?P<atomic_type>\d{1,})[\s]*(?P<X>[-|\][0-9.]{1,})[\s]*(?P<Y>[-|\][0-9.]{1,})[\s]*(?P<Z>[-|\][0-9.]{1,})[\s]*\n"
    
    df_g_xyz=DataFrame(columns=['atomic_symbol','X','Y','Z'])
    g_xyz=np.empty((0,3),dtype="float64")
    g_atom=np.empty((0,1))
    opened_file.seek(position,SEEK_SET)
    line_list=opened_file.readlines()[::-1]
    found=True
    i=1
    length=len(line_list)	
	
    while found and i<length:
        line_content=line_list[i]
        if match("\s{1,}Input orientation:\s{1,}\n",line_content) != None or match("\s{1,}Standard orientation:\s{1,}\n",line_content) != None:
            i-=5
            cont_found=True
            while cont_found:
                    line_content=line_list[i]
                    if match(pattern_g_XYZ,line_content) != None:
                        g_xyz_value=match(pattern_g_XYZ,line_content)
                        row=len(df_g_xyz)
                        df_g_xyz.loc[row,"atomic_symbol"]=" "+periodic_table_dict[g_xyz_value.group(2)]
                        df_g_xyz.loc[row,"X"]="   "+g_xyz_value.group(4)
                        df_g_xyz.loc[row,"Y"]="   "+g_xyz_value.group(5)
                        df_g_xyz.loc[row,"Z"]="   "+g_xyz_value.group(6) 
                        atomic_xyz=np.array([float(g_xyz_value.group(4)),float(g_xyz_value.group(5)),float(g_xyz_value.group(6))], ndmin=2)          
                        g_xyz=np.vstack((g_xyz,atomic_xyz),dtype="float64")
                        atom=periodic_table_dict[g_xyz_value.group(2)]
                        g_atom=np.append(g_atom,atom)
                        i-=1            
                    else:
                        cont_found=False
                        found=False
                        if pointer:
                            position=opened_file.tell()
                            if dframe:
                                return g_xyz, df_g_xyz,position
                            return g_xyz, position
                        else:
                            if dframe:
                                return g_xyz,df_g_xyz
                            else:
                                return g_xyz,g_atom
        else: i+=1

def collector_disctance_matrix(opened_file, collected_geom=0,max_iter=100000, position=0, pointer=False):# ezt teljesen be kell fejezni
    
    from os import SEEK_SET
    from re import match
    from numpy import zeros
    
    
    pattern_1="\s*Distance\s*matrix\s\((?P<unit>\w*)\)\:\n"
    # pattern_matrix1="\s*(?P<order>[0-9]{1,})\s*(?P<atomic_symbol>[a-zA-Z]{1,})\s*(?P<distance_1>[0-9\.]{1,})\n"
    # pattern_matrix2="\s*(?P<order>[0-9]{1,})\s*(?P<atomic_symbol>[a-zA-Z]{1,})\s*(?P<distance_1>[0-9\.]{1,})\s*(?P<distance_2>[0-9\.]{1,})\n"
    # pattern_matrix3="\s*(?P<order>[0-9]{1,})\s*(?P<atomic_symbol>[a-zA-Z]{1,})\s*(?P<distance_1>[0-9\.]{1,})\s*(?P<distance_2>[0-9\.]{1,})\s*(?P<distance_3>[0-9\.]{1,})\n"
    # pattern_matrix4="\s*(?P<order>[0-9]{1,})\s*(?P<atomic_symbol>[a-zA-Z]{1,})\s*(?P<distance_1>[0-9\.]{1,})\s*(?P<distance_2>[0-9\.]{1,})\s*(?P<distance_3>[0-9\.]{1,})\s*(?P<distance_4>[0-9\.]{1,})\n"
    pattern_matrix5="\s*(?P<order>[0-9]+)\s*(?P<atomic_symbol>[a-zA-Z]+)\s*(?P<distance_1>[0-9\.]*)\s*(?P<distance_2>[0-9\.]*)\s*(?P<distance_3>[0-9\.]*)\s*(?P<distance_4>[0-9\.]*)\s*(?P<distance_5>[0-9\.]*)\n"
    pattern_order_matrix="\s*(?P<atom_order1>\d*)\s*(?P<atom_order2>\d*)\s*(?P<atom_order3>\d*)\s*(?P<atom_order4>\d*)\s*(?P<atom_order5>\d*)\s*\n"
    
    
    
    num_atom=len(collected_geom)
    opened_file.seek(position,SEEK_SET)
    line_content=opened_file.readlines()[::1]
    found=True
    found_2=True
    found_3=True
    i=0
    matrix=zeros((num_atom,num_atom),dtype='float64')
    while i<max_iter and found:
        if match(pattern_1, line_content[i])!=None:
            unit=str(match(pattern_1, line_content[i]).group(2))
            while found_2:
                i=+1
                if match(pattern_order_matrix, line_content[i])!=None: #ez kell hogy indexelni tudjuk 
                    result_order=match(pattern_order_matrix, line_content[i])
                    order_1=int(result_order.group(1))
                    if order_1!=None:
                        m=1
                    order_2=int(result_order.group(2))
                    if order_2!=None:
                        m=2
                    order_3=int(result_order.group(3))
                    if order_3!=None:
                        m=3
                    order_4=int(result_order.group(4))
                    if order_4!=None:
                        m=4
                    order_5=int(result_order.group(5))
                    if order_5!=None:
                        m=5
                    order_col=[order_1,order_2,order_3,order_4,order_5]
                    i=+1
                if match(pattern_matrix5,line_content[i])!=None:
                    result_distance=match(pattern_matrix5,line_content[i])
                    order_row=result_distance.group(1)
                    atomic_symbol=result_distance.group(2)
                    distance_1=result_distance.group(3)
                    distance_2=result_distance.group(4)
                    distance_3=result_distance.group(5)
                    distance_4=result_distance.group(6)
                    distance_5=result_distance.group(7)
                    distance=[distance_1,distance_2,distance_3,distance_4,distance_5]
                    for a in range(m):
                        matrix[order_row-1][order_col[m]-1]=distance[m]
                    
        i=+1 
    
    ...
            
def standard_orientation(geom, atomic_list):
    import numpy as np
    
    mass_sum=0
    st_origo=np.empty((0,3))
    geom_copy=np.copy(geom)
    for i in range(len(atomic_list)):
        mass_sum+=float(atomic_mass[str(atomic_list[i])])
    geom_copy=geom_copy/mass_sum
    for i in range(len(geom_copy)):
        geom_copy[i]=geom_copy[i]*float(atomic_mass[str(atomic_list[i])])
        st_origo=+geom_copy[i]
    geom=geom_copy-st_origo
    return geom
     
def cpu_collector(opened_file, position=0, pointer=False):
    """collects the cpu time of the last calculation. In case you calculate opt and freq at the same time, 
    it will extract only the required time of the freq calculation.

    Args:
        opened_file (_type_): _description_
        position (int, optional): _description_. Defaults to 0.
        pointer (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    
    from os import SEEK_SET
    from re import match

    
    cpu_time_pattern=r"\s*Job cpu time.* (?P<days>[0-9]+)\s*days\s*(?P<hours>[0-9]+)\s*hours\s*(?P<minutes>[0-9]+)\s*minutes\s*(?P<seconds>[0-9\.]+)\s*seconds.*\n"
    elapsed_time_pattern=r"\s*Elapsed\s*time.* (?P<days>[0-9]+)\s*days\s*(?P<hours>[0-9]+)\s*hours\s*(?P<minutes>[0-9]+)\s*minutes\s*(?P<seconds>[0-9\.]+)\s*seconds.*\n"
    
    line_content=opened_file.readlines()[:-10:-1]
    opened_file.seek(position,SEEK_SET)
    found=True
    i=0
    while found:
        if len(line_content)>i:
            if match(elapsed_time_pattern,line_content[i]) !=None :
                elapsed_time=float(match(elapsed_time_pattern,line_content[i]).group(0))*24+float(match(elapsed_time_pattern,line_content[i]).group(1))+float(match(elapsed_time_pattern,line_content[i]).group(2))/60+float(match(elapsed_time_pattern,line_content[i]).group(3))/3600
            if match(cpu_time_pattern,line_content[i]) !=None :
                cpu_time=float(match(cpu_time_pattern,line_content[i]).group(0))*24+float(match(cpu_time_pattern,line_content[i]).group(1))+float(match(cpu_time_pattern,line_content[i]).group(2))/60+float(match(cpu_time_pattern,line_content[i]).group(3))/3600
                found=False
            i+=1
            
    if pointer:
        position=opened_file.tell()
        return cpu_time, elapsed_time, position
    return cpu_time, elapsed_time
    
    
def function_collector(opened_file, maxiter=3000, position=0, pointer=False):
    """Collects the number of functions used for the calculation.

    Args:
        opened_file (_type_): _description_
        maxiter (int, optional): _description_. Defaults to 3000.
        position (int, optional): _description_. Defaults to 0.
        pointer (bool, optional): _description_. Defaults to False.
    """
    from os import SEEK_SET
    from re import match

    functions_pattern=r"\s*(?P<basis_function>[0-9]{1,})\sbasis function.*\s(?P<primitive_gaussian>[0-9]{1,})\s*primitive gaussians.*\s(?P<cartesion_basis_function>[0-9]{1,})\scartesian\s*basis\s*functions.*\n"
    opened_file.seek(position, SEEK_SET)
    for i in range(maxiter):
        line_content = opened_file.readline()
		#mi kell: csak olyan ahol van opt es freq? vagy lenyegtelen?
        if match(functions_pattern, line_content):
            if pointer:
                number_function=match(functions_pattern, line_content).groupdict()
                opened_file.seek(1, SEEK_SET)
                position=opened_file.tell()
                return number_function, position
            else:
                return (match(functions_pattern, line_content).groupdict())

    return None
    
    
    
    
    
    
    
    
    
    
    ...
    





























