
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file, open_folder
from pathlib import *
import sys

from nettoolkit.pyJuniper.juniper import Juniper

# ======================================================================================

#### -- cache updates -- ####
def update_cache_juniper(i):
	update_cache(CACHE_FILE, mini_juniper_folder_output=i['mini_juniper_folder_output'])	


def exec_mini_juniper_folder_output_open(i):
	open_folder(i['mini_juniper_folder_output'])
def exec_mini_juniper_file_input_open(i):
	open_text_file(i['mini_juniper_file_input'])

# ================================ [ Juniper ] ========================================

@activity_finish_popup
def mini_juniper_to_set_start(i):
	if i['mini_juniper_file_input'] == '' : return
	p = Path(i['mini_juniper_file_input'])
	input_file = p.name
	output_file = ''
	if i['mini_juniper_folder_output']:
		output_file = i['mini_juniper_folder_output'] + '/' + ".".join(input_file.split(".")[:-1]) + '.set.txt'
	try:
		J = Juniper(i['mini_juniper_file_input'], output_file)    # define a Juniper Object
		s = J.convert_to_set(to_file=True)      # convert the Juniper config to set mode.
	except:
		print(f"[-] Set Conversion faced some issue... Please verify input")

@activity_finish_popup
def mini_juniper_remove_remarks_start(i):
	if i['mini_juniper_file_input'] == '': return
	p = Path(i['mini_juniper_file_input'])
	input_file = p.name
	output_file = ''
	if i['mini_juniper_folder_output']:
		output_file = i['mini_juniper_folder_output'] + '/' + ".".join(input_file.split(".")[:-1]) + '.-remarks.txt'
	try:
		J = Juniper(i['mini_juniper_file_input'], output_file)    # define a Juniper Object
		s = J.remove_remarks(
			to_file=True, 
			config_only=i['mini_juniper_remove_remarks_configonly']
		)
	except:
		print(f"[-] Juniper Remarks removal faced some issue... Please verify input")


# ======================================================================================

JUNIPER_EVENT_FUNCS = {
	'mini_juniper_to_set_btn_start': mini_juniper_to_set_start,
	'mini_juniper_remove_remarks_btn_start': mini_juniper_remove_remarks_start,
	'mini_juniper_folder_output': update_cache_juniper,

	'mini_juniper_file_input_open': exec_mini_juniper_file_input_open,
	'mini_juniper_folder_output_open': exec_mini_juniper_folder_output_open,
}
JUNIPER_EVENT_UPDATERS = set()
JUNIPER_ITEM_UPDATERS = set()
JUNIPER_RETRACTABLES = {'mini_juniper_file_input', 'mini_juniper_folder_output'}

