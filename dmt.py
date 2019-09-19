# dmt.py - methods for calling DMT to export BAQ data and re-import after making modifications
import log
import os
import subprocess

# path to the DMT executable, need to double all backslashes due to python string processing
dmt_exe = 'C:\\Epicor\\ERP10.2.300.4Client\\Client\\DMT.exe'

# epicor environment - only change the second part of this expression
dmt_cfg = 'EpicorTest10'
dmt_env = 'net.tcp://CHERRY/' + dmt_cfg

# common parameters for the DMT command
dmt_cmd_base = [dmt_exe,
                '-NoUI',
                '-sso',
                '-ConnectionURL="{0}"'.format(dmt_env),
                '-ConfigValue="{0}"'.format(dmt_cfg)]

def dmt_export(baq, csv_name):
    """Export the data for the given BAQ defined in the configured Epicor environment

    baq: Epicor ID of the BAQ to export
    csv_name: file path of the CSV to export from the specified BAQ
    """
    dmt_cmd = dmt_cmd_base + [
                '-Export',
                '-BAQ="{0}"'.format(baq),
                '-Target="{0}"'.format(csv_name)]

    try:
        result = subprocess.run(dmt_cmd)
    except subprocess.SubprocessError as err:
        log.log('failed to start DMT with error: {0}'.format(err.__str__))

    if result.returncode != 0:
        log.log('DMT command run: `' + ' '.join(dmt_cmd) + '`')
        log.log('DMT exited with error {0}'.format(result.returncode))

def dmt_import(phase, csv_name):
    """Import the new data in the specified file into the configured Epicor environment

    phase: name of the DMT step to use (generally the full name in the DMT left pane)
    csv_name: path to the CSV to import
    """
    dmt_cmd = dmt_cmd_base + [
                '-Update',
                '-Import="{0}"'.format(phase),
                '-Source="{0}"'.format(csv_name)]

    try:
        result = subprocess.run(dmt_cmd)
    except subprocess.SubprocessError as err:
        log.log('failed to start DMT with error: {0}'.format(err.__str__))

    if result.returncode != 0:
        log.log('DMT command run: `' + ' '.join(dmt_cmd) + '`')
        log.log('DMT exited with error {0}'.format(result.returncode))
