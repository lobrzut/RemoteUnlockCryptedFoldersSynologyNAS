import paramiko
import re
from getpass import getpass

host = "192.168.1.150"
port = 22
username = "root"
password = ""


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

dir_list = []
dir_list_conv = []
vol_list = []
vol_list_conv = []


# command_dir_path =  
command_find = "find / -type d -name @*@"    #find all crypt folders
# command_unmount = "umount /volume1/mycryptdir"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)


stdin, stdout, stderr = ssh.exec_command(command_find)
lines = stdout.readlines()

print(lines)
for x in lines:
    dir_list.append(x)

print('\nLista zabezbieczonych foledrów:\n ',dir_list, "\n")


for i in dir_list:
    ii = find_between(i,  "@", "@" )
    dir_list_conv.append(ii)

for v in dir_list:
    vv = find_between(v,  "/", "/" )
    vol_list_conv.append(vv)

print(vol_list_conv)

dict_list = dict(zip(dir_list_conv, dir_list))


print(dir_list_conv, '\n')
f = ''
ff = ''
folder = ''
passwd = ''

while f not in dir_list_conv:
    f = input('podaj ktory folder mam zamontowac: \n')
    if f not in dir_list_conv:
        print('nie ma takiego folderu - spróbój ponownie')
    
else:
    print('folder istnieje - zostanie zamontowany')
    passwd = getpass(f'PODAJ HASLO DO FOLDERU /  /: ')
    ff = dict_list[f]

folder = find_between(ff,  "@", "@" )

# while f in dir_list_conv:
#     print(f'{i}: folder istnieje - zostanie zamontowany')
#     if i in dir_list_conv:
        
#         ff = dict_list[i]
#         folder = find_between(ff,  "@", "@" )
#         passwd = input(f'PODAJ HASLO DO FOLDERU / {folder} /: ')
#         break
#     else:
#         print('nie ma takiego folderu')
#         break


index_dir_list_conv = dir_list_conv.index(folder)
volume = vol_list_conv[index_dir_list_conv]



print(f' wykonuje polecenie: mkdir /{volume}/{folder}/')
command_mkdir = f'mkdir /{volume}/{ii}/'
stdin, stdout, stderr = ssh.exec_command(command_mkdir)
lines = stderr.readlines()
print(lines)

print(f' wykonuje polecenie: mount.ecryptfs dla folderu: {folder}')
command_mount = f'mount.ecryptfs /{volume}/@{folder}@ /{volume}/{folder} -o ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_passthrough=n,no_sig_cache,ecryptfs_enable_filename_crypto,passwd={passwd}'
#,passwd={passwd}
stdin, stdout, stderr = ssh.exec_command(command_mount)
lines = stderr.readlines()
print(lines)

print(' wykonuje polecenie: synocheckshare')
command_syn1 = 'cd ..'
command_syn2 = "ls -l"

# stdin, stdout, stderr = ssh.exec_command(command_syn1)
# lines = stdout.readlines()
# print(lines)
stdin, stdout, stderr = ssh.exec_command(command_syn2)
lines = stderr.readlines()
print(lines)


# for x in dir_list:
#     print(x)

# command_mkdir = "mkdir /volume1/tak"
# #command_mount = "mount [/volume1/\@mycryptdir\@/]  /volume1/mycryptdir/ -t ecryptfs -o rw,relatime,ecryptfs_fnek_sig=88...,ecryptfs_sig=88...,ecryptfs_cipher=aes,ecryptfs_key_bytes=32"
# command_mount = "mount.ecryptfs /volume1/@tak@ /volume1/tak -o ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_passthrough=n,no_sig_cache,ecryptfs_enable_filename_crypto,passwd=12345678"
# command_syn = 'synocheckshare'
# #command_unmount = ""


# ssh_stdin.write('input value')
# ssh_stdin.flush()


# print("OK")

#działa:
#mkdir /volume1/tak
#mount.ecryptfs /volume1/@tak@ /volume1/tak -o ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_passthrough=n,no_sig_cache,ecryptfs_enable_filename_crypto,passwd=12345678
#synocheckshare
#synospace --map-file -d

#synoshare --enc_unmount /volume1/@tak@
# unmount - trzeba zroic
# unmount all - trzeba zrobic

ssh.close()