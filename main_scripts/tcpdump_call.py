import subprocess

#tcpdump -i @name_of_interface@ -c @count_of_packeg@ @name_of_file@


name_of_interface = ''
count_pack = ''
name_of_file_for_save = ''
command = ['tcpdump', '-i', name_of_interface, '-c', count_pack, '-w', name_of_file_for_save]
tcpdump_call = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
message = tcpdump_call.stdout.read()
tcpdump_call.terminate()
