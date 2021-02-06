
import boto3
import os

pathclaves=os.getenv("HOME")+"/.ssh/authorized_keys"

#funcion para sacar la clave publica de un usuario
def get_authorized_keys(args):
    iam = boto3.client('iam')
    #try:
    for key_desc in iam.list_ssh_public_keys(UserName=args)["SSHPublicKeys"]:
            key = iam.get_ssh_public_key(UserName=args, SSHPublicKeyId=key_desc["SSHPublicKeyId"], Encoding="SSH")
            if key["SSHPublicKey"]["Status"] == "Active":
                return (key["SSHPublicKey"]["SSHPublicKeyBody"])
#vemos los usuarios de operacion y metemos sus claves en una lista para comparar con lo que hay en el fichero actual
iam = boto3.client('iam')
clavesaws = []
for user in iam.list_users()['Users']:
        if (user['UserName'].isdigit()):
                usuario=(user['UserName'])
                clave= get_authorized_keys(usuario)
                clavesaws.insert(len(clavesaws),clave)
                #print("user:",usuario,clave)
clavesawsconcontenido=filter(None.__ne__, clavesaws)
#ahora vamos a crear otra array con las que estan en el fichero de claves
clavesmaquina=[]
with open(pathclaves,'r') as fichread:
        clavesmaquina = fichread.readlines()
fichread.close()

#ahora hay que hacer un "merge" de las quwe hay y las nuevas, teniendo en cuenta que las dos primeras son las de "fabrica"
clavesactualizadas=[]
clavesactualizadas.insert(len(clavesactualizadas),clavesmaquina[0].rstrip('\n'))
#normalmente la de sistema es solo una pero en algunos casos hay dos...meto ambas
#clavesactualizadas.insert(len(clavesactualizadas),clavesmaquina[1].rstrip('\n'))
for i in clavesawsconcontenido:
                clavesactualizadas.insert(len(clavesactualizadas),i)
#print (clavesactualizadas)
#ahora reconstruimos el fichero "HOME/.ssh/authorized_keys"
with open(pathclaves,'w') as fichwrite:
        for lineas in clavesactualizadas:
                print(lineas, file=fichwrite)
fichwrite.close()
