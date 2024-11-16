# Manufacturer Usage Description (MUD) through X509
Implementation of the MUD architecture (Manufacturer Usage Description) through the use of x509 certs.

### TODO LIST

>[!TODO] Guardare IoTLab

>[!DONE] Crea un'architettura di riferimento
>
>Fatto! Vedi [[Architettura di riferimento]]

>[!DONE] Sistema lo schema dell'architettura e crea un diagramma di flusso del comportamento della tua simulazione
>
>Vedi sezione [[Architettura di riferimento]]
>

>[!DONE] verifica se esiste il campo per queste estensioni di ASN1
>
>Sì! Esiste, ed è riportato nella RFC di MUD. L'inserimento dei valori di questi campi è stato simulato con un apposito script in Python, che genera CA, certificato del MUDFS del manufacturer e certificato del device, con relative chiavi!
>

>[!WARNING] Rendi lo script di cui sopra scalabile!
>
>Deve poter risalire la chain of trust fra il file .p7s e il dispositivo di IoT che lo riceve.
>MANCANTI:
>	- Controllare che file .p7s è firmato dal mudfs
>	- Controllo che mudfs e iot dev risalgano alla stessa CA
>

>[!TODO] Chiudere il giro di MUD, con ottenimento delle iptables e la verifica delle comunicazioni
>
>Dopo di che, passa alla sperimentazione su Fit IoTLab

>[!TODO] Crea un ambiente riproducibile con Ansible

>[!TODO] Cercare reference per tesi
>
>In particolare, vedere come fare i test.

>[!WARNING] See [[Architettura di riferimento#Questa architettura è legit?]]
# REFERENCES

Angelo Feraudo's osmud repository: https://github.com/aferaudo/osmud
Angelo Feraudo's UPS: https://github.com/aferaudo/user_policy_server
Dnsmasq patch for osmud: https://github.com/osmud/dnsmasq

## **SCADENZE**

Entro prima di Natale tutta la parte di IoT Lab, integrazione certificati, e comunicazione
Dopo Natale tutta la parte dei DID.
Da Gennaio, test.