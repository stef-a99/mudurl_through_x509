# Manufacturer Usage Description (MUD) through X509
Implementation of the MUD architecture (Manufacturer Usage Description) through the use of x509 certs.

### TODO LIST

>[!DONE] Crea un'architettura di riferimento
>
>Fatto! Vedi [[Architettura di riferimento]]

>[!TODO] Sistema lo schema dell'architettura e crea un diagramma di flusso del comportamento della tua simulazione
>
>Progressi nella sezione [[Architettura di riferimento#Appunti call del 16 ottobre 2024]]
>

>[!DONE] verifica se esiste il campo per queste estensioni di ASN1
>
>Sì! Esiste, ed è riportato nella RFC di MUD. L'inserimento dei valori di questi campi è stato simulato con un apposito script in Python, che genera CA, certificato del MUDFS del manufacturer e certificato del device, con relative chiavi!
>

>[!TODO] Rendi lo script di cui sopra scalabile!
>
>Deve poter risalire la chain of trust fra il file .p7s e il dispositivo di IoT che lo riceve.

>[!TODO] Crea un ambiente riproducibile con Ansible

>[!WARNING] See [[Architettura di riferimento#Questa architettura è legit?]]
# REFERENCES

Angelo Feraudo's osmud repository: https://github.com/aferaudo/osmud
Angelo Feraudo's UPS: https://github.com/aferaudo/user_policy_server
Dnsmasq patch for osmud: https://github.com/osmud/dnsmasq
