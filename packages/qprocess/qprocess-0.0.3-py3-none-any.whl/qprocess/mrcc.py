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

#TODO------------------------------------------------------------------------------------------------------------------

def checker_mrcc(opened_file, pointer=False, position=0):#kesz
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
	if first_five_lines.find("MRCC") != -1:
		if bool(pointer):
			position=opened_file.tell()
			return True, position
		return True
	else:
		return False

def checker_normaltermination(opened_file, position=0, pointer=False):#kesz
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
    
def checker_job(opened_file, max_lines_to_check=150, specific=[],pointer=False, position=0):# ez majd ki kell egesziteni a jobokkal
    ...

def collector_job(opened_file, max_iter:int=150, pointer:bool=False, position:int=0):
	"""_summary_

	Args:
		opened_file (_type_): _description_
		max_iter (int, optional): _description_. Defaults to 150.
		position (int, optional): _description_. Defaults to 0.
		pointer (bool, optional): _description_. Defaults to False.

	Returns:
		_type_: _description_
	"""
	from os import SEEK_SET
	from re import match

	pattern_calc="calc=(?P<calc>[a-zA-Z0-9,*()-]{1,})\n"
	pattern_basis="basis=(?P<basis>[a-zA-Z0-9,*()-]{1,})\n"
	basis, calc=None, None
	opened_file.seek(position, SEEK_SET)
	for i in range(max_iter):
		line_content=opened_file.readline()
		if match(pattern_calc, line_content)!=None:
			calc=match(pattern_calc, line_content).group(1)
		if match(pattern_basis, line_content)!=None:
			basis=match(pattern_basis, line_content).group(1)
		if (basis!=None) and (calc!=None):
			if pointer:
				position=opened_file.tell()
				return calc, basis, position
			return calc, basis
	if pointer:
		position=opened_file.tell()
		return calc, basis, position
	return calc, basis

    
def collector_DateNormalTermination(opened_file, pointer=False, position=0):#kesz
	from os import SEEK_SET
	from re import match

	pattern_Date_NormalTermination="\s*[*]*\s*(?P<year>[0-9]+)\-(?P<month>[0-9]+)\-(?P<day>[0-9]+)\s*(?P<hour>[0-9]+)\:(?P<min>[0-9]+)\:(?P<sec>[0-9]+)\s\**\n"

	opened_file.seek(position, SEEK_SET)
	line_content=opened_file.readlines()[:-5:-1]
	last_five_lines="".join(line_content)
	found=True
	i=0
	while found:
		if len(line_content)>i:
			if match(pattern_Date_NormalTermination,line_content[i]) !=None :
				hours=match(pattern_Date_NormalTermination,line_content[i]).group(4)
				mins=match(pattern_Date_NormalTermination,line_content[i]).group(5)
				secs=match(pattern_Date_NormalTermination,line_content[i]).group(6)
				days=match(pattern_Date_NormalTermination,line_content[i]).group(3)
				months=match(pattern_Date_NormalTermination,line_content[i]).group(2)
				years=match(pattern_Date_NormalTermination,line_content[i]).group(1)
				found=False 
				Date_Normaltermination=str(hours)+":"+str(mins)+":"+str(secs)+"__"+str(days)+":"+str(months)+":"+str(years)
				if pointer:
					position=opened_file.tell()
					return Date_Normaltermination, position
				return Date_Normaltermination
			else:i+=1
		else: 
			found=False
	return 
    
def collector_es(opened_file, max_iter=10000,es_method=None, es_basis=None, name=None,pointer=False, position=0, unit=False, specific=[]):#kesz
	from os import SEEK_SET
	from re import match
	from pandas import DataFrame 
    
	pattern_first="\s*Final result of the ADC\(2\) calculations for the excited states\:\n"
	pattern_unit="[a-zA-Z\s]*\[(?P<es_energy_au>[a-zA-Z]+)\][a-zA-Z\s]*\[(?P<es_energy_eV>[a-zA-Z]+)\][a-zA-Z\s]*\[(?P<es_energy_cm>[a-zA-Z0-9\-\^]+)\][a-zA-Z\s]*\[(?P<absorb_energy_nm>[a-zA-Z]+)\]\s*\n"
	pattern_es="\s*(?P<es>[0-9\.\-]*)\s*(?P<es_energy_au>[0-9\.\-]*)\s*(?P<es_energy_eV>[0-9\.\-]*)\s*(?P<es_energy_cm>[0-9\.\-]*)\s*(?P<es_energy_nm>[0-9\.\-]*)\s*\n"

	opened_file.seek(position, SEEK_SET)
	line_content=opened_file.readlines()[::-1]
	found=True
	i=0
	df=DataFrame(columns=["excited_state","es_method", "es_basis", "geom_method", "geom_basis","es_type","energy_eV", "wave_length", "jump_from","jump_to","jump","Wahrscheinlichkeit","osc"])
	while found:
		if match(pattern_first, line_content[i])!=None:
			i-=4
			if match(pattern_unit, line_content[i])!=None:
				units=[match(pattern_unit, line_content[i]).group(1),match(pattern_unit, line_content[i]).group(2),
          			match(pattern_unit, line_content[i]).group(3),match(pattern_unit, line_content[i]).group(4)]
				i-=2
				while found:
					if match(pattern_es, line_content[i])!=None:
						row=len(df)
						df.loc[row,"excited_state"]=match(pattern_es,line_content[i]).group(1)
						df.loc[row,"es_method"]=es_method
						df.loc[row,"es_basis"]=es_basis
						df.loc[row,"wave_length"]=match(pattern_es,line_content[i]).group(5)
						df.loc[row,"name"]=name
      
						if "au" in specific:
							df.loc[row,"es_energy_au"]=match(pattern_es,line_content[i]).group(2)
						if "eV" in specific:
							df.loc[row,"energy_eV"]=match(pattern_es,line_content[i]).group(3)
						if "cm" in specific:
							df.loc[row,"es_energy_cm"]=match(pattern_es,line_content[i]).group(4)
						i-=1
					else:
						if pointer:
							position=opened_file.tell()
							return df, position
						else:
							return df
		i+=1

def collector_geom(opened_file, pointer=False, position=0):# kesz
	"""bele kell irni h mit csinal, mit, milyen sorrendben ad vissza es hogy a df hogy nez ki

	Args:
		opened_file (_type_): _description_
		pointer (bool, optional): _description_. Defaults to False.
		position (int, optional): _description_. Defaults to 0.
	"""
    
    
	from os import SEEK_SET
	from re import match
	from pandas import DataFrame 
    
	pattern_first="\s*(?P<coord_sys>[a-zA-Z]*)[\s]*coordinates in standard orientation\s*\[(?P<unit>[a-zA-Z]*)\]\s*\n"
	pattern_geom="\s*(?P<order>[0-9]+)\s*(?P<symb_atoms>[a-zA-Z]+)\s*(?P<x_coord>[0-9\.\-]+)\s*(?P<y_coord>[0-9\.\-]+)\s*(?P<z_coord>[0-9\.\-]+)\s*\n"

	opened_file.seek(position, SEEK_SET)
	line_content=opened_file.readlines()[::-1]
	found=True
	i=0
	df=DataFrame(columns=['coordinate system','unit of length','order','atomic_symbol','X','Y','Z'])
	while found:
		if match(pattern_first, line_content[i])!=None:
			coord_sys=str(match(pattern_first, line_content[i]).group(1))
			unit=str(match(pattern_first, line_content[i]).group(2))
			i-=1
			while found:
				alma=line_content[i]
				if match(pattern_geom, line_content[i])!=None:
					row=len(df)
					df.loc[row,"unit of length"]=unit
					df.loc[row,"coordinate system"]=coord_sys
					df.loc[row,"order"]=match(pattern_geom,line_content[i]).group(1)
					df.loc[row,"atomic_symbol"]=match(pattern_geom,line_content[i]).group(2)
					df.loc[row,"X"]=match(pattern_geom,line_content[i]).group(3)
					df.loc[row,"Y"]=match(pattern_geom,line_content[i]).group(4)
					df.loc[row,"Z"]=match(pattern_geom,line_content[i]).group(5)
					i-=1
				else:
					if pointer:
						position=opened_file.tell()
						return df, position
					else:
						return df
		i+=1

def collector_osc_length(opened_file, pointer=False, position=0,specific=[]):#kesz
	"""_summary_

	Args:
		opened_file (_type_): _description_
		pointer (bool, optional): _description_. Defaults to False.
		position (int, optional): _description_. Defaults to 0.
		specific (list, optional): _description_. Defaults to [].

	Returns:
		_type_: _description_
	"""
    
	from os import SEEK_SET
	from re import match
	from pandas import DataFrame 
    
	pattern_first="\s* Final result for excited states\:\s*\n"
	pattern_osc="\s*(?P<es>[0-9\.\-]+)\s*(?P<something>[0-9\.\-]*)\s*(?P<x>[0-9\.\-]+)\s*(?P<y>[0-9\.\-]+)\s*(?P<z>[0-9\.\-]+)\s*(?P<es_dipol_strength>[0-9\.\-]+)\s*(?P<es_osc_strength>[0-9\.\-]+)\s*\n"

	opened_file.seek(position, SEEK_SET)
	line_content=opened_file.readlines()[::-1]
	found=True
	i=1
	df=DataFrame(columns=["excited_state","es_method", "es_basis", "geom_method", "geom_basis","es_type","energy_eV", "wave_length", "jump_from","jump_to","jump","Wahrscheinlichkeit","osc"])
	while found:
		if match(pattern_first, line_content[i])!=None:
			i-=7
			while found:
				if match(pattern_osc, line_content[i])!=None:
					row=len(df)
					df.loc[row,"excited_state"]=match(pattern_osc,line_content[i]).group(1)
					df.loc[row,"osc"]=match(pattern_osc,line_content[i]).group(7)
					if 'geom' in specific:
						df.loc[row,"x"]=match(pattern_osc,line_content[i]).group(3)
						df.loc[row,"y"]=match(pattern_osc,line_content[i]).group(4)
						df.loc[row,"z"]=match(pattern_osc,line_content[i]).group(5)
					if 'dipol' in specific:
						df.loc[row,"dipol"]=match(pattern_osc,line_content[i]).group(6)
					i-=1
				else:
					if pointer:
						found=False
						position=opened_file.tell()
						return df, position
					else:
						found=False
						return df
					


		i+=1
    


    




























